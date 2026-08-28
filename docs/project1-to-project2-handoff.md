# Project 1 to Project 2 Handoff

Context transfer document from Project 1 (VN Portfolio Optimizer) to Project 2 
(VN Portfolio Frontier). Upload this to Project HUST knowledge for continuity 
across chat sessions.

**Handoff date:** 2026-08-26  
**Project 1 status:** COMPLETE (v1.0.0 released)  
**Project 2 kickoff:** 2026-09-01

---

## About the User (Ginny)

**Identity:**
- Name: Mai Công Trà Giang (Ginny)
- Location: Vietnam

**Background — Career Changer:**
- 16 years in Vietnamese securities industry (2010-present)
- International Business degree @ Foreign Trade University (FTU, 2005-2010)
- Currently pursuing IT Engineering @ Hanoi University of Science and 
  Technology (HUST, 2025-2027) as second bachelor's degree
- Goal: "Data Leader positioning by mid-2027"

**Why career change:**
- Deep finance domain expertise + adding technical capability
- Bridge between traders (know markets, not code) and quant engineers 
  (know code, not markets)
- Target roles: quantitative finance, Vietnamese fintech, data engineering

**Certifications:**
- IBM Data Engineering Professional Certificate (Coursera, Oct 2024) — 
  16-course specialization.

**Hardware:**
- Current: HP Envy 13, 8GB RAM (constraint for Project 2)
- Upgrade decision deferred to Project 3 boundary (Dec 2026)
---

## Project 1 Summary

**Repository:** github.com/MCTGiang/vn-portfolio-optimizer  
**Live demo:** mctgiangproject1.streamlit.app  
**Version:** v1.0.0 (released 2026-08-15)  
**Status page:** stats.uptimerobot.com/spxJeakm9r

**What it does:**
Portfolio optimizer for Vietnamese VN30 stocks using Modern Portfolio Theory. 
Interactive Streamlit dashboard with bilingual UI (English/Vietnamese).

**Headline benchmark:**
- Full VN30 (29 tickers): **25.9% volatility reduction** vs equal-weighted 
  baseline over 5.6-year data window (2021-01-01 to 2026-08-20)
- MVP vol: 15.62%, EW vol: 21.08%

**Technical foundation:**
- Python 3.11+ (Python 3.10 dropped due to pandas 3.0+ requirement)
- scipy (SLSQP solver), pandas, numpy
- Streamlit + Plotly for UI
- SQLite for storage (3.4MB DB committed for CI reproducibility)
- vnstock (primary) + yfinance (fallback) data sources
- pytest (46 tests, 44% coverage)
- GitHub Actions CI (matrix: Python 3.11, 3.12)
- black + ruff for code quality

**Repository structure:**
vn-portfolio-optimizer/
├── .github/
│ ├── ISSUE_TEMPLATE/ (bug, feature, docs + config.yml)
│ ├── PULL_REQUEST_TEMPLATE.md
│ └── workflows/tests.yml
├── .claude/ (draft prompts + notes, transparency: not authentically used)
├── app/ (Streamlit app)
├── data/raw/portfolio.db (committed for CI)
├── docs/
│ ├── architecture.md (6 ADRs)
│ ├── development-log.md (sprint retrospective)
│ ├── deployment-testing.md
│ ├── roadmap.md (4-phase overview)
│ └── setup.md (installation guide)
├── notebooks/ (chronological 01-08 + tests 20-21 + canonical 90+)
├── reports/benchmark_results_20260821.csv
├── src/ (data_loader, features, portfolio_metrics, optimizer, update_db)
├── tests/ (46 tests across 5 files + conftest.py fixtures)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md (279 lines, English-first)
├── README.vi.md (75 lines, Vietnamese)
├── pyproject.toml (black + ruff config)
└── requirements.txt


**Feedback resolution: 7/7 items complete**

---

## Project 2 Scope

**Repository name:** `vn-portfolio-frontier`  
**Vietnamese:** Mở rộng Đường biên Hiệu quả và Tích hợp Phân tích Cảm xúc Thị trường  
**English:** Efficient Frontier Extension with Auto-Rebalancing and Market 
Sentiment Signals for Vietnamese Equity Portfolios  
**Timeline:** September - November 2026 (~3 months, ~10-11 hrs/week)

**Core features to build:**
1. **Efficient Frontier visualization** — Select portfolios across full 
   risk-return curve (multiple risk levels, not just MVP)
2. **Auto-rebalancing signals** — Periodic rebalancing with transaction costs 
   and turnover constraints
3. **NLP sentiment analysis** from Vietnamese financial news:
   - Sources: VnExpress, CafeF, VietStock
   - Model: PhoBERT (Vietnamese BERT) fine-tuned on financial text
   - Value proposition: STRUCTURED INFORMATION EXTRACTION 
     (ticker, event type, sentiment, magnitude, entities)
   - NOT "sentiment predicts returns" — that's weak positioning
   - Data labeling: ~5,000 Claude/GPT-4-labeled samples + ~200 human eval

**Technical stack (LOCKED as of 2026-08-26):**
- **Database: Neon Cloud PostgreSQL** (free tier initially)
  - Rationale: 8GB RAM constraint + zero infrastructure friction
  - Region: Singapore (closest to Vietnam)
  - Migration path: Neon → AWS RDS for Thesis (both PostgreSQL)
- Docker for application containerization (Streamlit, Prefect - not DB)
- Prefect for workflow orchestration (decision deadline: Sep 15, 2026)
- dbt for data transformations
- pytest + GitHub Actions (already established from Project 1)
- Streamlit frontend (Metabase as stretch goal)

**Critical requirement:**
At least ONE second heterogeneous data source (fundamentals or macro data) 
to justify "platform architecture" claims. Cannot use only VN30 prices.

**Key decisions pending:**

| Decision | Deadline | Options |
|----------|----------|---------|
| Prefect vs Airflow | Sep 15, 2026 | Recommended: Prefect |
| PhoBERT sentiment vs RAG | Nov 15, 2026 | Depends on data labeling quality |

**Decisions LOCKED (2026-08-26):**
- ✅ Database: Neon Cloud PostgreSQL
- ✅ Hardware: Continue HP Envy 13, upgrade decision deferred to Project 3
- ✅ Path: Hybrid cloud → local (evolve based on needs)

---

## Sprint Learnings from Project 1

### Debugging Journeys (7 lessons worth remembering)

**1. pytest ScopeMismatch:**
Session-scoped fixtures CANNOT depend on function-scoped fixtures. Wider 
scope cannot depend on narrower scope. Rule: all read-only fixtures 
(tickers, dates, constants) → scope="session".

**2. API verification before writing tests:**
Never assume API signatures. Always `grep "^def " src/module.py` first. 
Example: assumed `expected_returns(matrix)` but actual is 
`expected_returns(tickers, start, end)`.

**3. ERROR vs FAIL distinction in pytest:**
- ERROR = test cannot run (fixture setup fails, import error)
- FAIL = test runs, assertion fails
Different debugging paths. Missing fixtures = ERROR.

**4. Verification discipline:**
Never write commit messages with test numbers unless verified with fresh 
`pytest -v` output. Intermediate summaries can contain false claims.

**5. Python 3.10 pandas compatibility:**
pandas 3.0+ requires Python 3.11+. Decision: drop Python 3.10 rather than 
downgrade pandas. Modern data projects standardize on 3.11+.

**6. README duplicate sections:**
Replace-in-place without removing old sections creates duplicates. 
Always preview markdown before commit, not just after.

**7. Bash command leaked into README:**
Terminal paste accidents leave orphan text. Always scan for bash-like 
content after markdown edits.

### Meta-Learnings

**Honesty over optics:**
- "Show what you can defend" — consistent principle applied
- Coverage 44% (honest) > Coverage 60% (inflated)
- Ethics-driven cleanup: draft prompts moved to `.claude/` (transparency: 
  not authentically used during Project 1 development)
- Ginny's initial time estimates typically 25-30% low — plan accordingly

**Sprint discipline:**
- CI-first workflow (push → CI → fix → merge) prevents broken main
- Semantic branch naming: test/, ci/, docs/, infra/, polish/
- Conventional Commits format across all commits
- Small binary commits acceptable when trade-off is CI reliability

**Documentation strategy:**
- README = elevator pitch (60-second scan, target <300 lines)
- docs/ = detail seekers
- Modern OSS convention (React, Next.js follow this)
- Retrospective by phases > fake daily entries

---

## Working Style Preferences

**Language:**
- Vietnamese for casual discussion, planning, questions
- English for code, technical documentation, commit messages
- Mixed OK: "test đã pass" or "commit này done rồi"

**Commit messages:**
- Conventional Commits format: `type: description`
- Types used: feat, fix, docs, chore, test, refactor, ci, infra, polish
- Multi-line commits with detailed body sections
- Include verification evidence (test counts, coverage) when applicable

**Branch naming:**
- Semantic prefixes: `feat/`, `fix/`, `docs/`, `test/`, `refactor/`, 
  `chore/`, `ci/`, `infra/`, `polish/`
- Descriptive slug: `test/pytest-setup-data-loader`, NOT `test/day6`
- Delete branches after merge

**PR workflow:**
- Feature branch → push → PR → merge → cleanup
- Small doc-only changes: direct commit to main acceptable
- Non-trivial changes: always PR + CI verification
- PR descriptions with structured format (Motivation, Changes, Results)

**File organization:**
- Docs in `docs/` folder
- Config in `pyproject.toml` (centralized)
- `.github/` for OSS templates
- Notebook chronological naming (01-08 for build journey, 20-29 for tests, 
  90+ for canonical output)

---

## Special Instructions for Claude (New Chat)

**Critical rules:**

**1. Always verify with evidence, never claim numbers without source:**
- Never write commit messages with "X tests pass" unless verified with 
  fresh pytest output
- Never guess coverage percentages — use actual `--cov` output
- If intermediate discussion mentions numbers, verify before writing to git
- User has caught false claims before — this is a known failure mode

**2. Step-by-step incremental teaching style:**
- Wait for user's output before giving next step
- Give 1-2 commands at a time, not entire scripts
- Ask user to confirm/paste output before continuing
- Don't push forward if user has questions or seems uncertain
- Example: "Chạy X và gửi tôi output" then wait, không "Chạy X, Y, Z rồi commit"

**3. Honest scope over inflated promises:**
- If coverage will be 40% not 60%, say so upfront
- If task takes 4h not 2h, calibrate estimate
- If uncertain, express uncertainty explicitly
- Don't over-promise features to seem helpful

**4. Follow Project 1 conventions unless user requests change:**
- Conventional Commits
- Semantic branches
- pytest markers (unit, integration, slow, edge_case, regression)
- black + ruff configuration
- pyproject.toml centralization

**5. Language matching:**
- Match user's language in their message (Vietnamese → respond Vietnamese)
- Use English for code, commands, technical terms
- Bullet points and structure OK in Vietnamese responses

**6. Verification discipline reminders:**
- Before commit with metrics: "Chạy pytest -v và gửi output"
- Before claiming CI status: "Check Actions tab và screenshot"
- Before assuming API: "grep def src/module.py first"

---

## Project 2 Kickoff Plan

**Week 1 (Sep 1-7): Repository foundation + Neon setup**
- Register Neon Cloud account (region: Singapore)
- Create `vn-portfolio-frontier` repo on GitHub
- Copy Project 1 patterns: .github/, docs/ structure, pyproject.toml
- Initial README (English-first) + README.vi.md
- Initial ADRs for Project 2 decisions
- pytest infrastructure + first tests
- Register Bret Fisher's Docker Mastery course

**Week 2 (Sep 8-14): Neon PostgreSQL schema design**
- Design schema for VN30 prices (migrate from SQLite)
- Design schema for fundamentals data (new)
- Design schema for news/sentiment data (new)
- DBeaver GUI setup for local access
- Python connection via psycopg2-binary
- **Decision deadline: Prefect vs Airflow (Sep 15)**

**Week 3-4 (Sep 15-30): Prefect workflow orchestration**
- Prefect flows for data pipeline
- Scheduled updates (daily/weekly)
- Error handling and retry logic
- Deploy Prefect in Docker container

**Week 5-6 (Oct 1-15): dbt data transformations**
- dbt models for feature engineering
- Materialization strategies
- Testing dbt models
- Integration with Neon

**Week 7-9 (Oct 15 - Nov 8): Efficient frontier + rebalancing**
- Extend optimizer for efficient frontier
- Multiple portfolios along curve
- Rebalancing simulation with transaction costs
- Streamlit UI updates

**Week 10-12 (Nov 8-30): PhoBERT sentiment analysis**
- **Decision deadline: PhoBERT vs RAG (Nov 15)**
- Data collection: VnExpress, CafeF, VietStock scraping
- LLM distillation for labeling (~5,000 samples)
- Human eval samples (~200)
- Fine-tuning: Local (CPU) OR Colab Pro GPU
- Integration with existing pipeline

**Bret Fisher Docker Mastery course:** Register in Week 1, complete alongside 
implementation (~2-3 hrs/week study)

---
