# GLM 5.3 vs Claude Sonnet 5.5: coding benchmark comparison

21 LeetCode-style Python problems (5 easy, 10 medium, 6 hard), 3 independent samples each, 63 attempts per model. One shot per attempt, no feedback loop. An attempt passes only if every test case passes.

- **GLM 5.3** via the CompactifAI API (`glm-5-3`), `temperature: 0`, `max_tokens: 32768`, streamed. Run `20261026-163615`. GLM was tested on a public API with no speed SLA, so its latency figures reflect shared, best-effort capacity and not a guaranteed or dedicated deployment.
- **Claude Sonnet 5.5** (`claude-sonnet-5-5`), `max_tokens: 8192`. Run `20261026-155738`.
- Same system and user prompt for both. Prices are the verified values in `config/models.yaml` (GLM $0.20 in / $0.64 out / $0.018 cached per 1M tokens, Sonnet $2 / $10 / $0.10).

> **Method note.** Pass rates count all 63 attempts, including the failed ones. Token, latency and cost figures **exclude the `edit_distance` problem for both models** (60 attempts each), because it is the one problem GLM failed and its token use is an extreme outlier (24k to 32.8k tokens per attempt). The full-set cost is shown separately in the last summary row so the exclusion can be audited.

## Summary

| | GLM 5.3 | Sonnet 5.5 |
|---|---|---|
| Solved (all 63) | 61/63 (96.8%) | 63/63 (100.0%) |
| easy | 15/15 | 15/15 |
| medium | 30/30 | 30/30 |
| hard | 16/18 | 18/18 |
| Total cost (60 attempts, excl. `edit_distance`) | $0.0561 | $0.2419 |
| Cost / task | $0.00093 | $0.00403 |
| Cost / solved task | $0.00093 | $0.00403 |
| Cost ratio (GLM / Sonnet) | 0.23x | |
| *Audit: total cost, all 63 attempts* | *$0.1138* | *$0.2748* |

GLM misses 2 of 63 attempts, both on `edit_distance`. Sonnet solved all 63. On the 60 attempts outside `edit_distance`, GLM costs about 0.23x as much as Sonnet. The averages hide a wide spread in GLM's behaviour, shown below.

## Variance across the 60 attempts (excluding `edit_distance`)

| Metric | Model | Mean | Median | p90 | Max | Std dev |
|---|---|---|---|---|---|---|
| Output tokens | GLM | 1394 | 746 | 3132 | 8762 | 1748 |
| Output tokens | Sonnet | 350 | 304 | 586 | 893 | 172 |
| Latency (s) | GLM | 43.4 | 22.0 | 76.4 | 370.1 | 62.2 |
| Latency (s) | Sonnet | 3.1 | 2.8 | 4.8 | 6.9 | 1.1 |
| Cost / attempt ($) | GLM | 0.00093 | 0.00053 | 0.00205 | 0.00564 | 0.00112 |
| Cost / attempt ($) | Sonnet | 0.00403 | 0.00353 | 0.00642 | 0.00948 | 0.00173 |

Even without `edit_distance`, GLM's mean output (1394 tokens) is well above its median (746): a few attempts run long and pull the mean up. Sonnet's tokens are tight (std dev 172, max 893). GLM's latency ranges from under 5s to 370s, Sonnet's from 1.5s to 6.9s.

## Per problem

Output tokens and latency are shown as mean (min–max) over the 3 samples. Cost is the sum of the 3 samples. `edit_distance` is listed for pass rate and for reference but is excluded from every aggregate above.

| Problem | Diff | GLM pass | GLM out tokens | GLM latency (s) | GLM cost | Sonnet pass | Sonnet out tokens | Sonnet latency (s) | Sonnet cost | GLM/Sonnet cost |
|---|---|---|---|---|---|---|---|---|---|---|
| `best_time_to_buy_sell_stock` | easy | 3/3 | 391 (312–496) | 16.4 (11.7–25.3) | $0.0009 | 3/3 | 126 (118–132) | 2.5 (2.0–3.5) | $0.0052 | 0.17x |
| `longest_common_prefix` | easy | 3/3 | 1187 (279–1839) | 100.0 (12.4–215.7) | $0.0024 | 3/3 | 223 (197–237) | 2.2 (2.2–2.3) | $0.0080 | 0.30x |
| `merge_sorted_arrays` | easy | 3/3 | 325 (241–375) | 16.0 (13.1–20.0) | $0.0007 | 3/3 | 174 (168–177) | 1.5 (1.5–1.6) | $0.0068 | 0.11x |
| `two_sum` | easy | 3/3 | 136 (125–153) | 6.8 (5.6–8.4) | $0.0004 | 3/3 | 207 (167–236) | 2.4 (2.1–2.7) | $0.0078 | 0.05x |
| `valid_parentheses` | easy | 3/3 | 293 (236–404) | 8.1 (6.5–9.5) | $0.0007 | 3/3 | 179 (144–196) | 2.3 (1.7–3.0) | $0.0068 | 0.10x |
| `coin_change` | medium | 3/3 | 1049 (727–1452) | 27.9 (20.7–40.9) | $0.0021 | 3/3 | 370 (347–400) | 2.9 (2.8–3.1) | $0.0126 | 0.17x |
| `course_schedule` | medium | 3/3 | 862 (670–1194) | 38.7 (22.0–53.6) | $0.0018 | 3/3 | 466 (384–513) | 3.9 (3.4–4.3) | $0.0159 | 0.11x |
| `group_anagrams` | medium | 3/3 | 712 (261–1076) | 84.6 (10.7–203.3) | $0.0015 | 3/3 | 263 (236–284) | 2.6 (2.4–2.9) | $0.0094 | 0.16x |
| `longest_substring_no_repeat` | medium | 3/3 | 1053 (800–1235) | 35.8 (13.8–72.9) | $0.0021 | 3/3 | 220 (203–249) | 2.1 (2.0–2.2) | $0.0080 | 0.27x |
| `lru_cache` | medium | 3/3 | 667 (595–775) | 25.0 (12.3–43.7) | $0.0014 | 3/3 | 260 (252–271) | 2.6 (2.4–2.9) | $0.0099 | 0.14x |
| `merge_intervals` | medium | 3/3 | 598 (521–693) | 17.5 (9.8–22.5) | $0.0013 | 3/3 | 290 (268–314) | 2.7 (2.4–2.9) | $0.0103 | 0.12x |
| `number_of_islands` | medium | 3/3 | 656 (574–703) | 28.1 (4.0–42.9) | $0.0014 | 3/3 | 534 (463–635) | 3.7 (3.2–4.5) | $0.0176 | 0.08x |
| `product_except_self` | medium | 3/3 | 933 (529–1410) | 28.0 (15.4–36.2) | $0.0019 | 3/3 | 318 (250–393) | 3.1 (2.3–4.1) | $0.0110 | 0.17x |
| `three_sum` | medium | 3/3 | 751 (746–761) | 13.7 (4.4–25.8) | $0.0016 | 3/3 | 417 (389–469) | 3.1 (2.8–3.7) | $0.0142 | 0.11x |
| `word_break` | medium | 3/3 | 5931 (831–8762) | 237.5 (168.6–370.1) | $0.0115 | 3/3 | 624 (518–780) | 4.6 (4.0–5.5) | $0.0202 | 0.57x |
| `edit_distance` *(excluded from aggregates)* | hard | 1/3 | 29965 (24359–32768) | 150.9 (130.9–186.7) | $0.0577 | 3/3 | 1049 (979–1135) | 7.7 (7.2–8.5) | $0.0329 | 1.76x |
| `median_two_sorted` | hard | 3/3 | 3037 (2807–3172) | 38.5 (24.7–54.2) | $0.0060 | 3/3 | 605 (584–644) | 4.8 (4.8–4.8) | $0.0198 | 0.30x |
| `min_window_substring` | hard | 3/3 | 3225 (2886–3641) | 55.0 (30.8–90.5) | $0.0063 | 3/3 | 751 (660–893) | 5.8 (5.1–6.9) | $0.0242 | 0.26x |
| `n_queens` | hard | 3/3 | 3510 (621–6894) | 44.3 (7.2–76.4) | $0.0069 | 3/3 | 333 (298–361) | 3.4 (2.7–3.8) | $0.0115 | 0.60x |
| `sliding_window_maximum` | hard | 3/3 | 636 (468–937) | 12.8 (8.5–21.3) | $0.0013 | 3/3 | 270 (220–342) | 2.3 (2.0–2.6) | $0.0099 | 0.14x |
| `trapping_rain_water` | hard | 3/3 | 1929 (1771–2034) | 33.4 (18.0–59.7) | $0.0038 | 3/3 | 376 (309–420) | 3.1 (2.6–3.4) | $0.0127 | 0.30x |

## Where GLM's variance comes from

- **Sample-to-sample spread on the same problem.** `longest_common_prefix` (an easy problem) took 279 to 1839 tokens and 12s to 216s across its 3 samples. `group_anagrams` took 261 to 1076 tokens and 11s to 203s. `n_queens` took 621 to 6894 tokens. Sonnet's spread on the same problems is a few tens of tokens.
- **Long reasoning tails.** `word_break` (medium) used 831 to 8762 tokens and 169s to 370s per attempt, about 10x Sonnet's tokens. These attempts passed, but only because `max_tokens` is 32768. At 8192, all 3 were truncated in the earlier run.
- **`edit_distance` is the one real failure.** GLM used 24k to 32.8k tokens per attempt. Two of three samples hit the 32768 cap (`stop_reason: length`) and failed. One finished at 24,359 tokens and passed. Sonnet solved it in about 1,050 tokens. Its numbers are left out of the aggregates by design, so the cost ratio above flatters GLM: on this problem alone GLM cost about $0.058 vs $0.033 for Sonnet over 3 samples.
- **Hard problems are not uniformly harder for GLM.** `sliding_window_maximum` took 636 tokens on average, while `median_two_sorted` and `min_window_substring` took about 3,000.

## How the GLM numbers changed across runs

| GLM run | Config | Solved | Notes |
|---|---|---|---|
| `20261026-150756` | `max_tokens: 8192` | 56/63 (88.9%) | All 7 failures truncated (`stop_reason: length`): `edit_distance` 3/3, `word_break` 3/3, `longest_common_prefix` 1/3. |
| `20261026-163615` (first pass) | `max_tokens: 32768` | 60/63 (95.2%) | Truncation fixed for `word_break` and `longest_common_prefix`. `edit_distance` returned `503 request_deadline_exceeded` 3 times: CompactifAI's request budget expired before the model produced any output. |
| `20261026-163615` (after streaming) | `max_tokens: 32768`, streamed | 61/63 (96.8%) | Streaming removed the 503s. `edit_distance` now returns: 1 pass, 2 truncated at 32768 tokens. |

The reported GLM result (61/63) is the last row. The Sonnet run was not repeated.

## Caveats

- Excluding `edit_distance` lowers GLM's cost and token figures. Read the cost ratio as "on problems GLM can finish", not as a full-set cost. The audit row in the summary gives the full-set total.
- 3 samples per problem is a small sample. Sonnet's 100% has a wide confidence interval, and the per-problem GLM spread above is only 3 draws.
- A replacement problem, `regex_matching`, was tried and dropped. GLM failed it 3/3 (all attempts hit the 32768-token cap with no answer written) and Sonnet passed 3/3. It is not part of these results and is kept disabled in `src/glmcompare/problems/_regex_matching.py`. That result suggests the long-reasoning failure is not specific to `edit_distance`.
- The two models run with different `max_tokens` (32768 vs 8192). Sonnet's longest answer was 1,135 tokens, so its cap never mattered.
- GLM's output token count is the provider's `completion_tokens`, assumed to include reasoning tokens. Input token counts differ between the two tokenizers, so input costs are not exactly like-for-like.
- GLM was tested on a public API with no speed SLA. Its latency (median 22s, max 370s) and the `503 request_deadline_exceeded` errors seen earlier come from that shared, best-effort service and may not represent what a dedicated or on-prem deployment would deliver. Latency also includes the provider's queueing and streaming time and depends on load at the time of the run. Compare the two models' latency with that in mind.
- Costs use the verified prices above. `glmcompare report --run-id comparison --price glm=IN,OUT --price sonnet=IN,OUT` recomputes the standard report (which includes all problems).

Raw data: `results/comparison/` (`report.md`, `per_task.csv`, and one JSON per attempt under `glm/` and `sonnet/`).
