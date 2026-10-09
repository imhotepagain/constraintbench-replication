from string import Template

import pytest

from cbench.prompts import PROMPTS_DIR, load_prompt

ALL_PROMPTS = sorted((path.parent.name, path.stem) for path in PROMPTS_DIR.glob("*/*.md"))

TASK_VARIABLES = {
    "scenario": "A dealership network must choose which distribution centers to open.",
    "problem_data": "GearPoint Central PDC (id: f1): capacity=500, fixed_cost=$42000",
    "constraints": "f1 must remain open.",
    "objective": "Minimize total cost.",
    "output_schema": '{"type": "object"}',
}


def test_prompt_folder_is_not_empty():
    assert ALL_PROMPTS


@pytest.mark.parametrize("prompt_id,version", ALL_PROMPTS)
def test_frontmatter_matches_template(prompt_id, version):
    prompt = load_prompt(prompt_id, version)
    template = Template(prompt.template)
    assert prompt.meta["status"] in {"draft", "frozen"}
    assert prompt.meta["purpose"]
    assert template.is_valid(), "stray $ in template body; write a literal dollar as $$"
    assert set(prompt.meta["variables"]) == set(template.get_identifiers())


def test_render_fills_placeholders_and_keeps_dollars_in_values():
    text = load_prompt("task", "v1").render(**TASK_VARIABLES)
    assert "fixed_cost=$42000" in text
    assert "$scenario" not in text


def test_render_rejects_missing_or_unknown_variables():
    prompt = load_prompt("task", "v1")
    with pytest.raises(ValueError):
        prompt.render(scenario="only one variable")
    with pytest.raises(ValueError):
        prompt.render(**TASK_VARIABLES, extra="not declared")
