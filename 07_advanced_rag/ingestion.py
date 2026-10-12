
import hashlib
from pathlib import Path

from clients import search_client, embed
from extract import extract_pdf
from chunking import split_text


def document_id_for(path: Path) -> str:
    # Stable across content updates to the same filename.
    return hashlib.sha256(
        path.name.encode("utf-8")
    ).hexdigest()[:24]


def get_existing_chunks(document_id: str) -> list[dict]:
    safe_id = document_id.replace("'", "''")

    results = search_client.search(
        search_text="*",
        filter=f"document_id eq '{safe_id}'",
        select=["chunk_id", "version"],
        top=1000,
    )

    return [
        {
            "chunk_id": result["chunk_id"],
            "version": result["version"],
        }
        for result in results
    ]


def ingest_pdf(pdf_path: str):
    path = Path(pdf_path)

    document_id = document_id_for(path)
    version = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    old_chunks = get_existing_chunks(document_id)

    if old_chunks and all(
        item["version"] == version
        for item in old_chunks
    ):
        print("Document unchanged; skipping ingestion.")
        return

    pages = extract_pdf(str(path))
    new_chunks = []

    for page in pages:
        chunks = split_text(page["text"])

        for chunk_number, content in enumerate(chunks):
            chunk_id = (
                f"{document_id}-"
                f"{version[:12]}-"
                f"{page['page']}-"
                f"{chunk_number}"
            )

            new_chunks.append({
                "chunk_id": chunk_id,
                "document_id": document_id,
                "version": version,
                "page_number": page["page"],
                "title": path.name,
                "content": content,
                "content_vector": embed(content),
            })

    if not new_chunks:
        raise ValueError("No extractable text found.")

    # Upload new chunks first.
    upload_results = search_client.upload_documents(
        documents=new_chunks
    )

    if not all(result.succeeded for result in upload_results):
        raise RuntimeError(
            "Some chunks failed to upload. "
            "Old chunks were retained."
        )

    # Remove obsolete chunks after successful upload.
    old_ids = {
        item["chunk_id"] for item in old_chunks
    }
    new_ids = {
        item["chunk_id"] for item in new_chunks
    }

    obsolete_ids = old_ids - new_ids

    if obsolete_ids:
        delete_results = search_client.delete_documents(
            documents=[
                {"chunk_id": chunk_id}
                for chunk_id in obsolete_ids
            ]
        )

        if not all(r.succeeded for r in delete_results):
            raise RuntimeError(
                "Some obsolete chunks were not deleted."
            )

    print(
        f"Ingested {len(new_chunks)} chunks "
        f"from {path.name}"
    )


if __name__ == "__main__":
    ingest_pdf("documents/Disaster_Recovery_Plan.pdf")
