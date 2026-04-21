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
C_BRAND    = "#146026"   # dark green — brand / MVP
C_TAG      = "#80c433"   # bright green — sidebar tags
C_YELLOW   = "#cbdd56"   # lime — EW bar, donut accent
C_NEUTRAL  = "#6B7B6E"   # muted grey-green text
C_BORDER   = "#E5E7EB"   # light grey border
C_BG       = "#FFFFFF"   # white background
C_TEXT     = "#1F2937"   # dark text
C_MUTED    = "#6B7280"   # muted label text
C_UP       = "#16A34A"   # financial green (positive delta)
C_DOWN     = "#DC2626"   # financial red  (negative delta)
C_CARD_BG  = "#F9FAFB"   # card background

DONUT_COLORS = [C_BRAND, "#4CAF50", "#95bc26", C_YELLOW, "#A8D5A2", "#D4EDDA", C_MUTED, "#2D6A4F", "#52B788", "#B7E4C7", "#40916C", "#74C69D"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

/* General safe font application */
html, body, [class*="st-"], .stMarkdown, .stText {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Strictly protect Material Symbols */
.material-symbols-rounded, [data-testid="stIconMaterial"], .stIcon, i, svg {{
    font-family: 'Material Symbols Rounded' !important;
}}

/* ── Main layout ── */
.block-container {{ padding: 2rem 2rem 1rem 2rem !important; max-width: 100% !important; }}

/* ── Sidebar ── */
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

/* ── Multiselect tags ── */
span[data-baseweb="tag"] {{ background-color: {C_TAG} !important; border-radius: 4px !important; padding: 1px 8px !important; }}
span[data-baseweb="tag"] span {{ color: #fff !important; font-size: 12px !important; font-weight: 600 !important; }}

/* ── KPI Cards ── */
.kpi-wrap {{
    background: {C_CARD_BG}; border: 1px solid {C_BORDER}; border-radius: 8px; padding: 14px 16px 12px; min-height: 96px;
}}
.kpi-label {{ font-size: 11px; font-weight: 600; color: {C_MUTED}; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }}
.kpi-value {{ font-size: 28px; font-weight: 700; color: {C_TEXT}; line-height: 1.15; letter-spacing: -0.5px; }}
.kpi-delta {{ font-size: 12px; font-weight: 600; margin-top: 5px; display: flex; align-items: center; gap: 3px; }}
.kpi-delta.good  {{ color: {C_UP}; }}
.kpi-delta.bad   {{ color: {C_DOWN}; }}
.kpi-delta.neut  {{ color: {C_MUTED}; }}

/* ── Section header ── */
.sec-hdr {{
    font-size: 13px; font-weight: 700; color: {C_TEXT}; text-transform: uppercase; letter-spacing: 0.05em;
    padding-bottom: 6px; border-bottom: 2px solid {C_BRAND}; margin-bottom: 12px; display: inline-block;
}}

/* ── Page title row ── */
.page-title {{ font-size: 26px; font-weight: 700; color: {C_TEXT}; margin: 0; padding: 0; letter-spacing: -0.5px; text-transform: uppercase; }}
.header-glossary {{ font-size: 13px; color: {C_MUTED}; margin-top: 6px; line-height: 1.6; }}

/* ── Force DataFrame Header Alignment to Center ── */
div[data-testid="stDataFrame"] *[role="columnheader"] > div {{
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
}}

div[data-testid="stDataFrame"] *[role="columnheader"] .st-emotion-cache-1wmy9hl {{
    /* Đảm bảo text không bị lệch do icon sort mặc định của Streamlit */
    margin-left: auto;
    margin-right: auto;
}}

hr {{ margin: 12px 0 20px !important; border-color: {C_BORDER} !important; }}

/* Footer */
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
        <div style="font-size: 14px; color: {C_MUTED}; margin-top: 4px; display: flex; align-items: flex-start; gap: 6px;">
            <div style="margin-top: -2px; font-size: 14px;">🗂</div>
            <div style="line-height: 1.4;">
                {L['data_scope1']}<br>
                <span style="font-size: 12px; opacity: 0.85;">{L['data_scope2'].format(mm_yyyy=mm_yyyy)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception: pass

    st.markdown(f"<div style='font-size:11px;font-weight:700;color:{C_BRAND};text-transform:uppercase;letter-spacing:.05em;margin:16px 0 6px'>{L['model']}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size: 14px; color: {C_MUTED}; line-height: 1.8;">
        Minimum Variance Portfolio<br>
        Markowitz (1952)<br>
        {L['solver']}<br>
        <div style="line-height: 1.4; margin-top: 4px;">
            <span style="color: {C_TEXT}; font-weight: 500;">{L['rf_main']}</span><br>
            <span style="font-size: 12px; opacity: 0.85;">{L['rf_sub']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Header row ────────────────────────────────────────────────────────────────
c_title, c_space, c_pdf, c_excel = st.columns([5, 2, 1.5, 1.5])

with c_title:
    st.markdown(f"<h1 class='page-title'>{L['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-glossary'>{L['glossary']}</div>", unsafe_allow_html=True)

with c_pdf:
    st.button(f"📄 {L['exp_pdf']}", use_container_width=True) 

st.markdown("<hr>", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if len(selected) < 2:
    st.warning(L['warn2'])
    st.stop()

# ── Optimizer ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def run_optimizer(tickers_tuple): return min_variance_portfolio(list(tickers_tuple))

with st.spinner(L['spinning']):
    try: result = run_optimizer(tuple(sorted(selected)))
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()

N = len(selected)
w_eq = np.array([1.0 / N] * N)
mu = result['mu']
cov = result['cov']
eq_stats = portfolio_stats(w_eq, mu, cov)
std_arr = np.sqrt(np.diag(cov.values))

# ── Excel export logic ───────────────────────
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine='openpyxl') as writer:
    alloc_tmp = pd.DataFrame({
        L['col_ticker']: selected, L['col_mvp']: [f"{w:.1%}" for w in result['weights']],
        L['col_ew']: [f"{w:.1%}" for w in w_eq], L['col_ret']: [f"{r:.1%}" for r in mu.values],
        L['col_vol']: [f"{v:.1%}" for v in std_arr]
    }).sort_values(L['col_mvp'], ascending=False)
    alloc_tmp.to_excel(writer, sheet_name='Allocation', index=False)
buf.seek(0)

with c_excel:
    st.download_button(label=f"📊 {L['exp_xlsx']}", data=buf, file_name="portfolio_optimization.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
def kpi(label, val, delta, pct=True, decimals=2, invert=False):
    fmt = f"{{:.{decimals}%}}" if pct else f"{{:.{decimals}f}}"
    v_str, d_str = fmt.format(val), (f"+{fmt.format(delta)}" if delta >= 0 else fmt.format(delta))
    arrow = "▲" if delta > 0 else "▼" if delta < 0 else "—"
    css = ("good" if delta < 0 else "bad") if invert else ("good" if delta > 0 else "bad")
    if delta == 0: css = "neut"
    return f"<div class='kpi-wrap'><div class='kpi-label'>{label}</div><div class='kpi-value'>{v_str}</div><div class='kpi-delta {css}'>{arrow} {d_str} {L['vs_ew']}</div></div>"

c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi(L['kpi_ret'], result['port_return'], result['port_return'] - eq_stats['port_return']), unsafe_allow_html=True)
c2.markdown(kpi(L['kpi_vol'], result['port_volatility'], result['port_volatility'] - eq_stats['port_volatility'], invert=True), unsafe_allow_html=True)
c3.markdown(kpi(L['kpi_sharpe'], result['sharpe_ratio'], result['sharpe_ratio'] - eq_stats['sharpe_ratio'], pct=False, decimals=3), unsafe_allow_html=True)
c4.markdown(f"<div class='kpi-wrap'><div class='kpi-label'>{L['kpi_active']}</div><div class='kpi-value'>{int((result['weights'] > 0.001).sum())} / {N}</div><div class='kpi-delta good'>▼ {L['vol_red']} {result['improvement_pct']:.1f}%</div></div>", unsafe_allow_html=True)

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
        labels=labels, 
        values=vals, 
        hole=0.45, 
        textinfo='label+percent',
        textposition='outside',
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2))
    ))
    
    fig_pie.update_layout(
        uniformtext_minsize=11, 
        uniformtext_mode='hide', 
        legend=dict(orientation='v', x=1.2, y=0.5, font=dict(size=12)), 
        margin=dict(t=20, b=20, l=40, r=140),
        height=320, 
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Tỷ trọng: %{percent:.1%}<extra></extra>')
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

with col_bar:
    st.markdown(f"<div class='sec-hdr'>{L['sec_cmp']}</div>", unsafe_allow_html=True)
    fig_bar = go.Figure()
    m_labels = [L['kpi_ret'], L['kpi_vol'], L['kpi_sharpe']]
    m_vals, e_vals = [result['port_return'], result['port_volatility'], result['sharpe_ratio']], [eq_stats['port_return'], eq_stats['port_volatility'], eq_stats['sharpe_ratio']]
    
    fig_bar.add_trace(go.Bar(name=L['mvp_lbl'], x=m_labels, y=m_vals, marker_color=C_BRAND, text=[f"{v:.1%}" if i<2 else f"{v:.3f}" for i,v in enumerate(m_vals)], textposition='outside'))
    fig_bar.add_trace(go.Bar(name=L['ew_lbl'], x=m_labels, y=e_vals, marker_color='#E5E7EB', text=[f"{v:.1%}" if i<2 else f"{v:.3f}" for i,v in enumerate(e_vals)], textposition='outside'))
    fig_bar.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), height=320, legend=dict(orientation='h', y=-0.15), yaxis=dict(visible=False, range=[0, max(max(m_vals), max(e_vals)) * 1.3]), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# ── Heatmap ───────────────────────────────────────────────────────────────────
st.markdown(f"<div style='margin-top:12px'><div class='sec-hdr'>{L['sec_heat']}</div></div>", unsafe_allow_html=True)
corr_df = pd.DataFrame((cov.values / np.outer(std_arr, std_arr)).round(2), index=selected, columns=selected)
heat_scale = [[0.0, C_BRAND], [0.3, "#52B788"], [0.55, "#FFE08A"], [0.75, "#FFA04A"], [1.0, "#DC2626"]]

fig_heat = go.Figure(go.Heatmap(z=corr_df.values, x=selected, y=selected, colorscale=heat_scale, zmin=-0.2, zmax=1.0, text=corr_df.values, texttemplate='%{text:.2f}'))
fig_heat.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=max(250, 24 * len(selected)), xaxis=dict(tickangle=-45), yaxis=dict(autorange='reversed'), paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})

# ── Allocation Table ──────────────────────────────────────────────────────────
st.markdown(f"<div style='margin-top:12px'><div class='sec-hdr'>{L['sec_tbl']}</div></div>", unsafe_allow_html=True)

alloc_disp = pd.DataFrame({
    L['col_ticker']: selected, 
    L['col_mvp']: result['weights'] * 100,
    L['col_ew']: w_eq * 100, 
    L['col_ret']: mu.values * 100,
    L['col_vol']: std_arr * 100
}).sort_values(L['col_mvp'], ascending=False).reset_index(drop=True)

st.dataframe(
    alloc_disp,
    use_container_width=True,
    hide_index=True,
    column_config={
        L['col_ticker']: st.column_config.TextColumn(L['col_ticker'], alignment="center"),
        L['col_mvp']: st.column_config.NumberColumn(L['col_mvp'], format="%.1f%%", alignment="center"),
        L['col_ew']: st.column_config.NumberColumn(L['col_ew'], format="%.1f%%", alignment="center"),
        L['col_ret']: st.column_config.NumberColumn(L['col_ret'], format="%.1f%%", alignment="center"),
        L['col_vol']: st.column_config.NumberColumn(L['col_vol'], format="%.1f%%", alignment="center")
    }
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"<div class='footer'>{L['footer']}</div>", unsafe_allow_html=True)