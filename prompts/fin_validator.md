# Financial Logic Validator
# Usage: "Read prompts/fin_validator.md, validate the financial calculations in src/[module].py"

## Your role
You are a quantitative finance checker.
Verify that all financial formulas are implemented correctly per Modern Portfolio Theory.

## Reference formulas to validate against

### Returns
- Simple return: r_t = (P_t - P_{t-1}) / P_{t-1}
- Log return: ln(P_t / P_{t-1})
- Annualized return: mean(daily_returns) × 252
- Annualized volatility: std(daily_returns) × sqrt(252)

### Portfolio metrics
- Portfolio return: sum(w_i × r_i)
- Portfolio variance: w^T × Σ × w
- Portfolio volatility: sqrt(portfolio_variance)
- Sharpe Ratio: (portfolio_return - risk_free_rate) / portfolio_volatility
  Note: use risk_free_rate = 0.045 for Vietnam (approximate SBV rate)

### Optimization
- Objective: minimize w^T × Σ × w
- Constraints: sum(w_i) = 1
- Bounds: 0 ≤ w_i ≤ 1

## Validation steps
1. Pick VCB as test case — calculate by hand using 5 days of data from DB
2. Compare with Python output — tolerance: ±0.0001
3. Check Covariance Matrix is positive semi-definite: all eigenvalues >= 0
4. Verify optimizer output is feasible: weights sum to 1, all non-negative

## Report format
| Formula | Expected | Python output | Match | Note |
