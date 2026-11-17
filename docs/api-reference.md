# API Reference

## `Settings`

Controls FPS, resolution, duration, keyframe interval, enhancement, and output format.

## `VideoEngine`

- `generate(prompt, **options)` generates a video and returns `VideoOutput`.
- `clear()` resets the frame buffer and keyframe cache.

## `VideoOutput`

- `path` contains the generated file path.
- `save(destination)` copies the generated file to a destination.

## `KeyframeGenerator`

Pass a callback through `connect()` or `VideoEngine(keyframe_generator=...)` to use an external image backend.
