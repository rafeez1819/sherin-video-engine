"""A small built-in visual concept catalog."""


class AssetCatalog:
    def __init__(self) -> None:
        self.entries = {
            "cityscape": {
                "palette": "neon",
                "subjects": ["city"],
                "objects": ["buildings"],
            },
            "robot": {
                "palette": "metal",
                "subjects": ["robot"],
                "objects": ["machinery"],
            },
            "portrait": {
                "palette": "natural",
                "subjects": ["person"],
                "objects": ["camera"],
            },
            "nature": {
                "palette": "organic",
                "subjects": ["landscape"],
                "objects": ["trees"],
            },
        }

    def lookup(self, prompt: str) -> list[str]:
        prompt_lower = prompt.lower()
        return [name for name in self.entries if name in prompt_lower]
