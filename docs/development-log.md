# Development Log

Retrospective notes on the pre-Project 2 improvement sprint (August 2026).
Organized by phases rather than dates because work happened in focused
sessions rather than uniformly across days.

## Sprint Context

Following peer review of Project 1 (initial delivery Q1 2026), 7 feedback
items were identified requiring resolution before starting Project 2:

1. Replace TBD placeholders in Results with real benchmarks
2. Fix outdated 2025 roadmap timeline
3. Add screenshots and demo GIF for visual engagement
4. Add architecture diagrams for systems thinking signal
5. Restructure README (English-first with Vietnamese version)
6. Strengthen business framing (problem-solution-impact)
7. Add tests and CI/CD infrastructure

All 7 items completed. This document captures learnings across phases.

---

## Phase 1 — Foundation & Presentation

**Scope:** Repository cleanup, README rewrite, real benchmark numbers,
architecture documentation.

**Deliverables:**
- Complete README rewrite (English-first + Vietnamese sibling)
- Problem/Solution/Impact business framing (Feedback #6)
- 3 Mermaid architecture diagrams (Feedback #4)
- Hero GIF + 3 screenshots (Feedback #3)
- Roadmap updated to 2026-2028 with status indicators (Feedback #2)
- Real benchmarks: full VN30 achieves 25.9% vol reduction (Feedback #1)
- 6 formal Architecture Decision Records (ADRs) in `docs/architecture.md`
- Comprehensive `.gitignore` covering Python/Jupyter/Streamlit patterns
- Notebooks reorganized: preserved 01-08 chronology, added 20-21 for
  formal test suites, reserved 90+ for canonical outputs
- Benchmark CSV export for external tools

**Key decision — Ethics-driven cleanup:**
Draft prompts framework and reconstructed progress notes were moved to
`.claude/` folder (hidden from main README) because they weren't
authentically used during Project 1 development due to token budget
constraints. Cannot be defended with concrete evidence, so shouldn't be
part of public portfolio narrative.

**Principle established:** "Show what you can defend."

---

## Phase 2 — Test Infrastructure

**Scope:** Migrate ad-hoc notebook tests to formal pytest suite covering
all core modules.

**Deliverables:**
- Complete pytest infrastructure (`pytest.ini`, `conftest.py`)
- 46 tests across 5 test files:
  - `test_data_loader.py`: 8 tests (DB structure, loading)
  - `test_features.py`: 9 tests (returns matrix construction)
  - `test_portfolio_metrics.py`: 11 tests (μ, Σ, Sharpe)
  - `test_optimizer.py`: 14 tests (MVP correctness, constraints)
  - `test_integration.py`: 4 end-to-end pipeline tests
- 18+ session-scoped fixtures for expensive computations
- Custom markers (unit, integration, slow, edge_case, regression)
- Coverage: 44% overall (honest number, not inflated)
  - data_loader.py: 42%
  - features.py: 51%
  - portfolio_metrics.py: 53%
  - optimizer.py: 51%
- Runtime: 6.28s local for full suite

**Debugging journey — 3 lessons worth documenting:**

**Lesson 1: pytest scope rules**
Encountered `ScopeMismatch` error when session-scoped fixtures tried to
depend on function-scoped fixtures. Fixed by upgrading all read-only
data fixtures (tickers lists, date ranges, constants) to session scope.

**Rule:** Wider scope cannot depend on narrower scope.
- session > module > class > function

**Lesson 2: API verification before writing tests**
Wrote metrics tests assuming `expected_returns(returns_matrix)` signature,
but actual API is `expected_returns(tickers, start, end)`. Similar issue
with `cov_matrix` vs `covariance_matrix` function naming.

**Fix:** Always verify actual API before writing tests:
```bash
grep "^def " src/module.py
```

**Lesson 3: ERROR vs FAIL distinction**
Initial `test_optimizer.py` run showed "3 passed, 11 errors" - not
"3 passed, 11 failed". Key distinction:
- **FAIL**: Test runs, assertion fails
- **ERROR**: Test cannot run (fixture setup fails, import error)

11 errors were caused by missing MVP fixtures in `conftest.py`. Adding
3 fixtures fixed all 11 errors.

**Bonus lesson: Verification discipline**
During debugging, noticed intermediate outputs claimed "42 tests pass"
while actual output was "3 passed, 11 errors". Stopped and demanded
evidence before proceeding.

**Rule:** Never commit with test claims unless verified with fresh
pytest output. Numbers in commit messages must match reality.

---

## Phase 3 — CI/CD Automation

**Scope:** Automate test execution via GitHub Actions, add credibility
signals to README.

**Deliverables:**
- `.github/workflows/tests.yml` — matrix strategy (Python 3.11, 3.12)
- Pip caching for faster CI runs (~50s per Python version)
- CI triggers on push to main + pull requests
- 3 status badges on README: Tests passing, Python 3.11+, License MIT
- Committed `data/raw/portfolio.db` (3.4MB) for CI reproducibility

**Debugging journey:**

**Issue 1: Python 3.10 incompatibility**
Initial CI matrix included Python 3.10. Failed at install step:
`No matching distribution found for pandas>=3.0.2`

Root cause: pandas 3.0+ requires Python 3.11+.

**Decision:** Drop Python 3.10 rather than downgrade pandas.
- Python 3.10 EOL: October 2026 (5 months away)
- Modern data projects standardize on 3.11+
- 2 Python versions still provides cross-version validation

**Issue 2: Data strategy for CI**
Tests need real DB data (46 tests). Two options considered:
- Fetch data via API in CI (5-10 min, rate limit risk)
- Commit DB file to git (3.4MB binary)

**Chose to commit DB file:**
- Fast CI (~1 minute)
- No API dependencies
- Reproducible for new contributors
- Trade-off: binary in git acceptable at 3.4MB

Updated `.gitignore` with `!data/raw/portfolio.db` exception.

---

## Key Meta-Learnings

**On verification:**
- Always run tests before writing commit messages with numbers
- ERROR vs FAIL distinction matters for debugging
- Don't trust intermediate summaries — verify with fresh output

**On API design:**
- Verify actual signatures with `grep def` before assumptions
- Rich return types (dict with 11 keys) enable clean tests
- Built-in benchmark values (`equal_weights_vol`, `improvement_pct`)
  in optimizer output made regression tests trivial

**On honesty over optics:**
- Coverage 44% (honest) > Coverage 60% (inflated aspiration)
- Real-time work != daily uniform pace — sprint notes retrospective
  by phases more authentic than fake daily entries
- Ethics-driven cleanup of `.claude/` folder set the tone for the sprint

**On sprint discipline:**
- CI-first workflow (push → CI → fix → merge) prevents broken main
- Small binary commits acceptable when trade-off is CI reliability
- Conventional Commits format across all commits made history readable

---

## Cumulative Stats

- **Test files:** 5 (data_loader, features, portfolio_metrics, optimizer, integration)
- **Total tests:** 46 (all passing)
- **Coverage:** 44% overall
- **CI runtime:** ~50s per Python version
- **Local test runtime:** 6.28s
- **PRs merged:** 4 (#5 data_loader, #6 features+metrics, #7 optimizer+integration, #8 CI)
- **Python versions supported:** 3.11, 3.12
- **README badges:** 3 (Tests, Python, License)

**All 7 feedback items resolved.**

---

## Next Steps

**Immediate (Day 10):**
- Code formatting with black
- Linting with ruff, fix warnings
- CHANGELOG.md
- Tag v1.0.0

**Short-term (Days 11-15):**
- README final polish + link validation
- Social share (LinkedIn, Facebook, Reddit)
- GitHub Projects board + issue templates
- UptimeRobot monitoring
- Sprint retrospective + Project 2 kickoff

**Project 2 (September 2026):**
- Add efficient frontier extension
- Sentiment analysis integration
- Auto-rebalancing signals
- Repository: `vn-portfolio-frontier`