# Demo Preparer & UX Reviewer
# Usage: "Read prompts/demo.md, help me prepare the demo"

## Your role
Prepare a compelling demo of the portfolio optimization system.
Target audience: thesis advisor and examination board (Vietnamese).

## Demo script template (2-3 minutes)

### Opening (20 seconds)
"Đây là hệ thống tối ưu hóa danh mục đầu tư cho thị trường chứng khoán Việt Nam.
Hệ thống sử dụng Modern Portfolio Theory của Markowitz để tìm tỷ trọng phân bổ
tối ưu cho danh mục gồm các cổ phiếu VN30."

### Data section (30 seconds)
- Show: 30 mã VN30, dữ liệu 2021-2026 từ VCI
- Show: giá VCB gần nhất, so sánh với thị trường

### Optimization section (60 seconds)
- Select 5-6 tickers on dashboard
- Show: Pie chart tỷ trọng tối ưu vs Equal Weights
- Explain: "Minimum Variance Portfolio giảm rủi ro từ X% xuống Y%"
- Show: Correlation Heatmap — "các mã ít tương quan giúp đa dạng hóa tốt hơn"

### Metrics section (30 seconds)
- Show: Sharpe Ratio, Expected Return, Volatility
- Compare Optimized vs Equal Weights side by side

### Closing (20 seconds)
"Project 2 sẽ mở rộng sang Efficient Frontier và Auto-Rebalancing.
Đồ án tốt nghiệp sẽ tích hợp thêm Ensemble ML dự báo giá và quản lý rủi ro VaR/CVaR."

## UX checklist before demo
- [ ] Dashboard loads in < 5 seconds
- [ ] Pie chart shows % labels clearly
- [ ] Metric cards visible without scrolling
- [ ] Works on mobile (test on phone)
- [ ] No error when selecting edge case tickers
- [ ] Video recorded as backup (2-3 min)

## Defense Q&A preparation
See prompts/advisor.md for full Q&A practice
