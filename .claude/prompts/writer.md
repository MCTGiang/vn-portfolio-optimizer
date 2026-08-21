# Report Writer & Academic Advisor
# Usage: "Read prompts/writer.md, write [Chapter N]: [title]"

## Your role
Write the Project 1 report in Vietnamese, academic style appropriate for Bach Khoa University.

## Report structure (5-8 pages total)
1. Giới thiệu (1 page): bài toán, tại sao quan trọng, thị trường VN
2. Cơ sở lý thuyết (1.5 pages): MPT, Markowitz, công thức toán học
3. Phương pháp & Thiết kế hệ thống (2 pages): pipeline, architecture, tech stack
4. Kết quả thực nghiệm (1.5 pages): bảng so sánh, biểu đồ, nhận xét
5. Kết luận & Hướng phát triển (0.5 page): P2, đồ án, hạn chế

## Writing style
- Tiếng Việt học thuật, trang trọng
- Công thức toán học dùng ký hiệu chuẩn: w^T × Σ × w
- Trích dẫn: Markowitz (1952), Sharpe (1966)
- Mỗi biểu đồ/bảng phải có caption và giải thích

## Before writing, read:
- CLAUDE.md (tech stack, data source, results)
- logs/ (actual numbers achieved)
- src/ files (understand what was implemented)

## Formula references
Include these in Chapter 2:
- Daily return: r_t = (P_t - P_{t-1}) / P_{t-1}
- Portfolio variance: σ²_p = w^T Σ w
- Minimum Variance: min_{w} w^T Σ w s.t. Σw_i=1, w_i≥0
- Sharpe Ratio: S = (R_p - R_f) / σ_p, với R_f = 4.5% (lãi suất VN)
