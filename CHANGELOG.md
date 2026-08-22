# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-22

First stable release. Complete rewrite of Project 1 documentation and
introduction of test infrastructure, CI/CD, and code quality tooling.

### Added

**Testing infrastructure:**
- Complete pytest suite with 46 tests across 5 modules
- Session-scoped fixtures for expensive computations
- Custom markers (unit, integration, slow, edge_case, regression)
- Coverage reporting with pytest-cov (44% overall)
- Integration tests validating end-to-end pipeline
- Regression test (TC-28) protecting README benchmark claims

**CI/CD automation:**
- GitHub Actions workflow (`.github/workflows/tests.yml`)
- Matrix strategy: Python 3.11 and 3.12
- Automatic test runs on push to main and pull requests
- Pip caching for faster CI runs (~50s per Python version)
- Codecov integration for coverage tracking

**Documentation:**
- Complete README rewrite with English-first structure
- Vietnamese README sibling (`README.vi.md`)
- Problem/Solution/Impact business framing
- 3 Mermaid architecture diagrams (Data Flow, Code Structure, Optimization)
- 6 Architecture Decision Records (`docs/architecture.md`)
- Development log with sprint retrospective (`docs/development-log.md`)
- Hero GIF + 3 screenshots showcasing live app
- Status badges: Tests passing, Python 3.11+, License MIT

**Code quality tooling:**
- Black formatter configured (line-length 100)
- Ruff linter with comprehensive rule selection (E, W, F, I, B, C4, SIM, RUF)
- `pyproject.toml` centralized tool configuration
- All lint warnings resolved with documented justifications

**Notebooks reorganization:**
- Chronological naming: 01-08 (build journey), 20-21 (formal tests), 90+ (canonical outputs)
- `notebooks/README.md` documenting the naming convention

**Data artifacts:**
- Committed `data/raw/portfolio.db` (3.4MB) for CI reproducibility
- Benchmark CSV export at `reports/benchmark_results_20260821.csv`

### Changed

**Benchmarks (data cutoff 2021-01-01 to 2026-08-20):**
- Full VN30 portfolio: 25.9% volatility reduction vs equal-weighted baseline
- 5 diverse stocks: 8.5% volatility reduction
- 5 banks (high correlation): 8.8% volatility reduction
- All portfolios verified against README documented values

**Repository structure:**
- Draft prompts and reconstructed notes moved to `.claude/` folder
  (transparency about materials not authentically used in original development)
- Comprehensive `.gitignore` covering Python, Jupyter, Streamlit patterns

**Dependencies:**
- Added pytest 8.0+, pytest-cov 5.0+, pytest-mock 3.14+
- Added black 25.0+ and ruff 0.10+ for code quality

### Fixed

- `update_db()` and `min_variance_portfolio()` type hints now use explicit
  `X | None` instead of implicit Optional (PEP 484 compliance)
- Removed unused imports across `src/` modules
- Fixed f-strings without placeholders

### Removed

- Python 3.10 support dropped (pandas 3.0+ requires 3.11+)

### Documentation

- Roadmap updated to 2026-2028 timeline with clear status indicators
- Ethics principle established: "Show what you can defend"

---

## Development Sprint Overview

This release represents completion of a focused improvement sprint
addressing 7 feedback items from Project 1 review:

1. ✅ Real benchmarks (25.9% vol reduction documented)
2. ✅ Roadmap 2026-2028 with status indicators
3. ✅ Screenshots and demo GIF
4. ✅ Mermaid architecture diagrams (3 total)
5. ✅ English-first README with Vietnamese sibling
6. ✅ Problem-Solution-Impact business framing
7. ✅ Tests + CI/CD infrastructure

See `docs/development-log.md` for detailed sprint retrospective.

---

[1.0.0]: https://github.com/MCTGiang/vn-portfolio-optimizer/releases/tag/v1.0.0