# Milestone 1: reading guide

**Goal:** understand the problem ConstraintBench studies, what it claims, what it leaves open, and where our work fits. **Deliverable:** one page of notes in [`milestone-1-notes.md`](milestone-1-notes.md).

**Time:** about 10 hours over 2 weeks, in 4 sessions.

**PDFs:** `bash scripts/download_papers.sh` saves every paper in this guide to `papers/`, numbered in reading order. That folder is kept out of git.

| Session | What | Time |
|---|---|---|
| 1 | ConstraintBench, sections 1–4 (problem, math, benchmark design) | ~2.5 h |
| 2 | ConstraintBench, sections 5–7 and appendices (results, failures, limitations) | ~2 h |
| 3 | Related work: 6 papers, first pass only | ~3 h |
| 4 | Write the one-page notes, then review them with Claude | ~2 h |

## How to read a paper

Use the three-pass method from S. Keshav's *How to Read a Paper*:

1. **First pass (10 minutes):** title, abstract, introduction, section headings, figures and tables, conclusion. Can you say what the paper does and what it found?
2. **Second pass (1 hour):** read everything except proofs and fine details. Note what you don't understand.
3. **Third pass (only for ConstraintBench):** read as if you had to rebuild it, because we do. For every design choice, ask why they made it and what would change if they hadn't.

Write your answers to the questions below as you go, in your own words. If you get stuck on a concept (MIP, IIS, confidence interval…), ask Claude to explain it with an example from the paper.

---

## Part A: ConstraintBench

Tso et al., 2026. [arXiv:2602.22465](https://arxiv.org/abs/2602.22465) ([HTML version](https://arxiv.org/html/2602.22465v2), easier to read).

### Session 1: sections 1–4

**§1 Introduction**

1. In one sentence each: what do benchmarks like NL4Opt and IndustryOR test (*optimization modeling*), and what does ConstraintBench test (*direct optimization*)? Writing solver code works better in practice. Why do the authors still think direct optimization is worth measuring?
2. List the paper's 4 contributions. Which ones can we check ourselves, and which do we have to take on trust?

**§3 Preliminaries**

3. In your own words, using facility location as the example, explain: decision variable, constraint, objective, feasible solution, optimal solution.
4. Copy the facility-location formulation from §3.3 and explain each constraint in plain words. We build this domain first, in milestone 2.
5. What does Gurobi give that a human annotator can't? What is an IIS (irreducible infeasible subsystem), and why is it useful when generating problems?

**§4 ConstraintBench**

6. Draw the generation pipeline on paper, from seed to finished task. Which steps use an LLM, and which are deterministic code?
7. Seeds vary 5 dimensions (industry, scale, urgency, region, specialization). Why vary the story at all? What could go wrong if every problem had the same story? (SCHEDBench in Part B tests exactly this.)
8. Tasks are discarded if Gurobi can't prove optimality within the time limit. Which kinds of problems survive this filter, and what bias could that create?
9. The checker recomputes the objective from the raw decisions and ignores the number the model reports. Why? (§5.6 shows what happens otherwise.)
10. Write down the exact definitions of *feasible*, *optimal* (with ε), *objective quality* and *joint % optimal*. Objective quality only counts feasible answers. How could that make a weak model look good?

### Session 2: sections 5–7 and appendices

11. In Table 3, which model is best? Does the answer change depending on the metric you pick?
12. Claude Opus 4.6 has 13 errors, mostly from running out of tokens while reasoning (§6.1). The paper counts them as infeasible. Should we do the same, report them separately, or both? Why?
13. Facility location is 85% feasible but 0% optimal. Give two possible explanations, and one experiment that could tell them apart.
14. Pick 2 of the 4 failure categories in §5.5. For each one, write a hypothesis about *why* models fail that way, and an experiment that could test it. These feed extensions A and B.
15. Appendix D: "% optimal" rises from 17.1% to 38.1% as ε goes from 0.1% to 5%. What does that mean for how we report our results?
16. Each task was run once, and each domain has 20 tasks. The 95% confidence interval for a score p measured on n tasks is roughly ±1.96 × √(p(1−p)/n). Compute it for p = 50% with n = 20, then with n = 60. Is a 5-point gap between two models in Table 3 meaningful?
17. §6.2 lists 5 future-work ideas, and 3 of them are close to our extensions. Which ones? For each, write one sentence on how our version differs. This becomes our positioning.

---

## Part B: related work (first pass only)

About 30 minutes per paper: abstract, introduction, main results table or figure, conclusion. Answer the question in the last column.

| # | Paper | Why it matters to us | Question to answer |
|---|---|---|---|
| 1 | **SCHEDBench**, Sharma & Sharma, EMNLP Findings 2026. [arXiv:2608.00991](https://arxiv.org/abs/2608.00991) | The closest follow-up to ConstraintBench: direct answers to scheduling problems, checked by a solver, 13 models. Tests whether rephrasing the same problem changes the results. No feedback loop or size-scaling study. | What do they find about rephrasing and constraint order? Does it change how we should write our scenario prompts? |
| 2 | **COMPASS**, Qin et al., 2025. [arXiv:2510.07043](https://arxiv.org/abs/2510.07043) | Finds the same gap in travel-planning agents (70–90% feasible, 20–60% optimal). Blames "insufficient exploration of the search space," and finds coding agents help. | Does "insufficient exploration" explain ConstraintBench's failures too? What does it predict for extension C? |
| 3 | **TravelPlanner**, Xie et al., ICML 2024. [arXiv:2402.01622](https://arxiv.org/abs/2402.01622) | An earlier natural-language planning benchmark with hard constraints. GPT-4-Turbo passed only 0.6% of tasks in the full setting. | How do they define and check constraints? What's the same as ConstraintBench, and what's different? |
| 4 | **LLM-Modulo**, Kambhampati et al., ICML 2024. [arXiv:2402.01817](https://arxiv.org/abs/2402.01817) | Position paper: LLMs can't plan alone, but can in a loop with external verifiers ("critics"). This is the idea behind extension A. | What is the generate-test-critique loop? What kinds of feedback do the critics give? |
| 5 | **LLMs Cannot Self-Correct Reasoning Yet**, Huang et al., ICLR 2024. [arXiv:2310.01798](https://arxiv.org/abs/2310.01798) | Without external feedback, asking a model to "check its work" doesn't help and can hurt. Some reported gains came from unfair comparisons. | What fair baseline does extension A need so that gains come from the checker's feedback and not just extra attempts? |
| 6 | **Adding Error Bars to Evals**, Miller, 2024. [arXiv:2411.00640](https://arxiv.org/abs/2411.00640) | How to compute confidence intervals, compare two models fairly (paired tests), and plan how many tasks you need. | Roughly how many problems do we need to tell apart two models whose scores differ by 10 points? |

### Later reading (not for this milestone)

- **Extension C, models that write solver code:** ORLM / IndustryOR, Tang et al. ([arXiv:2405.17743](https://arxiv.org/abs/2405.17743)); OptiMUS, AhmadiTeshnizi et al. ([arXiv:2402.10172](https://arxiv.org/abs/2402.10172)).
- **Extension D, RL with verifiable rewards:** Solver-Informed RL, Chen et al. ([arXiv:2505.11792](https://arxiv.org/abs/2505.11792)); DeepSeek-R1 ([arXiv:2501.12948](https://arxiv.org/abs/2501.12948)).
- **Name confusion:** R-ConstraintBench ([arXiv:2508.15204](https://arxiv.org/abs/2508.15204)) is a different benchmark, on project scheduling.

---

## Session 4: write the notes

Fill in [`milestone-1-notes.md`](milestone-1-notes.md). Keep it to about one page. Then ask Claude to review it with you.

Write your hypotheses **before** running any experiment. Deciding in advance what you expect and what would change your mind (sometimes called pre-registration) keeps you honest when results come in.
