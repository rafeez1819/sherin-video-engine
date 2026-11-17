"""Prompt resolution helpers."""

from dataclasses import dataclass, field

from .catalog import AssetCatalog


@dataclass
class SceneBlueprint:
    prompt: str
    subjects: list[str] = field(default_factory=list)
    objects: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    style_hint: str = "cinematic"


class AssetResolver:
    def __init__(self) -> None:
        self.catalog = AssetCatalog()

    def analyze(self, prompt: str) -> SceneBlueprint:
        matches = self.catalog.lookup(prompt)
        subjects = []
        objects = []
        attributes = []

        for name in matches:
            entry = self.catalog.entries[name]
            subjects.extend(entry["subjects"])
            objects.extend(entry["objects"])
            attributes.append(entry["palette"])

        style_words = ("cinematic", "futuristic", "minimal", "natural")
        style_hint = next(
            (word for word in style_words if word in prompt.lower()), "cinematic"
        )
        actions = ["move", "glow"] if "city" in prompt.lower() else ["move"]

        return SceneBlueprint(
            prompt=prompt,
            subjects=subjects,
            objects=objects,
            attributes=attributes,
            actions=actions,
            style_hint=style_hint,
        )
