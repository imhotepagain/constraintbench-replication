"""Load and render the versioned prompt templates in prompts/.

Each template is prompts/<id>/<version>.md: YAML frontmatter, then the body.
Placeholders use string.Template syntax ($name), so JSON braces in prompts need
no escaping. See prompts/README.md for the versioning rules.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path
from string import Template

import yaml

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"


@dataclass(frozen=True)
class Prompt:
    id: str
    version: str
    meta: dict
    template: str
    sha256: str  # hash of the whole file; log it with every run

    def render(self, **variables: str) -> str:
        expected = set(self.meta["variables"])
        if set(variables) != expected:
            raise ValueError(
                f"{self.id}/{self.version} expects variables {sorted(expected)}, got {sorted(variables)}"
            )
        return Template(self.template).substitute(variables)


def load_prompt(prompt_id: str, version: str, prompts_dir: Path = PROMPTS_DIR) -> Prompt:
    path = prompts_dir / prompt_id / f"{version}.md"
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    _, front, body = raw.split("---\n", 2)
    meta = yaml.safe_load(front)
    if meta.get("id") != prompt_id or meta.get("version") != version:
        raise ValueError(f"{path}: frontmatter id/version don't match the file path")
    return Prompt(
        id=prompt_id,
        version=version,
        meta=meta,
        template=body.strip(),
        sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    )
