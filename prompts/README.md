# Prompts

Every prompt sent to an LLM lives here, one file per version: `prompts/<id>/<version>.md`. Keeping them versioned means every result can be traced back to the exact text the model saw.

| id | Used for | First needed |
|---|---|---|
| `task` | The problem given to the evaluated model (single turn, answer in JSON) | Milestone 2 |
| `scenario` | Turns a generated problem's data into a business story | Milestone 2 |
| `feedback` | Tells the model which constraints its answer broke (extension A) | Milestone 6 |
| `solver_code` | Asks the model to write Gurobi code instead of answering directly (extension C) | Milestone 7 |

## File format

YAML frontmatter, then the template body:

```markdown
---
id: task
version: v1
status: draft          # draft | frozen
purpose: What this prompt is for.
variables: [scenario, problem_data]
---
$scenario

$problem_data
```

- Placeholders use Python `string.Template` syntax: `$name` or `${name}`. Write a literal dollar sign in the body as `$$`. Values filled in at render time (such as `fixed_cost=$42000`) need no escaping.
- `variables` must list exactly the placeholders in the body. `tests/test_prompts.py` checks this for every file.

## Rules

1. `draft` prompts can be edited freely.
2. The first time a prompt is used in a recorded run, set `status: frozen`. After that, **never edit it**: copy it to the next version (`v2.md`), change the copy, and use the new version.
3. Every run logs the prompt's `id`, `version` and `sha256`, so a result can always be matched to its prompt.

## Usage

```python
from cbench.prompts import load_prompt

prompt = load_prompt("task", "v1")
text = prompt.render(scenario=..., problem_data=..., constraints=..., objective=..., output_schema=...)
prompt.sha256  # log this with the run
```
