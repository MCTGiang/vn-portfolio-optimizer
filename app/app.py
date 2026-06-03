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
import plotly.io as pio
import streamlit.components.v1 as components
from datetime import datetime

# Fallback mock data for UI testing when src modules are unavailable
try:
    from data_loader import VN30_TICKERS, get_db_summary
    from optimizer import min_variance_portfolio
    from portfolio_metrics import portfolio_stats
except ImportError:
    VN30_TICKERS = ['VCB','VNM','HPG','FPT','MWG','BID','CTG','VIC','GAS','MSN']
    def get_db_summary(): return pd.DataFrame({'start_date': ['2021-01-01'], 'end_date': ['2026-04-20'], 'rows': [39519]})
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

/* Gộp chung CSS cho cả nút Print (stButton) và nút Excel (stDownloadButton) */
div[data-testid="stDownloadButton"] button, 
div[data-testid="stButton"] button {{
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    color: #1F2937 !important;
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 6px !important;
    padding: 5px 12px !important;
    height: 38px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

div[data-testid="stDownloadButton"] button p,
div[data-testid="stButton"] button p {{
    font-size: 14px !important;
    line-height: 1 !important;
    margin: 0 !important;
}}

div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stButton"] button:hover {{
    border-color: #146026 !important; /* Màu xanh thương hiệu */
    color: #146026 !important;
    background: #FFFFFF !important;
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

/* 1. Phục hồi màu cho nút Primary (VIE/ENG) */
div[data-testid="stButton"] button[kind="primary"] {{
    background-color: #146026 !important;
    border-color: #146026 !important;
    color: white !important;
}}
div[data-testid="stButton"] button[kind="primary"] p {{
    color: white !important;
}}

/* 2. Làm nổi bật nút Cập nhật dữ liệu ở Sidebar */
div[data-testid="stSidebar"] button:has(p:contains("Cập nhật")) {{
    background-color: #f4faed !important; /* Nền xanh rất nhạt */
    border: 1px solid #80c433 !important; /* Viền xanh lime (Màu VCBS) */
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}}
div[data-testid="stSidebar"] button:has(p:contains("Cập nhật")) p {{
    color: #146026 !important; /* Chữ màu xanh đậm thương hiệu */
    font-weight: 600 !important;
}}
div[data-testid="stSidebar"] button:has(p:contains("Cập nhật")):hover {{
    background-color: #80c433 !important; /* Đổi màu nền khi trỏ chuột */
    border-color: #80c433 !important;
}}

div[data-testid="stSidebar"] button:has(p:contains("Cập nhật")):hover p {{
    color: white !important; /* Chữ trắng khi trỏ chuột */
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
        'data_scope1': '29 mã cổ phiếu thuộc rổ VN30',
        'data_scope2': '(Tham chiếu tại 04/2026 - Loại VPL do mới niêm yết 2025)',
        'source'     : 'Nguồn: VCI',
        'solver'     : 'Trình giải: scipy SLSQP',
        'rf_main'    : 'Rf = 4.5%',
        'rf_sub'     : '(Lãi suất phi rủi ro tham khảo SBV Việt Nam)',
        'btn_update'      : 'Cập nhật dữ liệu mới nhất',
        'status_updating' : 'Đang kết nối API và cập nhật Database...',
        'status_success'  : 'Cập nhật thành công!',
        'toast_success'   : 'Dữ liệu đã được làm mới!',
        'status_err'      : 'Lỗi',
        'toast_err'       : 'Không thể kết nối với nguồn dữ liệu.',
        'note_update'     : 'Lưu ý: Quá trình này có thể mất vài phút tùy vào tốc độ API.',
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
        'data_scope1': '29 VN30 tickers',
        'data_scope2': '(Reference at 04/2026 - Excl. VPL listed in 2025)',
        'source'     : 'Source: VCI',
        'solver'     : 'Solver: scipy SLSQP',
        'rf_main'    : 'Rf = 4.5%',
        'rf_sub'     : '(Risk-free rate - SBV Vietnam)',
        'btn_update'      : 'Update latest data',
        'status_updating' : 'Connecting to API and updating Database...',
        'status_success'  : 'Update successful!',
        'toast_success'   : 'Data has been refreshed!',
        'status_err'      : 'Error',
        'toast_err'       : 'Could not connect to data source.',
        'note_update'     : 'Note: This process may take a few minutes depending on API speed.',
        'footer'     : 'Markowitz (1952) Portfolio Selection · Data: VCI via vnstock3 · github.com/MCTGiang/vn-portfolio-optimizer',
    },
}

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'vi'

# ── DB initialization — must run before any other component ──────────────────
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
    # Show minimal page while fetching data for the first time (e.g. Streamlit Cloud)
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

    # Language toggle — two buttons styled as a pill via CSS
    tb_col1, tb_col2 = st.columns(2)
    with tb_col1:
        if st.button("VIE", key="btn_vi", width='stretch', type="primary" if lang_cur == 'vi' else "secondary"):
            st.session_state['lang'] = 'vi'
            st.rerun()
    with tb_col2:
        if st.button("ENG", key="btn_en", width='stretch', type="primary" if lang_cur == 'en' else "secondary"):
            st.session_state['lang'] = 'en'
            st.rerun()

    L = LANG[st.session_state['lang']]

    # Ticker selection
    st.markdown(f"<div style='font-size:11px;font-weight:700;color:{C_BRAND};text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px'>{L['cfg']}</div>", unsafe_allow_html=True)
    selected = st.multiselect(L['pick'], options=VN30_TICKERS, default=['VCB','VNM','HPG','FPT','MWG','BID','CTG','VIC','GAS','MSN'], label_visibility="collapsed")
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
            <div style="margin-top:-2px;font-size:14px;">📊</div>
            <div style="line-height:1.4;">
                {L['data_scope1']}<br>
                <span style="font-size:12px;opacity:0.85;">{L['data_scope2'].format(mm_yyyy=mm_yyyy)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception: pass

    # Manual data refresh button
    st.markdown(f"<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    if st.sidebar.button(f"🔄 {L['btn_update']}", width='stretch'):
        with st.status(f"🚀 {L['status_updating']}", expanded=True) as status:
            try:
                from data_loader import update_db, get_db_summary
                # Latest day in DB — only fetch new data from that point onward to minimize API calls and speed up the update process
                summary = get_db_summary()
                latest_date_str = summary['end_date'].max()
                update_db(start=latest_date_str) 
                
                st.cache_data.clear()
                
                status.update(label=f"✅ {L['status_success']}", state="complete", expanded=False)
                st.toast(L['toast_success'], icon="✅")
                st.rerun()
            except Exception as e:
                import traceback
                print("\n=== LỖI KHI BẤM NÚT CẬP NHẬT ===")
                traceback.print_exc() 
                print("==================================\n")
                
                status.update(label=f"❌ {L['status_err']}: {str(e)}", state="error")
                st.sidebar.error(L['toast_err'])

    st.markdown(
        f'<div style="font-size:12px; opacity:0.85; color:#6B7280; margin-top:4px; line-height:1.4;">'
        f'{L["note_update"]}'
        f'</div>', 
        unsafe_allow_html=True
    )

    # Model info
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
    # Placeholder — nút PDF sẽ được render bên dưới sau khi biểu đồ đã sẵn sàng
    pdf_placeholder = st.empty()

st.markdown("<hr>", unsafe_allow_html=True)

# ── Guard — require at least 2 tickers ───────────────────────────────────────
if len(selected) < 2:
    st.warning(L['warn2'])
    st.stop()

# ── Portfolio optimizer (cached, invalidates after 1 hour) ───────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def run_optimizer(tickers_tuple): return min_variance_portfolio(list(tickers_tuple))

with st.spinner(L['spinning']):
    try:
        result = run_optimizer(tuple(sorted(selected)))
    except ValueError as e:
        if 'not in DB' in str(e):
            # DB was wiped by cloud container restart — reinitialize automatically
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

# ── Derived variables ─────────────────────────────────────────────────────────
N = len(selected)
w_eq = np.array([1.0 / N] * N)
mu = result['mu']
cov = result['cov']
eq_stats = portfolio_stats(w_eq, mu, cov)
std_arr = np.sqrt(np.diag(cov.values))

# ── Excel export — 3 sheets: Allocation, Metrics, Correlation ─────────────────
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine='openpyxl') as writer:
    # Sheet 1: per-ticker allocation comparison
    alloc_tmp = pd.DataFrame({
        L['col_ticker']: selected,
        L['col_mvp']   : [f"{w:.1%}" for w in result['weights']],
        L['col_ew']    : [f"{w:.1%}" for w in w_eq],
        L['col_ret']   : [f"{r:.1%}" for r in mu.values],
        L['col_vol']   : [f"{v:.1%}" for v in std_arr],
    }).sort_values(L['col_mvp'], ascending=False)
    alloc_tmp.to_excel(writer, sheet_name='Allocation', index=False)

    # Sheet 2: portfolio-level metrics vs equal weights
    metric_label = 'Chỉ số' if st.session_state['lang'] == 'vi' else 'Metric'
    pd.DataFrame({
        metric_label: [L['kpi_ret'], L['kpi_vol'], L['kpi_sharpe'], L['kpi_active'], 'Vol Reduction vs EW'],
        L['mvp_lbl'] : [
            f"{result['port_return']:.2%}",
            f"{result['port_volatility']:.2%}",
            f"{result['sharpe_ratio']:.3f}",
            f"{int((result['weights'] > 0.001).sum())} / {N}",
            f"{result['improvement_pct']:.1f}%",
        ],
        L['ew_lbl']  : [
            f"{eq_stats['port_return']:.2%}",
            f"{eq_stats['port_volatility']:.2%}",
            f"{eq_stats['sharpe_ratio']:.3f}",
            f"{N} / {N}", "—",
        ],
    }).to_excel(writer, sheet_name='Metrics', index=False)

    # Sheet 3: pairwise correlation matrix
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
        width='stretch',
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

# ── KPI row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi(L['kpi_ret'],    result['port_return'],     result['port_return']     - eq_stats['port_return']),                  unsafe_allow_html=True)
c2.markdown(kpi(L['kpi_vol'],    result['port_volatility'], result['port_volatility'] - eq_stats['port_volatility'], invert=True), unsafe_allow_html=True)
c3.markdown(kpi(L['kpi_sharpe'], result['sharpe_ratio'],    result['sharpe_ratio']    - eq_stats['sharpe_ratio'],    pct=False, decimals=3), unsafe_allow_html=True)
c4.markdown(f"<div class='kpi-wrap'><div class='kpi-label'>{L['kpi_active']}</div><div class='kpi-value'>{int((result['weights']>0.001).sum())} / {N}</div><div class='kpi-delta good'>▼ {L['vol_red']} {result['improvement_pct']:.1f}%</div></div>", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Charts row ────────────────────────────────────────────────────────────────────
col_pie, col_bar = st.columns(2)

# Donut chart — allocation (tickers < 3% grouped into "Others")
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
    st.plotly_chart(fig_pie, width='stretch', config={'displayModeBar': False})

# Grouped bar chart — MVP vs Equal Weights on Return, Volatility, Sharpe
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
    st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': False})

# ── Correlation heatmap ───────────────────────────────────────────────────────
# Color scale: dark green (low) → yellow (mid) → orange-red (high = needs attention)
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
st.plotly_chart(fig_heat, width='stretch', config={'displayModeBar': False})

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
    width='stretch',
    hide_index=True,
    column_config={
        L['col_ticker']: st.column_config.TextColumn(L['col_ticker'], alignment="center"),
        L['col_mvp']   : st.column_config.NumberColumn(L['col_mvp'],  format="%.1f%%", alignment="center"),
        L['col_ew']    : st.column_config.NumberColumn(L['col_ew'],   format="%.1f%%", alignment="center"),
        L['col_ret']   : st.column_config.NumberColumn(L['col_ret'],  format="%.1f%%", alignment="center"),
        L['col_vol']   : st.column_config.NumberColumn(L['col_vol'],  format="%.1f%%", alignment="center"),
    }
)

# ── PDF Export — render sau khi tất cả biểu đồ đã sẵn sàng ──────────────────
# ── PDF Export — comprehensive layout matching dashboard ─────────────────────
def build_pdf(fig_donut, fig_bar, fig_heat, result, eq_stats, lang_key,
              selected_tickers, w_eq_arr, std_arr_val):
    """
    Tạo PDF báo cáo đầy đủ giống dashboard:
    Trang 1: Header xanh + 4 KPI cards + Donut + Bar (2 cột)
    Trang 2: Header xanh + Heatmap + Bảng chi tiết phân bổ
    Dùng matplotlib (không cần Chrome/kaleido).
    """
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    import numpy as _np
    import tempfile, os, glob

    L_cur = LANG[lang_key]

    # ── 1. Setup Unicode font (cho cả PDF và matplotlib) ──────────────────
    # Tìm DejaVuSans trong nhiều vị trí khả dĩ
    font_search_dirs = [
        os.path.join(os.path.dirname(__file__), 'fonts'),
        os.path.join(os.path.dirname(__file__), '..', 'fonts'),
        '/usr/share/fonts/truetype/dejavu',
        '/usr/share/fonts/TTF',
        '/Library/Fonts',
        'C:/Windows/Fonts',
    ]
    font_regular = font_bold = font_italic = None
    for d in font_search_dirs:
        for pat in ['DejaVuSans.ttf', 'DejaVuSans-*.ttf']:
            for f in glob.glob(os.path.join(d, pat)):
                fname = os.path.basename(f).lower()
                if 'bold' in fname and font_bold is None:
                    font_bold = f
                elif 'oblique' in fname and font_italic is None:
                    font_italic = f
                elif fname == 'dejavusans.ttf' and font_regular is None:
                    font_regular = f
        if font_regular and font_bold:
            break

    # Set matplotlib font (nếu có DejaVu — tránh "missing glyph" cho dấu Việt)
    if font_regular:
        try:
            font_manager.fontManager.addfont(font_regular)
            if font_bold:   font_manager.fontManager.addfont(font_bold)
            if font_italic: font_manager.fontManager.addfont(font_italic)
            plt.rcParams['font.family']      = 'DejaVu Sans'
            plt.rcParams['font.sans-serif']  = ['DejaVu Sans']
        except Exception:
            pass

    # ── 2. Khởi tạo PDF ───────────────────────────────────────────────────
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)  # tự quản lý layout

    # Đăng ký font Unicode cho PDF
    FONT = None
    if font_regular and font_bold:
        try:
            pdf.add_font("DejaVu", style="",  fname=font_regular)
            pdf.add_font("DejaVu", style="B", fname=font_bold)
            if font_italic:
                pdf.add_font("DejaVu", style="I", fname=font_italic)
            else:
                pdf.add_font("DejaVu", style="I", fname=font_regular)
            FONT = "DejaVu"
        except Exception:
            FONT = None

    def set_font(size, style=""):
        if FONT:
            pdf.set_font(FONT, style=style, size=size)
        else:
            pdf.set_font("Helvetica", style=style, size=size)

    def safe(text):
        """Strip dấu tiếng Việt nếu không có Unicode font."""
        if FONT:
            return text
        import unicodedata
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    # ── 3. Helper vẽ biểu đồ bằng matplotlib ──────────────────────────────
    tmpdir = tempfile.mkdtemp()
    BRAND  = '#146026'
    LIME   = '#80c433'
    GRAY_BG = '#E5E7EB'

    DONUT_COLORS_MPL = ['#146026', '#4CAF50', '#95bc26', '#cbdd56', '#A8D5A2',
                        '#D4EDDA', '#6B7280', '#2D6A4F', '#52B788', '#B7E4C7',
                        '#40916C', '#74C69D']

    def draw_donut(path, tickers, weights, others_label):
        mask = weights >= 0.03
        lbls = [t for t, m in zip(tickers, mask) if m]
        vals = weights[mask].tolist()
        other_sum = weights[~mask].sum()
        if other_sum > 0.001:
            lbls.append(others_label); vals.append(other_sum)
        clrs = DONUT_COLORS_MPL[:len(vals)]

        fig, ax = plt.subplots(figsize=(5.5, 4.2), facecolor='white')
        wedges, texts, autotexts = ax.pie(
            vals, labels=lbls, colors=clrs,
            autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
            pctdistance=0.78, labeldistance=1.1,
            textprops={'fontsize': 9}
        )
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold'); at.set_fontsize(8)
        ax.axis('equal')
        plt.tight_layout(pad=0.5)
        plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close(fig)

    def draw_bar(path, m_vals, e_vals, m_labels, mvp_lbl, ew_lbl):
        x = _np.arange(len(m_labels))
        w = 0.35
        fig, ax = plt.subplots(figsize=(5.5, 4.2), facecolor='white')
        b1 = ax.bar(x - w/2, m_vals, w, label=mvp_lbl, color=BRAND)
        b2 = ax.bar(x + w/2, e_vals, w, label=ew_lbl,  color=GRAY_BG,
                    edgecolor='#9CA3AF', linewidth=0.5)
        for bars, vals in [(b1, m_vals), (b2, e_vals)]:
            for bar, v in zip(bars, vals):
                txt = f'{v:.1%}' if abs(v) < 2 else f'{v:.3f}'
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        txt, ha='center', va='bottom', fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(m_labels, fontsize=9)
        ax.set_ylim(0, max(max(m_vals), max(e_vals)) * 1.25)
        ax.yaxis.set_visible(False)
        for s in ['top','right','left']:
            ax.spines[s].set_visible(False)
        ax.spines['bottom'].set_color('#9CA3AF')
        ax.legend(fontsize=9, loc='upper right', frameon=False)
        plt.tight_layout(pad=0.5)
        plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close(fig)

    def draw_heatmap(path, corr_matrix, tickers):
        n = len(tickers)
        fig, ax = plt.subplots(figsize=(max(7, n * 0.6), max(5.5, n * 0.55)),
                               facecolor='white')
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'vn', ['#146026', '#52B788', '#FFE08A', '#FFA04A', '#DC2626'])
        im = ax.imshow(corr_matrix, cmap=cmap, vmin=-0.2, vmax=1.0, aspect='auto')
        ax.set_xticks(range(n)); ax.set_xticklabels(tickers, rotation=0, fontsize=8)
        ax.set_yticks(range(n)); ax.set_yticklabels(tickers, fontsize=8)
        for i in range(n):
            for j in range(n):
                val = corr_matrix[i, j]
                clr = 'white' if val > 0.7 or val < 0.15 else '#1F2937'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=7, color=clr)
        cbar = plt.colorbar(im, ax=ax, shrink=0.7)
        cbar.ax.tick_params(labelsize=7)
        plt.tight_layout(pad=0.3)
        plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close(fig)

    # ── 4. Tạo ảnh ────────────────────────────────────────────────────────
    tickers_list = list(result['tickers'])
    weights_arr  = _np.array(result['weights'])
    others_lbl   = safe("Khác") if lang_key == 'vi' else "Others"

    donut_path = os.path.join(tmpdir, "donut.png")
    bar_path   = os.path.join(tmpdir, "bar.png")
    heat_path  = os.path.join(tmpdir, "heat.png")

    draw_donut(donut_path, tickers_list, weights_arr, others_lbl)

    m_labels = [safe(L_cur['kpi_ret']), safe(L_cur['kpi_vol']), safe(L_cur['kpi_sharpe'])]
    m_vals   = [result['port_return'], result['port_volatility'], result['sharpe_ratio']]
    e_vals   = [eq_stats['port_return'], eq_stats['port_volatility'], eq_stats['sharpe_ratio']]
    draw_bar(bar_path, m_vals, e_vals, m_labels,
             safe(L_cur['mvp_lbl']), safe(L_cur['ew_lbl']))

    corr = result['cov'].values / _np.outer(std_arr_val, std_arr_val)
    draw_heatmap(heat_path, corr, tickers_list)

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                          TRANG 1                                    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    pdf.add_page()

    # ── Header xanh ──────────────────────────────────────────────────────
    pdf.set_fill_color(20, 96, 38)   # #146026
    pdf.rect(0, 0, 297, 22, style='F')
    pdf.set_text_color(255, 255, 255)
    set_font(16, "B")
    pdf.set_xy(10, 5)
    title = safe("TỐI ƯU HÓA DANH MỤC VN30") if lang_key == 'vi' else "VN30 PORTFOLIO OPTIMIZER"
    pdf.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    set_font(9, "")
    pdf.set_xy(10, 13)
    subt = safe("Minimum Variance Portfolio · Markowitz (1952) · Rf = 4.5% (SBV)")
    pdf.cell(0, 5, subt, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.set_text_color(31, 41, 55)
    pdf.ln(6)

    # ── 4 KPI cards ───────────────────────────────────────────────────────
    kpi_y = 28
    kpi_w = 67
    kpi_h = 22
    kpi_x_start = 10
    kpi_gap = 3

    n_active = int((weights_arr > 0.001).sum())
    delta_ret    = result['port_return']     - eq_stats['port_return']
    delta_vol    = result['port_volatility'] - eq_stats['port_volatility']
    delta_sharpe = result['sharpe_ratio']    - eq_stats['sharpe_ratio']
    vol_red_pct  = result.get('improvement_pct',
                              (eq_stats['port_volatility'] - result['port_volatility']) /
                              eq_stats['port_volatility'] * 100)

    kpis = [
        (safe(L_cur['kpi_ret']),    f"{result['port_return']:.2%}",
         f"{'+' if delta_ret>=0 else ''}{delta_ret*100:.2f}%", delta_ret > 0),
        (safe(L_cur['kpi_vol']),    f"{result['port_volatility']:.2%}",
         f"{'+' if delta_vol>=0 else ''}{delta_vol*100:.2f}%", delta_vol < 0),
        (safe(L_cur['kpi_sharpe']), f"{result['sharpe_ratio']:.3f}",
         f"{'+' if delta_sharpe>=0 else ''}{delta_sharpe:.3f}", delta_sharpe > 0),
        (safe(L_cur['kpi_active']), f"{n_active} / {len(tickers_list)}",
         safe(f"Rủi ro giảm {vol_red_pct:.1f}%") if lang_key == 'vi'
         else f"Vol reduced {vol_red_pct:.1f}%", True),
    ]

    for i, (lbl, val, delta_str, is_good) in enumerate(kpis):
        x = kpi_x_start + i * (kpi_w + kpi_gap)
        # card bg
        pdf.set_fill_color(249, 250, 251)  # #F9FAFB
        pdf.set_draw_color(229, 231, 235)
        pdf.rect(x, kpi_y, kpi_w, kpi_h, style='DF')
        # label
        pdf.set_xy(x + 3, kpi_y + 2)
        pdf.set_text_color(107, 114, 128)
        set_font(7, "B")
        pdf.cell(kpi_w - 6, 3, lbl, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        # value
        pdf.set_xy(x + 3, kpi_y + 7)
        pdf.set_text_color(31, 41, 55)
        set_font(13, "B")
        pdf.cell(kpi_w - 6, 7, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        # delta
        pdf.set_xy(x + 3, kpi_y + 16)
        if is_good:
            pdf.set_text_color(22, 163, 74)
        else:
            pdf.set_text_color(220, 38, 38)
        set_font(7, "")
        arrow = "▲" if (i < 3 and is_good) or (i == 1 and not is_good) else "▼"
        # Simpler arrows that DejaVu supports
        arrow = "+" if is_good and i != 1 else ("-" if not is_good else "v")
        if i == 3: arrow = "v"
        pdf.cell(kpi_w - 6, 3, f"{arrow} {delta_str}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

    # ── Donut + Bar song song ────────────────────────────────────────────
    chart_y = kpi_y + kpi_h + 6
    chart_h = 90
    pdf.set_text_color(31, 41, 55)

    # Tiêu đề biểu đồ
    set_font(10, "B")
    pdf.set_xy(10, chart_y)
    pdf.cell(140, 5, safe(L_cur['sec_alloc']), align='L')
    pdf.set_xy(152, chart_y)
    pdf.cell(140, 5, safe(L_cur['sec_cmp']), align='L')
    # underline
    pdf.set_draw_color(20, 96, 38); pdf.set_line_width(0.5)
    pdf.line(10, chart_y + 5.5, 60, chart_y + 5.5)
    pdf.line(152, chart_y + 5.5, 202, chart_y + 5.5)

    # Render ảnh
    pdf.image(donut_path, x=10,  y=chart_y + 7, w=135, h=chart_h)
    pdf.image(bar_path,   x=152, y=chart_y + 7, w=135, h=chart_h)

    # Footer trang 1
    pdf.set_y(200)
    pdf.set_text_color(130, 130, 130)
    set_font(7, "I")
    pdf.cell(0, 4, safe("Trang 1/2 · Markowitz (1952) Portfolio Selection · VCI via vnstock"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║                          TRANG 2                                    ║
    # ╚════════════════════════════════════════════════════════════════════╝
    pdf.add_page()

    # ── Header xanh trang 2 ──────────────────────────────────────────────
    pdf.set_fill_color(20, 96, 38)
    pdf.rect(0, 0, 297, 16, style='F')
    pdf.set_text_color(255, 255, 255)
    set_font(13, "B")
    pdf.set_xy(10, 4)
    pdf.cell(0, 8, safe(L_cur['sec_heat']) + "  &  " + safe(L_cur['sec_tbl']),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

    pdf.set_text_color(31, 41, 55)
    pdf.set_y(20)

    # ── Heatmap (full width) ─────────────────────────────────────────────
    heat_h = 110 if len(tickers_list) <= 10 else 130
    pdf.image(heat_path, x=10, y=22, w=277, h=heat_h)

    # ── Bảng chi tiết phân bổ ────────────────────────────────────────────
    table_y = 22 + heat_h + 4
    pdf.set_y(table_y)

    # Header bảng
    pdf.set_fill_color(20, 96, 38)
    pdf.set_text_color(255, 255, 255)
    set_font(8, "B")
    col_w = [40, 55, 55, 55, 55]  # tổng 260
    col_x = 18
    headers = [safe(L_cur['col_ticker']), safe(L_cur['col_mvp']),
               safe(L_cur['col_ew']),     safe(L_cur['col_ret']),
               safe(L_cur['col_vol'])]
    pdf.set_x(col_x)
    for w, h in zip(col_w, headers):
        pdf.cell(w, 6, h, border=0, align='C', fill=True)
    pdf.ln(6)

    # Sort theo MVP weight giảm dần
    sort_idx = sorted(range(len(tickers_list)),
                      key=lambda i: -weights_arr[i])
    pdf.set_text_color(31, 41, 55)
    set_font(8, "")
    row_count_max = 10  # hiển thị tối đa 10 dòng trong PDF cho gọn
    rows_to_show = sort_idx[:row_count_max]
    for idx_pos, i in enumerate(rows_to_show):
        if idx_pos % 2 == 0:
            pdf.set_fill_color(249, 250, 251)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_x(col_x)
        cells = [
            tickers_list[i],
            f"{weights_arr[i]*100:.1f}%",
            f"{w_eq_arr[i]*100:.1f}%",
            f"{result['mu'].values[i]*100:.1f}%",
            f"{std_arr_val[i]*100:.1f}%",
        ]
        for w, c in zip(col_w, cells):
            pdf.cell(w, 5.5, c, border=0, align='C', fill=True)
        pdf.ln(5.5)

    # Footer trang 2
    pdf.set_y(200)
    pdf.set_text_color(130, 130, 130)
    set_font(7, "I")
    pdf.cell(0, 4,
             safe("Trang 2/2 · github.com/MCTGiang/vn-portfolio-optimizer · MSSV 202490043"),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    return bytes(pdf.output())



try:
    pdf_bytes = build_pdf(fig_pie, fig_bar, fig_heat, result, eq_stats,
                          st.session_state['lang'],
                          selected, w_eq, std_arr)
    with pdf_placeholder:
        st.download_button(
            label=f"📄 {L['exp_pdf']}",
            data=pdf_bytes,
            file_name="portfolio_optimization.pdf",
            mime="application/pdf",
            width='stretch',
        )
except Exception as pdf_err:
    with pdf_placeholder:
        st.caption(f"⚠️ PDF: {pdf_err}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"<div class='footer'>{L['footer']}</div>", unsafe_allow_html=True)