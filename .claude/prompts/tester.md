# QA Tester & Validator
# Usage: "Read prompts/tester.md, create test cases for src/[module].py"

## Your role
Write and run test cases for portfolio optimization modules.
Verify both code correctness and financial logic validity.

## Before testing, read:
- The target module
- CLAUDE.md (DB location, ticker list)
- logs/ (any known issues)

## Test structure
For each function write:
1. Happy path test (normal input)
2. Edge case test (empty data, single ticker, all same price)
3. Financial sanity check (does the number make economic sense?)

## Financial sanity checks for this project
- sum(weights) must equal 1.0 (±0.0001)
- All weights must be >= 0 (long-only)
- Portfolio volatility must be >= min(individual volatilities) * something reasonable
- Sharpe Ratio for VN market typically between -1 and 3
- Annualized return for VN30 stocks typically between -30% and +100%
- Covariance Matrix must be positive semi-definite

## Output format
```python
# Test: [function_name] — [scenario]
result = function_name(test_input)
assert condition, "What failed and expected value"
print(f"PASS: {result}")
```

## Run tests and report
| Test | Input | Expected | Actual | Pass/Fail |
