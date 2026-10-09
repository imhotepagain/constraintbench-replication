"""Sanity-check the environment for the ConstraintBench reproduction.

Run with:  uv run python scripts/check_env.py
"""

import importlib
import math
import os
import sys

from dotenv import load_dotenv

load_dotenv()

ok = True


def report(label, passed, detail=""):
    global ok
    ok &= passed
    print(f"[{'OK ' if passed else 'FAIL'}] {label}" + (f"  ({detail})" if detail else ""))


# 1. Python version
report("Python >= 3.11", sys.version_info >= (3, 11), sys.version.split()[0])

# 2. Packages
for pkg in ["gurobipy", "pydantic", "yaml", "openai", "anthropic", "google.genai", "pandas", "cbench"]:
    try:
        mod = importlib.import_module(pkg)
        report(f"import {pkg}", True, getattr(mod, "__version__", ""))
    except ImportError as e:
        report(f"import {pkg}", False, str(e))

# 3. Gurobi: solve a tiny facility-location MIP (same structure as the paper's Appendix A)
try:
    import gurobipy as gp
    from gurobipy import GRB

    customers = {"c1": ((12, 18), 70), "c2": ((30, 5), 40), "c3": ((45, 40), 55)}
    facilities = {  # (x, y), capacity, fixed_cost, var_cost
        "f1": ((16, 16), 500, 42000, 3.6),
        "f2": ((40, 30), 120, 25000, 4.1),
        "f3": ((35, 10), 90, 18000, 5.0),
    }
    max_dist = 50

    m = gp.Model("smoke_test")
    m.Params.OutputFlag = 0
    y = m.addVars(facilities, vtype=GRB.BINARY, name="open")
    x = m.addVars(customers, facilities, lb=0, ub=1, name="assign")
    m.setObjective(
        gp.quicksum(facilities[j][2] * y[j] for j in facilities)
        + gp.quicksum(facilities[j][3] * customers[i][1] * x[i, j] for i in customers for j in facilities),
        GRB.MINIMIZE,
    )
    m.addConstrs(x.sum(i, "*") == 1 for i in customers)
    m.addConstrs(x[i, j] <= y[j] for i in customers for j in facilities)
    m.addConstrs(
        gp.quicksum(customers[i][1] * x[i, j] for i in customers) <= facilities[j][1] * y[j] for j in facilities
    )
    for i, ((cx, cy), _) in customers.items():
        for j, ((fx, fy), *_rest) in facilities.items():
            if math.dist((cx, cy), (fx, fy)) > max_dist:
                m.addConstr(x[i, j] == 0)
    m.addConstr(y["f1"] == 1)  # "f1 must remain operational"
    m.optimize()

    solved = m.Status == GRB.OPTIMAL
    opened = [j for j in facilities if y[j].X > 0.5] if solved else []
    report("Gurobi solves a MIP", solved, f"v{'.'.join(map(str, gp.gurobi.version()))}, obj={m.ObjVal:,.1f}, open={opened}")
except Exception as e:
    report("Gurobi solves a MIP", False, str(e))

# 4. API keys (only checks presence, never prints them)
for var in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]:
    present = bool(os.getenv(var))
    print(f"[{'OK ' if present else '-- '}] {var} {'set' if present else 'not set (add to .env when ready)'}")

print("\nCore environment ready." if ok else "\nSomething is missing — see FAIL lines above.")
