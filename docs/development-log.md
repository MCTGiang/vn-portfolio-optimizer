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


---

## Sprint Closure — 2026-08-26

Official closing of the pre-Project 2 improvement sprint. This section 
documents final metrics, comprehensive learnings, and transition to Project 2.

### Sprint Timeline

- **Started:** 2026-08-04 (Monday)
- **Ended:** 2026-08-26 (Tuesday)
- **Duration:** 22 days (16 working days + 6 weekend days)
- **Total time invested:** ~35-40 hours across focused work sessions

### Final Metrics

**Testing Infrastructure:**
- Total tests: 46 (up from 0)
- Test files: 5 (data_loader, features, portfolio_metrics, optimizer, integration)
- Coverage: 44% overall (honest number, not inflated)
- Runtime: 6.3s local, ~50s in CI
- Custom markers: 5 (unit, integration, slow, edge_case, regression)

**CI/CD:**
- GitHub Actions matrix: Python 3.11, 3.12
- Auto-triggers: push to main, pull requests
- Pip caching for faster runs
- Public status badges on README

**Documentation:**
- README.md: 279 lines (English-first, cut from 328 via aggressive refactor)
- README.vi.md: 75 lines (Vietnamese sibling)
- CHANGELOG.md: 105 lines (Keep a Changelog format)
- CONTRIBUTING.md: 163 lines (contributor workflow)
- docs/ folder: 7 files (setup, architecture, roadmap, development-log, 
  deployment-testing, notebooks/README)

**Code Quality:**
- Black formatted: 11 files
- Ruff linted: 33 issues → 0 warnings
- pyproject.toml: centralized tool config
- Type hints: PEP 484 compliant

**Release & Distribution:**
- v1.0.0 tagged and released
- GitHub Release page with comprehensive notes
- 4 status badges on README (Tests, Python, License, Status)
- Profile README with career changer positioning
- Repo topics for discoverability (16 tags)
- Public status page (UptimeRobot)

**OSS Infrastructure:**
- 3 issue templates (bug, feature, docs)
- 1 PR template with comprehensive checklist
- Issue template chooser with contact links
- GitHub Discussions enabled

**Deployment Health:**
- UptimeRobot monitoring (5-min HTTP checks)
- Email alerts configured and tested
- Public status page: stats.uptimerobot.com/spxJeakm9r
- Verified cross-browser (Chrome, Edge)
- Verified mobile responsive (3 device sizes)
- Verified network resilience (3G load test)

**Git Statistics:**
- Commits: 40+ across sprint
- Pull Requests merged: 9 (#5, #6, #7, #8, #10, #11, #12)
- Direct commits to main: ~10 (small doc changes, hotfixes)
- Zero force pushes (clean history)

### Feedback Resolution Status

All 7 original feedback items from Project 1 review:

| # | Feedback Item | Status | Evidence |
|---|--------------|--------|----------|
| 1 | Real benchmarks (replace TBD) | ✅ Complete | Full VN30: 25.9% vol reduction documented |
| 2 | Roadmap 2026-2028 | ✅ Complete | Phase table with status indicators |
| 3 | Screenshots + demo GIF | ✅ Complete | Hero GIF + 3 screenshots in README |
| 4 | Architecture diagrams | ✅ Complete | 3 Mermaid diagrams (Data Flow, Code Structure, Optimization) |
| 5 | English-first README | ✅ Complete | README.md (EN) + README.vi.md sibling |
| 6 | Business framing | ✅ Complete | Problem-Solution-Impact structure |
| 7 | Tests + CI/CD | ✅ Complete | 46 tests, GitHub Actions, 44% coverage, 4 badges |

**Score: 7/7 (100%)**

### Key Debugging Journeys (worth documenting)

**1. pytest ScopeMismatch (Day 7)**
- Symptom: Session-scoped fixtures failed when depending on function-scoped
- Root cause: pytest scope rules — wider cannot depend on narrower
- Fix: Extended session scope to all read-only fixtures
- Time to fix: 20 minutes

**2. API signature assumption (Day 7)**
- Symptom: Metrics fixtures returned TypeError
- Root cause: Assumed `expected_returns(matrix)` but actual is `expected_returns(tickers, start, end)`
- Fix: Verified with `grep "^def " src/module.py` before writing tests
- Rule established: Always verify API before assuming

**3. ERROR vs FAIL distinction (Day 8)**
- Symptom: pytest showed "3 passed, 11 errors" (not "failed")
- Root cause: Missing fixtures caused test setup errors, not assertion failures
- Fix: Added 3 MVP fixtures to conftest.py
- Learning: ERROR ≠ FAIL — different debugging paths

**4. Verification discipline (Day 8)**
- Symptom: Claimed "42 tests pass" while actual output was "3 passed, 11 errors"
- Root cause: Intermediate documentation without evidence
- Fix: Always run fresh pytest before commit messages with numbers
- Meta-rule: Never trust AI claims about test results — verify yourself

**5. Python 3.10 CI failure (Day 9)**
- Symptom: CI failed at install step: "No matching distribution for pandas>=3.0.2"
- Root cause: pandas 3.0+ requires Python 3.11+
- Decision: Drop Python 3.10 rather than downgrade pandas
- Rationale: Python 3.10 EOL October 2026, modern data projects standardize on 3.11+

**6. README duplicate sections (Day 11)**
- Symptom: 2 "## Quick Start" and 2 "## Documentation" sections
- Root cause: Replace-in-place without removing old sections
- Fix: Manual review + cleanup
- Learning: Preview markdown before commit, not just after

**7. Bash command leaked into README (Day 11)**
- Symptom: `tree -L 2 -I 'venv|...'` orphan text in Quick Start
- Root cause: Terminal paste accident during earlier edit
- Fix: Manual scan + removal
- Learning: Always scan for orphan text after markdown edits

### Meta-Learnings

**On Verification:**
- Always run tests before writing commit messages with numbers
- ERROR vs FAIL distinction matters for debugging strategy
- Intermediate summaries can contain false claims — verify with fresh output
- Trust engineering evidence, not narrative

**On API Design:**
- Verify actual signatures with grep before assumptions
- Rich return types (dict with 11 documented keys) enable clean tests
- Built-in benchmark values in optimizer output made regression tests trivial
- Good API design pays dividends in test quality

**On Honesty Over Optics:**
- Coverage 44% (honest) > Coverage 60% (inflated aspiration)
- Real-time work != daily uniform pace — retrospective by phases more authentic
- Ethics-driven cleanup of .claude/ folder set the tone for the sprint
- "Show what you can defend" applied consistently

**On Sprint Discipline:**
- CI-first workflow (push → CI → fix → merge) prevents broken main
- Small binary commits acceptable when trade-off is CI reliability (portfolio.db)
- Conventional Commits format made history readable
- Semantic branch naming enabled clear intent (test/, ci/, docs/, infra/, polish/)

**On Documentation:**
- README = elevator pitch (60-second scan)
- docs/ = detail seekers
- Modern OSS convention: README <300 lines
- Separation of concerns: what vs why vs how

**On Distribution Strategy:**
- Timing matters: LinkedIn feed post "peaks too early" 10 months before job apply
- GitHub profile optimization is zero-cost, permanent, no expiration
- Save big announcements for milestones (thesis defense, first job)
- Discovery via topics + description > active promotion

**On Positioning:**
- "Career changer with 16 years domain expertise" >> "IT student"
- Domain knowledge is competitive moat for quant/fintech roles
- Ginny (nickname) bridges Vietnamese/international identity
- Second bachelor's degree signals commitment to career pivot

### What Went Well

- Consistent Conventional Commits format across all 40+ commits
- Ethical decisions early (Day 5: .claude/ folder move) set tone
- Verification discipline caught false claims before propagation
- Iterative branch-per-day workflow prevented broken main
- Documentation-first approach for OSS templates and CONTRIBUTING

### What Could Improve

- Should have written development-log.md from Day 1 (retrospective is less authentic)
- Coverage number "aspirational 60%" set false expectations initially
- Some early days took longer than estimated (~25-30% overrun typical)
- Should have verified fixtures earlier when writing test files

### Tools & Practices That Worked

- **pytest fixtures with session scope** — 6.3s for 46 tests is excellent
- **GitHub Actions matrix strategy** — cross-Python validation without complexity
- **Conventional Commits + semantic branches** — history stayed readable
- **pyproject.toml centralization** — one config file for black, ruff, project settings
- **UptimeRobot free tier** — monitoring that just works
- **Streamlit Cloud** — deployment platform that requires zero DevOps knowledge

### Transitioning to Project 2

**Ready to start (Sep 1, 2026):**
- Repository foundation replicable (Project 1 patterns established)
- Testing infrastructure template proven
- CI/CD workflow copyable
- Documentation structure defined
- Positioning locked (career changer with domain expertise)

**Key decisions pending for Project 2:**
- Prefect vs Airflow (target: Sep 15, 2026)
- PhoBERT sentiment vs RAG for information extraction (target: Nov 15, 2026)
- PostgreSQL migration approach (dump SQLite vs fresh schema)

**Learning targets for Project 2:**
- Docker containerization (via Bret Fisher's course)
- PostgreSQL beyond basic SQL
- Prefect workflow orchestration
- PhoBERT fine-tuning
- dbt data transformations

### Cumulative Portfolio State

**Public artifacts:**
- 1 production Streamlit app with live monitoring
- 1 GitHub repository (v1.0.0 released, 4 status badges)
- 8 documentation files
- 46 automated tests
- Profile with clear positioning

**Ready for:**
- Recruiter search discovery (via topic tags, profile bio)
- Contributor onboarding (via CONTRIBUTING.md + templates)
- Project 2 development (foundations established)

---

*Sprint officially closed 2026-08-26. Project 2 kickoff begins 2026-09-01.*