# Architecture Overview

SHERIN uses six pipeline stages:

1. **Prompt resolution** turns text into a scene blueprint.
2. **Keyframe generation** creates or retrieves source images.
3. **Frame buffering** retains ordered frames in a circular 60-slot sequence.
4. **Micro-variation** interpolates between keyframes.
5. **Enhancement** resizes and sharpens every frame.
6. **Assembly** encodes MP4 or WebM output.
