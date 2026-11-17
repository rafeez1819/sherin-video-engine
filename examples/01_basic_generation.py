from src.config import Settings
from src.engine import VideoEngine


def main() -> None:
    engine = VideoEngine(
        Settings(
            fps=60,
            resolution="1080p",
            duration=3,
            keyframe_interval=1.0,
        )
    )
    result = engine.generate(
        "A futuristic cityscape at night with glowing neon lights",
        style="cinematic",
    )
    result.save("output/neon_city.mp4")
    print(f"Saved {result.path.resolve()} @ {result.fps} FPS")


if __name__ == "__main__":
    main()
