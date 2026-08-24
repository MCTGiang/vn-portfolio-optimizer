# Contributing to VN Portfolio Optimizer

Thank you for your interest in contributing! This project is part of a 4-phase 
research initiative on quantitative investment for Vietnamese equities. See 
[ROADMAP](./docs/roadmap.md) for context.

## Ways to Contribute

- 🐛 **Report bugs** — Use [Bug Report template](../../issues/new?template=bug_report.md)
- ✨ **Suggest features** — Use [Feature Request template](../../issues/new?template=feature_request.md)
- 📚 **Improve docs** — Use [Documentation template](../../issues/new?template=documentation.md)
- 💻 **Submit pull requests** — See workflow below
- 💬 **Join discussions** — [GitHub Discussions](../../discussions)

## Before You Start

**For non-trivial changes**, please open an issue first to discuss:
- What problem you're solving
- Your proposed approach
- Whether it aligns with the [roadmap](./docs/roadmap.md)

This avoids wasted effort on PRs that don't fit the project direction.

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/vn-portfolio-optimizer.git
cd vn-portfolio-optimizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# 3. Install dependencies (includes dev tools)
pip install -r requirements.txt

# 4. Verify setup
pytest -v          # Should show 46/46 tests pass
ruff check src/    # Should show "All checks passed!"
```

For detailed setup, see [docs/setup.md](./docs/setup.md).

## Development Workflow

### 1. Create a branch

Use semantic prefixes:

- `feat/description` — New features
- `fix/description` — Bug fixes
- `docs/description` — Documentation only
- `test/description` — Test additions
- `refactor/description` — Code restructuring
- `chore/description` — Maintenance tasks
- `ci/description` — CI/CD changes
- `infra/description` — Infrastructure

```bash
git checkout -b feat/efficient-frontier-viz
```

### 2. Make your changes

**Code style:**
- Format with `black src/ tests/`
- Lint with `ruff check src/ tests/`
- Both are enforced by CI

**Testing:**
- Add tests for new functionality
- Aim to maintain or improve coverage
- Run full suite: `pytest -v`
- Run only fast tests: `pytest -m "not slow" -v`

**Commit messages:**

Follow [Conventional Commits](https://www.conventionalcommits.org/):


Examples:
- `feat: add efficient frontier visualization`
- `fix: correct Sharpe ratio calculation for edge case`
- `docs: update setup guide with Windows PowerShell steps`
- `test: add regression tests for MVP with 3 assets`

### 3. Submit a pull request

- Push your branch: `git push origin feat/your-feature`
- Open PR against `main` branch
- Fill out the PR template completely
- Wait for CI to pass (Python 3.11 + 3.12)
- Address review feedback

**PR requirements:**
- All CI checks pass ✅
- Tests added for new functionality
- Documentation updated (if user-facing)
- Follows code style (black + ruff)
- Meaningful commit messages

## Code Guidelines

### Python Style

- Line length: **100 characters** (configured in `pyproject.toml`)
- Type hints: **Use them** for new function signatures
- Docstrings: Follow Google style
- Prefer explicit over implicit

### Testing Philosophy

- **Unit tests**: Fast, isolated, test one thing
- **Integration tests**: Test full pipeline (marked `@pytest.mark.integration`)
- **Regression tests**: Protect documented benchmarks (marked `@pytest.mark.regression`)
- **Edge case tests**: Boundary conditions (marked `@pytest.mark.edge_case`)

Available markers: `unit`, `integration`, `slow`, `edge_case`, `regression`

### Financial Correctness

This project handles financial calculations. **Correctness matters more than performance.**

- Numerical precision: Use appropriate tolerances (e.g., `1e-6` for float comparisons)
- Edge cases: Test with realistic financial scenarios (high correlation, extreme returns)
- Validation: New optimization methods should have regression tests against known results

## Roadmap Alignment

**Current focus (Project 1):** Bug fixes, documentation improvements, test coverage.

**Coming soon (Project 2, Q4 2026):** Efficient frontier, sentiment analysis, auto-rebalancing.

Features aligned with future phases are welcome but may be deferred. See [docs/roadmap.md](./docs/roadmap.md) for planning details.

## What NOT to Contribute

To keep scope manageable:

- ❌ **Trading execution logic** — Reserved for thesis phase (2027)
- ❌ **Real-time data streaming** — Reserved for thesis phase
- ❌ **Multi-user authentication** — Out of scope for research project
- ❌ **Complex UI redesigns** — Streamlit provides sufficient functionality
- ❌ **Cryptocurrency support** — Focus is Vietnamese equities

Open an issue if you're unsure!

## Attribution

Contributions are attributed via Git commit authorship. Significant contributions may be acknowledged in:
- CHANGELOG.md release notes
- Project 2/3/thesis acknowledgments

## Questions?

- **General discussion**: [GitHub Discussions](../../discussions)
- **Bug/feature specifics**: [Open an issue](../../issues/new/choose)
- **Direct contact**: Via GitHub profile

---

*This project follows the principle: **"Show what you can defend."** Contributions with clear reasoning, tests, and documentation are prioritized.*