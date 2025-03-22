import edge_tts

TEXT = "Hello World!"
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"


def main() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    communicate.save_sync(OUTPUT_FILE)


if __name__ == "__main__":
    main()