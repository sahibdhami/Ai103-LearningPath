
import os

from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()


def transcribe_audio(audio_path: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"],
    )

    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(
        filename=audio_path
    )

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = recognizer.recognize_once()

    if result.reason == (
        speechsdk.ResultReason.RecognizedSpeech
    ):
        return result.text

    if result.reason == (
        speechsdk.ResultReason.NoMatch
    ):
        return "No speech recognized."

    if result.reason == (
        speechsdk.ResultReason.Canceled
    ):
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Speech recognition canceled: "
            f"{cancellation.reason}; "
            f"{cancellation.error_details}"
        )

    return "Recognition did not complete."


if __name__ == "__main__":
    transcript = transcribe_audio(
        "samples/customer-call.wav"
    )

    print("Transcript:", transcript)
