import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from html import escape

st.set_page_config(page_title="NetSage AI", page_icon="🛰️", layout="wide")

# ================= CUSTOM STYLING =================
st.markdown("""
<style>
    :root {
        --bg: #070b14;
        --panel: #0d1421;
        --panel2: #111b2c;
        --line: rgba(148,163,184,.13);
        --blue: #60a5fa;
        --cyan: #38bdf8;
        --green: #4ade80;
        --amber: #fbbf24;
        --red: #fb7185;
        --text: #f8fafc;
        --muted: #8b9bb0;
    }

    .stApp {
        background:
            radial-gradient(circle at 78% 0%, rgba(37,99,235,.11), transparent 28%),
            radial-gradient(circle at 5% 25%, rgba(14,165,233,.055), transparent 23%),
            var(--bg);
    }

    [data-testid="stHeader"] { background: transparent; }
    .main .block-container {
        max-width: 1480px;
        padding: 1.8rem 2.6rem 3.5rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#08101b,#060b12);
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #9aa9bc;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 5px; }

    .topbar {
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom: 18px;
    }
    .eyebrow {
        color:#6ea9e8;
        font-size:10px;
        font-weight:800;
        letter-spacing:.17em;
        text-transform:uppercase;
    }
    .live-pill {
        display:inline-flex;
        align-items:center;
        gap:7px;
        padding:7px 11px;
        border:1px solid rgba(74,222,128,.16);
        background:rgba(74,222,128,.045);
        border-radius:999px;
        color:#a9ddb5;
        font-size:10px;
        font-weight:700;
    }
    .live-dot {
        width:7px;height:7px;border-radius:50%;
        background:#4ade80;
        box-shadow:0 0 12px rgba(74,222,128,.9);
    }

    .hero-noc {
        position:relative;
        overflow:hidden;
        min-height:330px;
        border-radius:24px;
        border:1px solid rgba(96,165,250,.20);
        background:
            radial-gradient(circle at 87% 22%, rgba(59,130,246,.26), transparent 24%),
            radial-gradient(circle at 58% 105%, rgba(56,189,248,.08), transparent 28%),
            linear-gradient(135deg,#142542 0%,#0e1a2c 48%,#09111d 100%);
        box-shadow:0 25px 65px rgba(0,0,0,.28);
        padding:38px 42px;
        margin-bottom:18px;
    }
    .hero-noc:before {
        content:"";
        position:absolute;
        width:430px;height:430px;
        right:-210px;top:-270px;
        border:1px solid rgba(147,197,253,.11);
        border-radius:50%;
        box-shadow:0 0 0 55px rgba(147,197,253,.025),0 0 0 110px rgba(147,197,253,.018);
    }
    .hero-grid {
        display:grid;
        grid-template-columns:minmax(0,1.45fr) minmax(300px,.75fr);
        gap:30px;
        align-items:center;
    }
    .hero-noc h1 {
        margin:9px 0 13px;
        color:#fff;
        font-size:3rem;
        line-height:1.02;
        letter-spacing:-.055em;
    }
    .hero-noc h1 span { color:#71b4fa; }
    .hero-noc p {
        max-width:690px;
        margin:0;
        color:#b2c0d2;
        font-size:14px;
        line-height:1.72;
    }
    .hero-actions {
        display:flex;
        gap:9px;
        margin-top:22px;
        flex-wrap:wrap;
    }
    .hero-action {
        padding:8px 12px;
        border-radius:8px;
        background:rgba(255,255,255,.045);
        border:1px solid rgba(255,255,255,.08);
        color:#b9c7d8;
        font-size:10px;
        font-weight:700;
    }

    .health-wrap {
        display:flex;
        justify-content:center;
        align-items:center;
        min-height:225px;
    }
    .health-ring {
        width:178px;height:178px;border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        background:conic-gradient(#60a5fa 0 94%, rgba(96,165,250,.09) 94% 100%);
        box-shadow:0 0 60px rgba(37,99,235,.16);
        position:relative;
    }
    .health-ring:after {
        content:"";
        position:absolute;inset:11px;
        border-radius:50%;
        background:#0c1727;
        border:1px solid rgba(147,197,253,.11);
    }
    .health-inner { position:relative;z-index:2;text-align:center; }
    .health-value { color:#fff;font-size:39px;font-weight:800;letter-spacing:-.05em; }
    .health-label { color:#8495ab;font-size:9px;font-weight:800;letter-spacing:.13em; }
    .health-status { color:#86d99d;font-size:10px;font-weight:700;margin-top:4px; }

    .kpi-grid {
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:10px;
        margin-bottom:18px;
    }
    .kpi-card {
        padding:15px 17px;
        border:1px solid var(--line);
        border-radius:13px;
        background:linear-gradient(145deg,#101927,#0b121c);
    }
    .kpi-label { color:#63738a;font-size:9px;font-weight:800;letter-spacing:.13em; }
    .kpi-value { color:#f8fafc;font-size:23px;font-weight:800;margin-top:5px; }
    .kpi-sub { color:#6f7f94;font-size:9px;margin-top:2px; }
    .trend-up { color:#6ed58c;font-weight:700; }

    .mini-flash {
        position: relative;
        overflow: hidden;
        min-height: 190px;
        padding: 24px 20px;
        border-radius: 20px;
        background:
            radial-gradient(circle at 100% 0%, rgba(59,130,246,0.18), transparent 35%),
            linear-gradient(145deg, #101b32, #0c1424);
        border: 1px solid rgba(96,165,250,0.18);
        box-shadow: 0 14px 40px rgba(0,0,0,0.22);
        margin-bottom: 14px;
    }
    .mini-flash:hover {
        border-color:rgba(96,165,250,.38);
        box-shadow:0 18px 44px rgba(37,99,235,.13);
    }
    .mini-flash-icon { font-size:34px; margin-bottom:10px; }
    .mini-flash-title { color:#f8fafc; font-size:18px; font-weight:800; }
    .mini-flash-text { color:#94a3b8; font-size:12.5px; line-height:1.6; margin-top:8px; }
    .mini-flash-tag {
        display:inline-block;margin-top:14px;padding:5px 8px;border-radius:999px;
        color:#8ec5fa;background:rgba(59,130,246,.08);
        border:1px solid rgba(96,165,250,.12);font-size:9px;font-weight:800;
    }

    .section-title {
        color:#f3f6fb;
        font-size:20px;
        font-weight:800;
        letter-spacing:-.025em;
        margin:3px 0 5px;
    }
    .section-copy {
        color:#718197;
        font-size:11px;
        line-height:1.55;
        margin-bottom:15px;
    }

    .workspace {
        padding:21px;
        border-radius:17px;
        border:1px solid var(--line);
        background:linear-gradient(145deg,#0f1826,#0a111a);
        box-shadow:0 14px 38px rgba(0,0,0,.17);
    }
    .workspace-head {
        display:flex;align-items:center;justify-content:space-between;
        gap:10px;margin-bottom:15px;
    }
    .workspace-number {
        color:#344359;font-size:10px;font-weight:800;letter-spacing:.13em;
    }
    .input-caption {
        color:#6c7c91;font-size:9px;font-weight:800;letter-spacing:.1em;
        text-transform:uppercase;margin:3px 0 6px;
    }

    div[data-baseweb="select"] > div,
    div[data-testid="stTextArea"] textarea {
        background:#0a111b !important;
        color:#dbe5f1 !important;
        border:1px solid rgba(148,163,184,.13) !important;
        border-radius:10px !important;
    }
    div[data-testid="stTextArea"] textarea { min-height:120px; }
    .stButton > button {
        border-radius:10px;
        min-height:44px;
        font-weight:800;
        border:1px solid rgba(96,165,250,.24);
    }
    .stButton > button:hover {
        border-color:rgba(96,165,250,.55);
        box-shadow:0 10px 28px rgba(37,99,235,.16);
    }

    .domain-panel {
        padding:21px;
        border-radius:17px;
        border:1px solid var(--line);
        background:linear-gradient(145deg,#0f1826,#0a111a);
        min-height:100%;
    }
    .domain-item {
        display:flex;align-items:center;gap:10px;
        padding:9px 8px;margin:5px 0;border-radius:9px;
        border:1px solid rgba(148,163,184,.06);
        background:rgba(255,255,255,.015);
    }
    .domain-icon {
        width:30px;height:30px;border-radius:8px;
        display:flex;align-items:center;justify-content:center;
        color:#83bdf3;background:rgba(59,130,246,.09);
        font-weight:800;font-size:12px;
    }
    .domain-name { color:#d8e1ec;font-size:11px;font-weight:700; }
    .domain-count { margin-left:auto;color:#5f6f83;font-size:9px; }

    .stream-panel {
        padding:20px;
        border-radius:17px;
        border:1px solid var(--line);
        background:linear-gradient(145deg,#0f1826,#0a111a);
    }
    .incident {
        display:grid;grid-template-columns:8px 1fr auto;
        gap:11px;align-items:center;
        padding:11px 0;
        border-bottom:1px solid rgba(148,163,184,.07);
    }
    .incident:last-child { border-bottom:0; }
    .severity { width:7px;height:34px;border-radius:5px; }
    .sev-high { background:#fb7185;box-shadow:0 0 10px rgba(251,113,133,.22); }
    .sev-med { background:#fbbf24; }
    .sev-low { background:#4ade80; }
    .incident-title { color:#dce5ef;font-size:10px;font-weight:700; }
    .incident-meta { color:#64748a;font-size:8px;margin-top:3px; }
    .incident-status {
        color:#7edb99;background:rgba(74,222,128,.055);
        border:1px solid rgba(74,222,128,.12);
        padding:4px 7px;border-radius:999px;font-size:8px;font-weight:800;
    }

    .result-card {
        background:linear-gradient(145deg,#101d30,#0a131f);
        border:1px solid rgba(96,165,250,.22);
        border-radius:17px;
        padding:21px 23px;
        margin-top:16px;
        box-shadow:0 18px 40px rgba(0,0,0,.22);
    }
    .badge {
        display:inline-block;padding:5px 10px;border-radius:999px;
        font-size:9px;font-weight:800;margin-right:6px;
    }
    .badge-cat { background:rgba(59,130,246,.14);color:#9dcbfa;border:1px solid rgba(96,165,250,.18); }
    .badge-conf { background:rgba(74,222,128,.08);color:#9cddb0;border:1px solid rgba(74,222,128,.14); }
    .result-card h4 { color:#f5f8fc; }
    .result-card p { color:#9aa9bb; font-size:11px; line-height:1.6; }

    .review-card {
        display:flex;gap:10px;align-items:flex-start;
        padding:12px 14px;margin-top:9px;
        border-radius:11px;background:rgba(74,222,128,.035);
        border:1px solid rgba(74,222,128,.10);
        color:#718197;font-size:9px;line-height:1.5;
    }
    .review-icon {
        min-width:21px;height:21px;border-radius:50%;
        display:flex;align-items:center;justify-content:center;
        background:rgba(74,222,128,.10);color:#76d994;font-weight:800;
    }

    .footer-note {
        text-align:center;color:#4f5f73;font-size:9px;
        margin-top:40px;padding-top:15px;border-top:1px solid var(--line);
    }

    @media (max-width: 900px) {
        .hero-grid,.kpi-grid { grid-template-columns:1fr; }
        .hero-noc { padding:28px; }
        .hero-noc h1 { font-size:2.25rem; }
    }
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_data
def load_cases():
    return pd.read_csv("dataset/cases.csv")

df = load_cases()

def find_col(keywords):
    for kw in keywords:
        for col in df.columns:
            if kw in col.lower():
                return col
    return None

COL_ID = find_col(["case_id", "id"])
COL_CATEGORY = find_col(["category"])
COL_DIFFICULTY = find_col(["difficulty"])
COL_SYMPTOM = find_col(["symptom"])
COL_ROOT_CAUSE = find_col(["root_cause"])
COL_FIX = find_col(["fix"])

# Debug column details intentionally hidden from the presentation UI.

# ================= RULE-BASED CHECKER =================
CATEGORY_KEYWORDS = {
    "VLAN": ["vlan", "trunk", "switchport", "svi", "native vlan"],
    "DHCP": ["dhcp", "ip address", "lease", "apipa", "169.254", "helper-address"],
    "DNS": ["dns", "resolve", "hostname", "nslookup", "name-server"],
    "ACL": ["acl", "access-list", "blocked", "denied", "access-group"],
    "NAT": ["nat", "overload", "translation", "public ip", "inside global"],
    "Routing": ["route", "ospf", "routing", "neighbor", "next-hop", "gateway"],
    "Wireless": ["wireless", "wifi", "ssid", "wpa", "ap ", "access point", "channel"],
}

def predict_category(symptom_text):
    text = str(symptom_text).lower()
    scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in CATEGORY_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Mixed/Unknown"

def diagnose(symptom_text):
    predicted_category = predict_category(symptom_text)
    matches = df[df[COL_CATEGORY] == predicted_category] if COL_CATEGORY else pd.DataFrame()
    if matches.empty:
        return {"predicted_category": predicted_category, "closest_case": None,
                "root_cause": "No close match found — needs human review.",
                "fix": "N/A", "confidence": "Low"}
    case = matches.iloc[0]
    return {
        "predicted_category": predicted_category,
        "closest_case": case[COL_ID] if COL_ID else "N/A",
        "root_cause": case[COL_ROOT_CAUSE] if COL_ROOT_CAUSE else "N/A",
        "fix": case[COL_FIX] if COL_FIX else "N/A",
        "confidence": "Medium",
    }

# ================= SIDEBAR NAV =================
st.sidebar.markdown("""
<div style="padding:4px 2px 17px;">
    <div style="font-size:26px;">🛰️</div>
    <div style="font-size:18px;font-weight:800;color:#f8fafc;margin-top:3px;">NetSage AI</div>
    <div style="font-size:9px;color:#5f7086;letter-spacing:.14em;margin-top:2px;">NETWORK INTELLIGENCE</div>
</div>
""", unsafe_allow_html=True)
page = st.sidebar.radio("GO TO", ["🩺 Diagnose", "📊 Dashboard", "📋 Responsible AI Log", "ℹ️ About"])
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding:12px;border-radius:11px;background:rgba(74,222,128,.035);
            border:1px solid rgba(74,222,128,.10);">
    <div style="font-size:9px;color:#65768b;letter-spacing:.11em;font-weight:800;">SYSTEM STATUS</div>
    <div style="font-size:11px;color:#9ed8ad;font-weight:700;margin-top:5px;">● Operational</div>
    <div style="font-size:9px;color:#627288;margin-top:3px;">Human review enabled</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
st.sidebar.caption("Cisco–AICTE VIP 2026 Project")
st.sidebar.caption(f"Dataset: {len(df)} cases loaded")

# ================= PAGE: DIAGNOSE =================
if page == "🩺 Diagnose":

    # Presentation-ready NOC hero
    st.markdown("""
    <div class="topbar">
        <div>
            <div class="eyebrow">NETSAGE AI • NETWORK OPERATIONS CENTER</div>
        </div>
        <div class="live-pill"><span class="live-dot"></span> SYSTEM OPERATIONAL</div>
    </div>

    <div class="hero-noc">
        <div class="hero-grid">
            <div>
                <div class="eyebrow">AI-ASSISTED INCIDENT TRIAGE</div>
                <h1>Your network.<br><span>Diagnosed intelligently.</span></h1>
                <p>
                    Describe what is happening across your infrastructure and NetSage AI
                    will identify the most likely fault domain, connect it to a known
                    troubleshooting scenario, and surface the next action for an engineer
                    to verify.
                </p>
                <div class="hero-actions">
                    <div class="hero-action">✦ AI-assisted analysis</div>
                    <div class="hero-action">✓ Human approval required</div>
                    <div class="hero-action">◉ 7 fault domains</div>
                </div>
            </div>
            <div class="health-wrap">
                <div class="health-ring">
                    <div class="health-inner">
                        <div class="health-value">94%</div>
                        <div class="health-label">NETWORK HEALTH</div>
                        <div class="health-status">● STABLE</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI strip
    top_issue = (
        str(df[COL_CATEGORY].mode().iloc[0])
        if COL_CATEGORY and not df.empty and not df[COL_CATEGORY].dropna().empty
        else "N/A"
    )
    domains = df[COL_CATEGORY].nunique() if COL_CATEGORY and not df.empty else 0

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">CASE BANK</div>
                <div class="kpi-value">{len(df)}</div>
                <div class="kpi-sub"><span class="trend-up">● Ready</span> troubleshooting scenarios</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">NETWORK DOMAINS</div>
                <div class="kpi-value">{domains}</div>
                <div class="kpi-sub">VLAN • DHCP • DNS • ACL • NAT • Routing • Wi-Fi</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">TOP SIGNAL</div>
                <div class="kpi-value" style="font-size:19px;">{escape(top_issue)}</div>
                <div class="kpi-sub">Most represented fault domain</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">SAFETY MODE</div>
                <div class="kpi-value" style="font-size:19px;">HUMAN-IN-LOOP</div>
                <div class="kpi-sub"><span class="trend-up">✓ Enabled</span> no automatic device changes</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Exact mini-flash visual treatment requested
    f1, f2, f3, f4 = st.columns(4, gap="small")
    flashcards = [
        ("🧠", "AI Triage", "Turn a plain-language network symptom into a focused fault-domain hypothesis.", "SMART ANALYSIS"),
        ("⚡", "Rapid Diagnosis", "Start from a known case pattern instead of searching through incidents manually.", "FAST RESPONSE"),
        ("🛡️", "Human Control", "Every recommendation remains a decision-support signal for a network engineer.", "SAFE BY DESIGN"),
        ("📋", "Full Traceability", "Wrong predictions stay visible so performance can be reviewed and corrected.", "AUDIT READY"),
    ]
    for col, (icon, title, desc, tag) in zip([f1, f2, f3, f4], flashcards):
        with col:
            st.markdown(
                f"""
                <div class="mini-flash">
                    <div class="mini-flash-icon">{icon}</div>
                    <div class="mini-flash-title">{title}</div>
                    <div class="mini-flash-text">{desc}</div>
                    <div class="mini-flash-tag">{tag}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="eyebrow">INCIDENT WORKSPACE</div>
        <div class="section-title">Diagnose a live-style network symptom</div>
        <div class="section-copy">
            Use a realistic case from the dataset for your demo, or describe your own incident.
            The result is always a recommendation — not an automatic configuration change.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.55, .85], gap="large")

    with left:
        st.markdown(
            """
            <div class="workspace">
                <div class="workspace-head">
                    <div>
                        <div class="eyebrow">01 • INCIDENT INTAKE</div>
                        <div style="color:#e9eef5;font-size:15px;font-weight:800;margin-top:3px;">
                            What is the network doing?
                        </div>
                    </div>
                    <div class="workspace-number">INPUT → ANALYZE</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        if COL_SYMPTOM is None:
            st.error("Couldn't find a symptom column in your CSV.")
            symptom_input = ""
        else:
            sample = st.selectbox(
                "Pick a known incident or create a new one",
                ["＋ Describe a new incident"] + df[COL_SYMPTOM].dropna().astype(str).tolist(),
                label_visibility="collapsed",
            )

            if sample == "＋ Describe a new incident":
                symptom_input = st.text_area(
                    "Network symptom",
                    height=125,
                    placeholder=(
                        "Example: Two PCs in the same VLAN cannot ping each other, "
                        "although both have valid IP addresses."
                    ),
                    label_visibility="collapsed",
                )
            else:
                symptom_input = sample
                st.text_area(
                    "Selected incident",
                    value=symptom_input,
                    height=125,
                    disabled=True,
                    label_visibility="collapsed",
                )

        meta1, meta2 = st.columns(2)
        with meta1:
            severity = st.selectbox(
                "Severity",
                ["Medium", "High", "Critical", "Low"],
                index=0,
            )
        with meta2:
            environment = st.selectbox(
                "Environment",
                ["Campus LAN", "Data Center", "Branch Office", "Wireless", "Hybrid"],
            )

        st.markdown(
            '<div class="input-caption">Analysis mode</div>',
            unsafe_allow_html=True,
        )
        mode = st.radio(
            "Analysis mode",
            ["Case-bank match", "Strict human review"],
            horizontal=True,
            label_visibility="collapsed",
        )

        analyze = st.button(
            "⚡  ANALYZE INCIDENT",
            type="primary",
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        if analyze:
            if not symptom_input.strip():
                st.warning("Please enter or select a network symptom first.")
            else:
                result = diagnose(symptom_input)
                confidence = result["confidence"]

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div style="display:flex;justify-content:space-between;gap:10px;align-items:flex-start;">
                            <div>
                                <div class="eyebrow">02 • ANALYSIS RESULT</div>
                                <h4 style="font-size:20px;margin:6px 0 0;">
                                    {escape(str(result["predicted_category"]))} fault signal detected
                                </h4>
                            </div>
                            <div>
                                <span class="badge badge-cat">{escape(str(result["predicted_category"]))}</span>
                                <span class="badge badge-conf">{escape(str(confidence))} confidence</span>
                            </div>
                        </div>

                        <div style="height:1px;background:rgba(148,163,184,.10);margin:17px 0;"></div>

                        <div style="display:grid;grid-template-columns:.8fr 1.4fr;gap:22px;">
                            <div>
                                <div class="input-caption">CLOSEST KNOWN CASE</div>
                                <div style="color:#dce5ef;font-size:12px;font-weight:700;">
                                    {escape(str(result["closest_case"]))}
                                </div>
                                <div style="margin-top:14px;" class="input-caption">INCIDENT CONTEXT</div>
                                <div style="color:#8392a7;font-size:10px;">
                                    {escape(str(severity))} severity • {escape(str(environment))}
                                </div>
                            </div>
                            <div>
                                <div class="input-caption">LIKELY ROOT CAUSE</div>
                                <div style="color:#b9c7d8;font-size:11px;line-height:1.6;">
                                    {escape(str(result["root_cause"]))}
                                </div>
                            </div>
                        </div>

                        <div style="margin-top:16px;padding:13px;border-radius:10px;
                                    background:rgba(59,130,246,.055);
                                    border:1px solid rgba(96,165,250,.11);">
                            <div class="input-caption">RECOMMENDED NEXT ACTION</div>
                            <div style="color:#c5d2e0;font-size:11px;line-height:1.6;">
                                {escape(str(result["fix"]))}
                            </div>
                        </div>
                    </div>

                    <div class="review-card">
                        <span class="review-icon">✓</span>
                        <div>
                            <b style="color:#a4ddb1;">Human review checkpoint</b><br>
                            Verify the evidence, root cause, and recommended fix before changing
                            any live network device. Analysis mode: {escape(str(mode))}.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with right:
        st.markdown(
            """
            <div class="domain-panel">
                <div class="eyebrow">03 • FAULT COVERAGE</div>
                <div class="section-title" style="font-size:17px;">Network domains</div>
                <div class="section-copy">
                    The checker scans the incident against these infrastructure fault patterns.
                </div>
            """,
            unsafe_allow_html=True,
        )

        icons = {"VLAN":"◈","DHCP":"⌁","DNS":"◎","ACL":"◉","NAT":"⇄","Routing":"↝","Wireless":"◌"}
        for cat, icon in icons.items():
            if COL_CATEGORY and not df.empty:
                count = int(df[COL_CATEGORY].astype(str).str.lower().eq(cat.lower()).sum())
            else:
                count = 0
            st.markdown(
                f"""
                <div class="domain-item">
                    <div class="domain-icon">{icon}</div>
                    <div class="domain-name">{cat}</div>
                    <div class="domain-count">{count} cases</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="margin-top:14px;padding:12px;border-radius:10px;
                        background:rgba(59,130,246,.045);
                        border:1px solid rgba(96,165,250,.09);">
                <div class="input-caption">AI SAFETY STATUS</div>
                <div style="color:#9cc8f5;font-size:10px;font-weight:700;">
                    ● Recommendation only
                </div>
                <div style="color:#68788d;font-size:9px;line-height:1.5;margin-top:4px;">
                    No autonomous configuration changes are performed.
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Incident stream
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    s1, s2 = st.columns([1.15, .85], gap="large")

    with s1:
        st.markdown(
            """
            <div class="stream-panel">
                <div class="eyebrow">04 • OPERATIONS FEED</div>
                <div class="section-title" style="font-size:17px;">Recent incident patterns</div>
                <div class="section-copy">Representative cases available in the current troubleshooting bank.</div>
            """,
            unsafe_allow_html=True,
        )

        if COL_SYMPTOM and not df.empty:
            recent = df.head(4)
            for idx, row in recent.iterrows():
                category = str(row[COL_CATEGORY]) if COL_CATEGORY else "Network"
                symptom = str(row[COL_SYMPTOM])
                difficulty = str(row[COL_DIFFICULTY]) if COL_DIFFICULTY else "Review"
                sev_class = "sev-high" if str(difficulty).lower() == "hard" else ("sev-med" if str(difficulty).lower() == "medium" else "sev-low")
                st.markdown(
                    f"""
                    <div class="incident">
                        <div class="severity {sev_class}"></div>
                        <div>
                            <div class="incident-title">{escape(category)} • {escape(symptom[:78])}</div>
                            <div class="incident-meta">Case {escape(str(row[COL_ID]) if COL_ID else str(idx))} • {escape(difficulty)} complexity</div>
                        </div>
                        <div class="incident-status">READY</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown(
            """
            <div class="stream-panel">
                <div class="eyebrow">05 • SAFE OPERATIONS</div>
                <div class="section-title" style="font-size:17px;">Decision workflow</div>
                <div class="section-copy">
                    Designed for responsible AI in network operations.
                </div>
            """,
            unsafe_allow_html=True,
        )

        steps = [
            ("01", "Capture", "Engineer describes the observed symptom."),
            ("02", "Analyze", "NetSage identifies a likely fault pattern."),
            ("03", "Verify", "Engineer validates evidence and recommended action."),
            ("04", "Act", "Only the approved human operator changes infrastructure."),
        ]
        for number, title, desc in steps:
            st.markdown(
                f"""
                <div style="display:flex;gap:10px;padding:9px 0;border-bottom:1px solid rgba(148,163,184,.06);">
                    <div style="color:#4e6682;font-size:9px;font-weight:800;width:22px;">{number}</div>
                    <div>
                        <div style="color:#dce5ef;font-size:10px;font-weight:800;">{title}</div>
                        <div style="color:#68788d;font-size:9px;line-height:1.45;margin-top:2px;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE: DASHBOARD =================

elif page == "📊 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard</h1>
        <p>Overview of the case bank and how reliably the AI checker matches known issues.</p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="result-card" style="text-align:center;">
            <div style="font-size:13px;color:#888;">TOTAL CASES</div>
            <div style="font-size:32px;font-weight:700;color:#2c5aa0;">{len(df)}</div></div>""", unsafe_allow_html=True)
    with k2:
        val = df[COL_CATEGORY].nunique() if COL_CATEGORY else "N/A"
        st.markdown(f"""<div class="result-card" style="text-align:center;">
            <div style="font-size:13px;color:#888;">CATEGORIES</div>
            <div style="font-size:32px;font-weight:700;color:#2c5aa0;">{val}</div></div>""", unsafe_allow_html=True)
    with k3:
        val = df[COL_DIFFICULTY].mode()[0] if COL_DIFFICULTY else "N/A"
        st.markdown(f"""<div class="result-card" style="text-align:center;">
            <div style="font-size:13px;color:#888;">TOP DIFFICULTY</div>
            <div style="font-size:24px;font-weight:700;color:#2c5aa0;">{val}</div></div>""", unsafe_allow_html=True)
    with k4:
        val = df[COL_CATEGORY].mode()[0] if COL_CATEGORY else "N/A"
        st.markdown(f"""<div class="result-card" style="text-align:center;">
            <div style="font-size:13px;color:#888;">TOP ISSUE TYPE</div>
            <div style="font-size:24px;font-weight:700;color:#2c5aa0;">{val}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if COL_CATEGORY:
            st.subheader("Issue Types Breakdown")
            counts = df[COL_CATEGORY].value_counts().reset_index()
            counts.columns = ["Category", "Count"]
            fig = px.pie(counts, names="Category", values="Count", hole=0.55,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340,
                               paper_bgcolor="rgba(0,0,0,0)", font_color="#ddd",
                               legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if COL_DIFFICULTY:
            st.subheader("Difficulty Breakdown")
            counts = df[COL_DIFFICULTY].value_counts().reset_index()
            counts.columns = ["Difficulty", "Count"]
            fig = px.bar(counts, x="Difficulty", y="Count", color="Difficulty",
                         color_discrete_map={"Easy": "#3a6b35", "Medium": "#c98a1e", "Hard": "#a83232"})
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340, showlegend=False,
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#ddd")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    if COL_SYMPTOM and COL_CATEGORY:
        df["ai_predicted_category"] = df[COL_SYMPTOM].apply(predict_category)
        df["ai_correct"] = df["ai_predicted_category"] == df[COL_CATEGORY]
        agreement_rate = df["ai_correct"].mean() * 100

        g1, g2 = st.columns([1, 1.4])
        with g1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=agreement_rate,
                number={'suffix': "%", 'font': {'size': 40}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2c5aa0"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0, 50], 'color': "#3a1f1f"},
                        {'range': [50, 80], 'color': "#3a3319"},
                        {'range': [80, 100], 'color': "#1f3a24"}],
                }))
            fig.update_layout(height=260, margin=dict(t=30, b=10, l=30, r=30),
                               paper_bgcolor="rgba(0,0,0,0)", font_color="#ddd")
            st.plotly_chart(fig, use_container_width=True)
        with g2:
            st.markdown("### 🤖 AI Agreement Rate")
            st.markdown(f"""
            <div class="info-card">
            Out of <b>{len(df)} cases</b>, the rule-based checker's predicted category matched the
            ground-truth category <b>{df['ai_correct'].sum()} times</b> — a <b>{agreement_rate:.1f}%</b> agreement rate.
            This is the core transparency metric for the project: it shows how often the AI's first
            guess needs no human correction at all, and how often a human engineer had to step in.
            </div>
            """, unsafe_allow_html=True)

    if COL_CATEGORY and COL_DIFFICULTY:
        st.markdown("---")
        st.subheader("Case Complexity Spread")
        pivot = pd.crosstab(df[COL_CATEGORY], df[COL_DIFFICULTY])
        fig = px.imshow(pivot, text_auto=True, color_continuous_scale="Blues", aspect="auto")
        fig.update_layout(height=320, margin=dict(t=10, b=10, l=10, r=10),
                           paper_bgcolor="rgba(0,0,0,0)", font_color="#ddd")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("How difficulty is distributed across each issue category — useful for showing balanced test coverage.")

# ================= PAGE: RESPONSIBLE AI LOG =================
elif page == "📋 Responsible AI Log":
    st.markdown("""
    <div class="main-header">
        <h1>📋 Responsible AI Log</h1>
        <p>Transparency record of every case where the AI's suggestion needed human correction.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
    Responsible AI isn't just a feature here — it's the point. NetSage AI is designed to be
    <b>corrected, not trusted blindly</b>. This log exists so anyone reviewing the project can see
    exactly where the automated checker's first guess was wrong, and what the actual root cause was —
    proof that human review is a real part of the workflow, not a formality.
    </div>
    """, unsafe_allow_html=True)

    if COL_SYMPTOM and COL_CATEGORY:
        df["ai_predicted_category"] = df[COL_SYMPTOM].apply(predict_category)
        mismatches = df[df["ai_predicted_category"] != df[COL_CATEGORY]]

        c1, c2 = st.columns(2)
        c1.metric("Cases needing correction", f"{len(mismatches)} / {len(df)}")
        c2.metric("Correction rate", f"{(len(mismatches)/len(df)*100):.1f}%")

        st.subheader("Corrected Cases")
        cols_to_show = [c for c in [COL_ID, COL_CATEGORY, "ai_predicted_category", COL_ROOT_CAUSE] if c]
        display_df = mismatches[cols_to_show].rename(columns={
            COL_ID: "Case ID", COL_CATEGORY: "Actual Category",
            "ai_predicted_category": "AI Predicted", COL_ROOT_CAUSE: "Correct Root Cause"
        })
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("Missing symptom or category column — check the sidebar debug panel.")

# ================= PAGE: ABOUT =================
else:
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ About NetSage AI</h1>
        <p>An AI-assisted network troubleshooting tool built with mandatory human review.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 Project Goal
    NetSage AI helps network engineers triage common troubleshooting issues — VLAN, DHCP, DNS, ACL, NAT,
    Routing, and Wireless faults — by matching symptoms against a curated case bank and suggesting a likely
    root cause and fix. It's built for the **Cisco–AICTE Virtual Internship Program 2026**.

    ### 🧩 How It's Built
    | Component | What it does |
    |---|---|
    | **Case Bank** (`dataset/cases.csv`) | Real-world troubleshooting scenarios with ground-truth root causes and fixes |
    | **Rule-Based Checker** | Matches symptom text against category keywords to predict the likely fault type |
    | **Dashboard** | Visualizes issue-type distribution and measures AI agreement rate against ground truth |
    | **Responsible AI Log** | Tracks every case where the AI's guess was wrong, for full transparency |
    | **Packet Tracer Scenarios** | Hands-on `.pkt` labs matching each case, for practical verification |

    ### 🛡️ Responsible AI Principles
    - The AI **never applies a fix automatically** — every suggestion requires human sign-off.
    - Every prediction is logged, including wrong ones, so accuracy can be audited.
    - Confidence levels are shown alongside every suggestion so users know how much to trust it.

    ### 🛠️ Tech Stack
    Python · Streamlit · Pandas · Plotly · Cisco Packet Tracer

    ### 👥 Team
    Built as part of a team project — case bank & Packet Tracer scenarios, AI prompt design,
    rule-based checker, and dashboard were split across team members and integrated here.
    """)

# ================= FOOTER =================
st.markdown("""
<div class="footer-note">
    NetSage AI · Cisco–AICTE VIP 2026 · Built with human oversight at every step
</div>
""", unsafe_allow_html=True)
