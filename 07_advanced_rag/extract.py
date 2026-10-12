
from pathlib import Path
from pypdf import PdfReader


def extract_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages = []

    for page_number, page in enumerate(
        reader.pages, start=1
    ):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip(),
            })

    return pages


if __name__ == "__main__":
    pdf_path = Path("documents/recovery-plan.pdf")

    for page in extract_pdf(str(pdf_path)):
        print(
            f"Page {page['page']}: "
            f"{len(page['text'])} characters"
        )
