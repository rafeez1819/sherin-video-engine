from src.config import RESOLUTION_MAP, Settings


def main() -> None:
    print("SHERIN Video Engine specifications")
    for name, dimensions in RESOLUTION_MAP.items():
        print(f"{name}: {dimensions[0]}x{dimensions[1]}")
    print(f"Default FPS: {Settings().fps}")


if __name__ == "__main__":
    main()
