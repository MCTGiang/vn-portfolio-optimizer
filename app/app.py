"""
app.py — VN Portfolio Optimizer Dashboard
Minimalist & Professional Edition (Fixed UI/UX)
Run: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import io

# Mock data loader for UI testing (if modules are missing)
try:
    from data_loader import VN30_TICKERS, get_db_summary
    from optimizer import min_variance_portfolio
    from portfolio_metrics import portfolio_stats
except ImportError:
    VN30_TICKERS = ['VCB','VNM','HPG','FPT','MWG','BID','CTG','KDC','GAS','REE']
    def get_db_summary(): return pd.DataFrame({'start_date': ['2021-01-04'], 'end_date': ['2026-04-20'], 'rows': [39519]})
    def min_variance_portfolio(tickers):
        n = len(tickers)
        w = np.random.dirichlet(np.ones(n), size=1)[0]
        return {'weights': w, 'mu': pd.Series(np.random.uniform(0.05, 0.25, n), index=tickers), 
                'cov': pd.DataFrame(np.identity(n)*0.04, index=tickers, columns=tickers),
                'port_return': 0.12, 'port_volatility': 0.15, 'sharpe_ratio': 0.3, 'improvement_pct': 24.7}
    def portfolio_stats(w, mu, cov): return {'port_return': 0.10, 'port_volatility': 0.18, 'sharpe_ratio': 0.2}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VN Portfolio Optimizer",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ─────────────────────────────────────────────────────────────
C_BRAND    = "#146026"
C_TAG      = "#80c433"
C_YELLOW   = "#cbdd56"
C_NEUTRAL  = "#6B7B6E"
C_BORDER   = "#E5E7EB"
C_BG       = "#FFFFFF"
C_TEXT     = "#1F2937"
C_MUTED    = "#6B7280"
C_UP       = "#16A34A"
C_DOWN     = "#DC2626"
C_CARD_BG  = "#F9FAFB"

DONUT_COLORS = [C_BRAND, "#4CAF50", "#95bc26", C_YELLOW, "#A8D5A2", "#D4EDDA", C_MUTED, "#2D6A4F", "#52B788", "#B7E4C7", "#40916C", "#74C69D"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"], .stMarkdown, .stText {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}
.material-symbols-rounded, [data-testid="stIconMaterial"], .stIcon, i, svg {{
    font-family: 'Material Symbols Rounded' !important;
}}

.block-container {{ padding: 2rem 2rem 1rem 2rem !important; max-width: 100% !important; }}

section[data-testid="stSidebar"] > div:first-child {{
    background: {C_BG} !important; border-right: 1px solid {C_BORDER} !important; padding-top: 1rem !important;
}}

button[kind="primary"] {{
    background-color: {C_BRAND} !important;
    border-color: {C_BRAND} !important;
    color: white !important;
}}
button[kind="primary"]:hover {{
    background-color: #0f4a1c !important;
}}

span[data-baseweb="tag"] {{ background-color: {C_TAG} !important; border-radius: 4px !important; padding: 1px 8px !important; }}
span[data-baseweb="tag"] span {{ color: #fff !important; font-size: 12px !important; font-weight: 600 !important; }}

.kpi-wrap {{
    background: {C_CARD_BG}; border: 1px solid {C_BORDER}; border-radius: 8px; padding: 14px 16px 12px; min-height: 96px;
}}
.kpi-label {{ font-size: 11px; font-weight: 600; color: {C_MUTED}; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }}
.kpi-value {{ font-size: 28px; font-weight: 700; color: {C_TEXT}; line-height: 1.15; letter-spacing: -0.5px; }}
.kpi-delta {{ font-size: 12px; font-weight: 600; margin-top: 5px; display: flex; align-items: center; gap: 3px; }}
.kpi-delta.good  {{ color: {C_UP}; }}
.kpi-delta.bad   {{ color: {C_DOWN}; }}
.kpi-delta.neut  {{ color: {C_MUTED}; }}

.sec-hdr {{
    font-size: 13px; font-weight: 700; color: {C_TEXT}; text-transform: uppercase; letter-spacing: 0.05em;
    padding-bottom: 6px; border-bottom: 2px solid {C_BRAND}; margin-bottom: 12px; display: inline-block;
}}

.page-title {{ font-size: 26px; font-weight: 700; color: {C_TEXT}; margin: 0; padding: 0; letter-spacing: -0.5px; text-transform: uppercase; }}
.header-glossary {{ font-size: 13px; color: {C_MUTED}; margin-top: 6px; line-height: 1.6; }}

div[data-testid="stDataFrame"] *[role="columnheader"] > div {{
    display: flex !important; justify-content: center !important; text-align: center !important;
}}

hr {{ margin: 12px 0 20px !important; border-color: {C_BORDER} !important; }}

/* ── Export buttons: sync font size & style ── */
div[data-testid="stDownloadButton"] button {{
font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    color: {C_TEXT} !important;
    background: {C_BG} !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 6px !important;
    padding: 5px 12px !important;
    height: 38px !important; /* Cố định chiều cao */
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

div[data-testid="stDownloadButton"] button p {{
    font-size: 14px !important;
    line-height: 1 !important;
    margin: 0 !important;
}}

div[data-testid="stDownloadButton"] button:hover {{
    border-color: {C_BRAND} !important;
    color: {C_BRAND} !important;
    background: {C_BG} !important;
}}

div[data-testid="stSidebar"] button:has(div:contains("Cập nhật dữ liệu")) {{
    background-color: transparent !important;
    border: 1px solid #146026 !important;
    color: #146026 !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}}

div[data-testid="stSidebar"] button:has(div:contains("Cập nhật dữ liệu")):hover {{
    background-color: #146026 !important;
    color: white !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

.footer {{ font-size: 11px; color: {C_MUTED}; text-align: center; padding: 16px 0 10px; border-top: 1px solid {C_BORDER}; margin-top: 24px; }}
</style>
""", unsafe_allow_html=True)

# ── Language ──────────────────────────────────────────────────────────────────
LANG = {
    'vi': {
        'title'      : 'TỐI ƯU HÓA DANH MỤC VN30',
        'cfg'        : 'Danh mục',
        'pick'       : 'Chọn mã cổ phiếu (≥ 2)',
        'db_info'    : 'Dữ liệu',
        'model'      : 'Mô hình',
        'warn2'      : '⚠️ Vui lòng chọn ít nhất 2 mã cổ phiếu.',
        'spinning'   : 'Đang tối ưu hóa danh mục...',
        'kpi_ret'    : 'LỢI NHUẬN KỲ VỌNG',
        'kpi_vol'    : 'RỦI RO (VOLATILITY)',
        'kpi_sharpe' : 'TỶ SỐ SHARPE',
        'kpi_active' : 'VỊ THẾ HOẠT ĐỘNG',
        'vs_ew'      : 'so với Đồng đều',
        'vol_red'    : 'Rủi ro giảm',
        'sec_alloc'  : 'Phân bổ tỷ trọng',
        'sec_cmp'    : 'MVP vs Đồng đều',
        'sec_heat'   : 'Ma trận tương quan',
        'sec_tbl'    : 'Chi tiết phân bổ',
        'others'     : 'Khác',
        'mvp_lbl'    : 'MVP',
        'ew_lbl'     : 'Đồng đều',
        'col_ticker' : 'Mã CK',
        'col_mvp'    : 'Tỷ trọng MVP (%)',
        'col_ew'     : 'Tỷ trọng Đồng đều (%)',
        'col_ret'    : 'Lợi nhuận (%)',
        'col_vol'    : 'Rủi ro (%)',
        'exp_pdf'    : 'Xuất PDF',
        'exp_xlsx'   : 'Xuất Excel',
        'glossary'   : '<b>MVP</b> (Minimum Variance Portfolio) - Danh mục rủi ro tối thiểu<br><b>Đồng đều</b> (Equal Weights) - Danh mục chia đều tỷ trọng.',
        'data_scope1': '30 mã cổ phiếu thuộc rổ VN30',
        'data_scope2': '(Tham chiếu tại {mm_yyyy})',
        'source'     : 'Nguồn: VCI',
        'solver'     : 'Trình giải: scipy SLSQP',
        'rf_main'    : 'Rf = 4.5%',
        'rf_sub'     : '(Lãi suất phi rủi ro tham khảo SBV Việt Nam)',
        'footer'     : 'Markowitz (1952) Portfolio Selection · Dữ liệu: VCI qua vnstock3 · github.com/MCTGiang/vn-portfolio-optimizer',
    },
    'en': {
        'title'      : 'VN30 PORTFOLIO OPTIMIZER',
        'cfg'        : 'Portfolio',
        'pick'       : 'Select tickers (≥ 2)',
        'db_info'    : 'Data',
        'model'      : 'Model',
        'warn2'      : '⚠️ Please select at least 2 tickers.',
        'spinning'   : 'Optimizing portfolio...',
        'kpi_ret'    : 'EXPECTED RETURN',
        'kpi_vol'    : 'VOLATILITY (RISK)',
        'kpi_sharpe' : 'SHARPE RATIO',
        'kpi_active' : 'ACTIVE POSITIONS',
        'vs_ew'      : 'vs Equal Weights',
        'vol_red'    : 'Risk reduction',
        'sec_alloc'  : 'Portfolio Allocation',
        'sec_cmp'    : 'MVP vs Equal Weights',
        'sec_heat'   : 'Correlation Matrix',
        'sec_tbl'    : 'Allocation Detail',
        'others'     : 'Others',
        'mvp_lbl'    : 'MVP',
        'ew_lbl'     : 'Equal Weights',
        'col_ticker' : 'Ticker',
        'col_mvp'    : 'MVP Weight (%)',
        'col_ew'     : 'EW Weight (%)',
        'col_ret'    : 'Exp. Return (%)',
        'col_vol'    : 'Volatility (%)',
        'exp_pdf'    : 'Export PDF',
        'exp_xlsx'   : 'Export Excel',
        'glossary'   : '<b>MVP</b> - Minimum Variance Portfolio<br><b>Equal Weights</b> - Equally weighted portfolio.',
        'data_scope1': '30 VN30 tickers',
        'data_scope2': '(Reference at {mm_yyyy})',
        'source'     : 'Source: VCI',
        'solver'     : 'Solver: scipy SLSQP',
        'rf_main'    : 'Rf = 4.5%',
        'rf_sub'     : '(Risk-free rate - SBV Vietnam)',
        'footer'     : 'Markowitz (1952) Portfolio Selection · Data: VCI via vnstock3 · github.com/MCTGiang/vn-portfolio-optimizer',
    },
}

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'vi'

# ── Auto-init DB ───────────────────────────────────────────────────────────────
_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'portfolio.db')

def _db_is_ready():
    if not os.path.exists(_DB_PATH):
        return False
    try:
        import sqlite3
        con = sqlite3.connect(_DB_PATH)
        count = con.execute("SELECT COUNT(*) FROM Stock_Prices").fetchone()[0]
        con.close()
        return count > 1000
    except Exception:
        return False

if not _db_is_ready():
    st.set_page_config(page_title="VN Portfolio Optimizer", page_icon="📈", layout="wide")
    st.info("🔄 Đang khởi tạo dữ liệu lần đầu — vui lòng chờ khoảng 3 phút...")
    try:
        os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
        from data_loader import update_db
        update_db(start='2021-01-01')
        st.rerun()
    except Exception as e:
        st.error(f"❌ Không tải được dữ liệu: {e}")
        st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    lang_cur = st.session_state['lang']

    tb_col1, tb_col2 = st.columns(2)
    with tb_col1:
        if st.button("VIE", key="btn_vi", use_container_width=True, type="primary" if lang_cur == 'vi' else "secondary"):
            st.session_state['lang'] = 'vi'
            st.rerun()
    with tb_col2:
        if st.button("ENG", key="btn_en", use_container_width=True, type="primary" if lang_cur == 'en' else "secondary"):
            st.session_state['lang'] = 'en'
            st.rerun()

    L = LANG[st.session_state['lang']]

    st.markdown(f"<div style='font-size:11px;font-weight:700;color:{C_BRAND};text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px'>{L['cfg']}</div>", unsafe_allow_html=True)
    selected = st.multiselect(L['pick'], options=VN30_TICKERS, default=['VCB','VNM','HPG','FPT','MWG','BID','CTG','KDC','GAS','REE'], label_visibility="collapsed")
    st.caption(L['pick'])

    st.markdown(f"<div style='font-size:11px;font-weight:700;color:{C_BRAND};text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px'>{L['db_info']}</div>", unsafe_allow_html=True)
    try:
        summary = get_db_summary()
        end_date_str = summary['end_date'].max()
        mm_yyyy = f"{end_date_str[5:7]}/{end_date_str[:4]}"
        st.caption(f"📦 {L['source']}")
        st.caption(f"📅 {summary['start_date'].min()} → {end_date_str}")
        st.markdown(f"""
        <div style="font-size:14px;color:{C_MUTED};margin-top:4px;display:flex;align-items:flex-start;gap:6px;">
            <div style="margin-top:-2px;font-size:14px;">🗂</div>
            <div style="line-height:1.4;">
                {L['data_scope1']}<br>
                <span style="font-size:12px;opacity:0.85;">{L['data_scope2'].format(mm_yyyy=mm_yyyy)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception: pass

    st.markdown(f"<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    # Tạo nút cập nhật thủ công
    if st.sidebar.button("🔄 Cập nhật dữ liệu mới nhất", use_container_width=True):
        with st.status("🚀 Đang kết nối API và cập nhật Database...", expanded=True) as status:
            try:
                from data_loader import update_db
                # Gọi hàm update từ ngày cuối cùng trong DB hoặc một mốc cố định
                update_db(start='2021-01-01') 
                
                # QUAN TRỌNG: Xóa cache để dashboard load lại dữ liệu mới vừa tải về
                st.cache_data.clear()
                
                status.update(label="✅ Cập nhật thành công!", state="complete", expanded=False)
                st.toast("Dữ liệu đã được làm mới!", icon="✅")
                st.rerun()
            except Exception as e:
                status.update(label=f"❌ Lỗi: {str(e)}", state="error")
                st.sidebar.error("Không thể kết nối với nguồn dữ liệu.")

    st.caption("Lưu ý: Quá trình này có thể mất vài phút tùy vào tốc độ API.")

    st.markdown(f"<div style='font-size:11px;font-weight:700;color:{C_BRAND};text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px'>{L['model']}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:14px;color:{C_MUTED};line-height:1.8;">
        Minimum Variance Portfolio<br>
        Markowitz (1952)<br>
        {L['solver']}<br>
        <div style="line-height:1.4;margin-top:4px;">
            <span style="color:{C_TEXT};font-weight:500;">{L['rf_main']}</span><br>
            <span style="font-size:12px;opacity:0.85;">{L['rf_sub']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Header row ────────────────────────────────────────────────────────────────
c_title, c_pdf, c_excel = st.columns([5, 1.8, 1.8])

with c_title:
    st.markdown(f"<h1 class='page-title'>{L['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-glossary'>{L['glossary']}</div>", unsafe_allow_html=True)

with c_pdf:
    st.markdown(
        "<div>"
        "<button onclick='window.print()' style='"
        "width:100%; height:38px; padding:5px 12px; font-size:14px; font-weight:400;"
        "border:1px solid #E5E7EB; border-radius:6px;"
        "background:#fff; color:#1F2937; cursor:pointer;"
        "white-space:nowrap; display:flex; align-items:center; justify-content:center; gap:6px;"
        "font-family:Inter,-apple-system,sans-serif;"
        "'>📄 " + L['exp_pdf'] + "</button></div>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if len(selected) < 2:
    st.warning(L['warn2'])
    st.stop()

# ── Optimizer ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def run_optimizer(tickers_tuple): return min_variance_portfolio(list(tickers_tuple))

with st.spinner(L['spinning']):
    try:
        result = run_optimizer(tuple(sorted(selected)))
    except ValueError as e:
        if 'not in DB' in str(e):
            st.cache_data.clear()
            with st.spinner("🔄 Dữ liệu bị reset — đang tải lại (~3 phút)..."):
                try:
                    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
                    from data_loader import update_db
                    update_db(start='2021-01-01')
                    st.rerun()
                except Exception as reinit_err:
                    st.error(f"❌ Không tải được dữ liệu: {reinit_err}")
                    st.stop()
        else:
            st.error(f"❌ {e}")
            st.stop()
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()

N = len(selected)
w_eq = np.array([1.0 / N] * N)
mu = result['mu']
cov = result['cov']
eq_stats = portfolio_stats(w_eq, mu, cov)
std_arr = np.sqrt(np.diag(cov.values))

# ── Excel export ───────────────────────────────────────────────────────────────
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine='openpyxl') as writer:
    alloc_tmp = pd.DataFrame({
        L['col_ticker']: selected,
        L['col_mvp']   : [f"{w:.1%}" for w in result['weights']],
        L['col_ew']    : [f"{w:.1%}" for w in w_eq],
        L['col_ret']   : [f"{r:.1%}" for r in mu.values],
        L['col_vol']   : [f"{v:.1%}" for v in std_arr],
    }).sort_values(L['col_mvp'], ascending=False)
    alloc_tmp.to_excel(writer, sheet_name='Allocation', index=False)

    pd.DataFrame({
        'Chỉ số' if st.session_state['lang'] == 'vi' else 'Metric': [
            L['kpi_ret'], L['kpi_vol'], L['kpi_sharpe'],
            L['kpi_active'], 'Vol Reduction vs EW'
        ],
        L['mvp_lbl']: [
            f"{result['port_return']:.2%}",
            f"{result['port_volatility']:.2%}",
            f"{result['sharpe_ratio']:.3f}",
            f"{int((result['weights']>0.001).sum())} / {N}",
            f"{result['improvement_pct']:.1f}%",
        ],
        L['ew_lbl']: [
            f"{eq_stats['port_return']:.2%}",
            f"{eq_stats['port_volatility']:.2%}",
            f"{eq_stats['sharpe_ratio']:.3f}",
            f"{N} / {N}", "—",
        ],
    }).to_excel(writer, sheet_name='Metrics', index=False)

    corr_np = cov.values / np.outer(std_arr, std_arr)
    corr_df_xl = pd.DataFrame(corr_np.round(4), index=selected, columns=selected)
    corr_df_xl.to_excel(writer, sheet_name='Correlation')
buf.seek(0)

with c_excel:
    st.download_button(
        label=f"📊 {L['exp_xlsx']}",
        data=buf,
        file_name="portfolio_optimization.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

# ── KPI Cards ─────────────────────────────────────────────────────────────────
def kpi(label, val, delta, pct=True, decimals=2, invert=False):
    fmt = f"{{:.{decimals}%}}" if pct else f"{{:.{decimals}f}}"
    v_str = fmt.format(val)
    d_str = (f"+{fmt.format(delta)}" if delta >= 0 else fmt.format(delta))
    arrow = "▲" if delta > 0 else "▼" if delta < 0 else "—"
    css = ("good" if delta < 0 else "bad") if invert else ("good" if delta > 0 else "bad")
    if delta == 0: css = "neut"
    return f"<div class='kpi-wrap'><div class='kpi-label'>{label}</div><div class='kpi-value'>{v_str}</div><div class='kpi-delta {css}'>{arrow} {d_str} {L['vs_ew']}</div></div>"

c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi(L['kpi_ret'],    result['port_return'],     result['port_return']     - eq_stats['port_return']),                  unsafe_allow_html=True)
c2.markdown(kpi(L['kpi_vol'],    result['port_volatility'], result['port_volatility'] - eq_stats['port_volatility'], invert=True), unsafe_allow_html=True)
c3.markdown(kpi(L['kpi_sharpe'], result['sharpe_ratio'],    result['sharpe_ratio']    - eq_stats['sharpe_ratio'],    pct=False, decimals=3), unsafe_allow_html=True)
c4.markdown(f"<div class='kpi-wrap'><div class='kpi-label'>{L['kpi_active']}</div><div class='kpi-value'>{int((result['weights']>0.001).sum())} / {N}</div><div class='kpi-delta good'>▼ {L['vol_red']} {result['improvement_pct']:.1f}%</div></div>", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
col_pie, col_bar = st.columns(2)

with col_pie:
    st.markdown(f"<div class='sec-hdr'>{L['sec_alloc']}</div>", unsafe_allow_html=True)
    mask = result['weights'] >= 0.03
    labels = [t for t, m in zip(selected, mask) if m]
    vals = result['weights'][mask].tolist()
    if result['weights'][~mask].sum() > 0.001:
        labels.append(L['others']); vals.append(result['weights'][~mask].sum())
    colors = DONUT_COLORS[:len(vals)]
    if L['others'] in labels: colors[-1] = C_MUTED

    fig_pie = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.45,
        textinfo='label+percent', textposition='outside',
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2))
    ))
    fig_pie.update_layout(
        uniformtext_minsize=11, uniformtext_mode='hide',
        legend=dict(orientation='v', x=1.2, y=0.5, font=dict(size=12)),
        margin=dict(t=20, b=20, l=40, r=140),
        height=320, paper_bgcolor='rgba(0,0,0,0)'
    )
    fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Tỷ trọng: %{percent:.1%}<extra></extra>')
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

with col_bar:
    st.markdown(f"<div class='sec-hdr'>{L['sec_cmp']}</div>", unsafe_allow_html=True)
    m_labels = [L['kpi_ret'], L['kpi_vol'], L['kpi_sharpe']]
    m_vals = [result['port_return'], result['port_volatility'], result['sharpe_ratio']]
    e_vals = [eq_stats['port_return'], eq_stats['port_volatility'], eq_stats['sharpe_ratio']]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name=L['mvp_lbl'], x=m_labels, y=m_vals, marker_color=C_BRAND,
        text=[f"{v:.1%}" if i < 2 else f"{v:.3f}" for i, v in enumerate(m_vals)],
        textposition='outside'
    ))
    fig_bar.add_trace(go.Bar(
        name=L['ew_lbl'], x=m_labels, y=e_vals, marker_color='#E5E7EB',
        text=[f"{v:.1%}" if i < 2 else f"{v:.3f}" for i, v in enumerate(e_vals)],
        textposition='outside'
    ))
    fig_bar.update_layout(
        barmode='group',
        margin=dict(t=10, b=10, l=10, r=10),
        height=340,
        legend=dict(orientation='h', y=-0.15),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# ── Heatmap ───────────────────────────────────────────────────────────────────
st.markdown(f"<div style='margin-top:12px'><div class='sec-hdr'>{L['sec_heat']}</div></div>", unsafe_allow_html=True)
corr_df = pd.DataFrame((cov.values / np.outer(std_arr, std_arr)).round(2), index=selected, columns=selected)
heat_scale = [[0.0, C_BRAND], [0.3, "#52B788"], [0.55, "#FFE08A"], [0.75, "#FFA04A"], [1.0, "#DC2626"]]

fig_heat = go.Figure(go.Heatmap(
    z=corr_df.values, x=selected, y=selected,
    colorscale=heat_scale, zmin=-0.2, zmax=1.0,
    text=corr_df.values, texttemplate='%{text:.2f}'
))
fig_heat.update_layout(
    margin=dict(t=10, b=10, l=10, r=10),
    height=max(250, 24 * len(selected)),
    xaxis=dict(tickangle=-45),
    yaxis=dict(autorange='reversed'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})

# ── Allocation Table ──────────────────────────────────────────────────────────
st.markdown(f"<div style='margin-top:12px'><div class='sec-hdr'>{L['sec_tbl']}</div></div>", unsafe_allow_html=True)

alloc_disp = pd.DataFrame({
    L['col_ticker']: selected,
    L['col_mvp']   : result['weights'] * 100,
    L['col_ew']    : w_eq * 100,
    L['col_ret']   : mu.values * 100,
    L['col_vol']   : std_arr * 100,
}).sort_values(L['col_mvp'], ascending=False).reset_index(drop=True)

st.dataframe(
    alloc_disp,
    use_container_width=True,
    hide_index=True,
    column_config={
        L['col_ticker']: st.column_config.TextColumn(L['col_ticker'], alignment="center"),
        L['col_mvp']   : st.column_config.NumberColumn(L['col_mvp'],  format="%.1f%%", alignment="center"),
        L['col_ew']    : st.column_config.NumberColumn(L['col_ew'],   format="%.1f%%", alignment="center"),
        L['col_ret']   : st.column_config.NumberColumn(L['col_ret'],  format="%.1f%%", alignment="center"),
        L['col_vol']   : st.column_config.NumberColumn(L['col_vol'],  format="%.1f%%", alignment="center"),
    }
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"<div class='footer'>{L['footer']}</div>", unsafe_allow_html=True)