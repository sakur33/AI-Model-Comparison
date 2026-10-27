# GLMComparison

Compare **Claude Sonnet 5.6** against **GLM 5.3 (served by the CompactifAI API)** on a set of
LeetCode-style Python problems, then compute **cost per task** from the real token usage of each run.

- 21 problems (5 easy, 10 medium, 6 hard), original statements of classic interview problems.
- Each problem has hand-written edge cases plus seeded, larger generated cases (these catch
  O(n²) solutions via a per-case time limit). Expected outputs of generated cases come from a
  reference solution; the hand-written cases validate those references (`glmcompare validate`).
- Candidate code runs in a separate Python process with per-case timeouts, so crashes, infinite
  loops and stray `print`s cannot break the harness.
- Token usage is stored per attempt, so you can change prices and rebuild the report without re-querying.

## Setup

```bash
cd GLMComparison
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in the keys
```

Then edit `config/models.yaml`:

1. Confirm the **model ids** (`claude-sonnet-5-6` and `glm-5.3` are placeholders).
2. Fill in **prices** (USD per 1M tokens) for both models. Anthropic's come from its pricing page,
   CompactifAI's from your account. Left as `null`, costs show `n/a`.
3. CompactifAI is called through an OpenAI-compatible chat-completions client. Set
   `COMPACTIFAI_BASE_URL` and `COMPACTIFAI_API_KEY` in `.env`.

## Usage

```bash
glmcompare list                                   # problems and number of test cases
glmcompare validate                               # reference solutions must be 100% green
glmcompare run --models sonnet glm --samples 1    # query both models, evaluate, write report
glmcompare run --models sonnet glm --samples 5 --run-id big   # pass@1 statistics; reuse id to resume
glmcompare run --models glm --difficulty hard --problems edit_distance trap
glmcompare report --run-id latest --price glm=0.6,2.2   # what-if pricing, no API calls
pytest                                            # harness tests (no API keys needed)
```

Try the pipeline offline first: `glmcompare run --models mock`.

Results land in `results/<run-id>/`: one JSON per attempt (response, extracted code, tokens, latency,
failing cases), plus `report.md` and `per_task.csv`.

## Metrics

- **Pass rate**: attempt passes only if all test cases pass.
- **Cost / task** = total cost / attempts. **Cost / solved task** = total cost / passed attempts
  (the number that matters when comparing a cheaper but less accurate model).
- Cost = `input_tokens * in_price + cache_read * cache_price + output_tokens * out_price`.
  Reasoning tokens count as output tokens for both providers.

## Fairness notes

- Both models get the identical system and user prompt; only `params` in `models.yaml` differ.
  Newer Claude models may reject `temperature`, so it is only sent if you set it.
- `max_tokens` (default 8192) caps output; a truncated answer fails, and thinking models may need more.
- Use `--samples >= 3` for any conclusion; single attempts are noisy.
- The sandbox is process-level isolation only. Model code runs on your machine, so run it in a
  container or VM if that matters.

## Adding a problem

Create `src/glmcompare/problems/<id>.py` exposing `PROBLEM = Problem(...)` (see `two_sum.py`). The
reference function must be self-contained (imports inside) and named like `entry_point`. Use
`checker=` when several outputs are valid. Run `glmcompare validate`.
