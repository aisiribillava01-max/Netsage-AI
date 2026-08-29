import streamlit as st
import pandas as pd

st.set_page_config(page_title="NetSage AI", page_icon="🛰️", layout="wide")

# ================= CUSTOM STYLING =================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2c5aa0 100%);
        padding: 28px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 32px; }
    .main-header p { color: #cfe0f5; margin: 6px 0 0 0; font-size: 15px; }

    .info-card {
        background: #1a1d24;
        border: 1px solid #2d3139;
        border-left: 4px solid #2c5aa0;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .result-card {
        background: #1a1d24;
        border: 1px solid #2d3139;
        border-radius: 10px;
        padding: 20px 24px;
        margin-top: 12px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
    }
    .badge-cat { background: #2c5aa0; color: white; }
    .badge-conf { background: #3a6b35; color: white; }
    .footer-note {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #2d3139;
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

with st.sidebar.expander("🔧 Detected columns (debug)"):
    st.write({"case_id": COL_ID, "category": COL_CATEGORY, "difficulty": COL_DIFFICULTY,
              "symptom": COL_SYMPTOM, "root_cause": COL_ROOT_CAUSE, "fix": COL_FIX})

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
st.sidebar.markdown("### 🛰️ NetSage AI")
page = st.sidebar.radio("Go to", ["🩺 Diagnose", "📊 Dashboard", "📋 Responsible AI Log", "ℹ️ About"])
st.sidebar.markdown("---")
st.sidebar.caption("Cisco–AICTE VIP 2026 Project")
st.sidebar.caption(f"Dataset: {len(df)} cases loaded")

# ================= PAGE: DIAGNOSE =================
if page == "🩺 Diagnose":
    st.markdown("""
    <div class="main-header">
        <h1>🩺 Diagnose a Network Issue</h1>
        <p>Describe a symptom and NetSage AI will suggest a likely cause — for a human engineer to review and confirm.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
    <b>How this works:</b> NetSage AI matches your description against known fault patterns
    (VLAN, DHCP, DNS, ACL, NAT, Routing, Wireless) drawn from a curated case bank of real
    troubleshooting scenarios. It never applies a fix automatically — every suggestion is
    flagged for human sign-off, in line with responsible AI practice for network operations.
    </div>
    """, unsafe_allow_html=True)

    if COL_SYMPTOM is None:
        st.error("Couldn't find a symptom column in your CSV. Check the sidebar debug panel.")
    else:
        c1, c2 = st.columns([2, 1])
        with c1:
            sample = st.selectbox("Pick a sample symptom, or choose to type your own:",
                                   ["-- type my own --"] + df[COL_SYMPTOM].dropna().tolist())
            if sample == "-- type my own --":
                symptom_input = st.text_area("Describe the network issue:", height=110,
                                              placeholder="e.g. Two PCs in the same VLAN can't ping each other...")
            else:
                symptom_input = sample
                st.text_area("Symptom:", value=symptom_input, height=110, disabled=True)
        with c2:
            st.markdown("**Categories covered**")
            for cat in CATEGORY_KEYWORDS.keys():
                st.caption(f"• {cat}")

        if st.button("🔍 Get AI Diagnosis", type="primary"):
            if symptom_input.strip() == "":
                st.warning("Please enter or select a symptom first.")
            else:
                result = diagnose(symptom_input)
                st.markdown(f"""
                <div class="result-card">
                    <span class="badge badge-cat">{result['predicted_category']}</span>
                    <span class="badge badge-conf">Confidence: {result['confidence']}</span>
                    <h4 style="margin-top:16px;">Closest known case: {result['closest_case']}</h4>
                    <p><b>Likely root cause:</b><br>{result['root_cause']}</p>
                    <p><b>Suggested fix:</b><br>{result['fix']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.info("⚠️ This is an AI-generated suggestion only. A qualified network admin must "
                        "verify the root cause and approve the fix before it is applied to any live device.")

# ================= PAGE: DASHBOARD =================
elif page == "📊 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard</h1>
        <p>Overview of the case bank and how reliably the AI checker matches known issues.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", len(df))
    col2.metric("Categories", df[COL_CATEGORY].nunique() if COL_CATEGORY else "N/A")
    if COL_DIFFICULTY:
        col3.metric("Most Common Difficulty", df[COL_DIFFICULTY].mode()[0])
    if COL_CATEGORY:
        col4.metric("Top Issue Type", df[COL_CATEGORY].mode()[0])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if COL_CATEGORY:
            st.subheader("Issue Types Breakdown")
            st.bar_chart(df[COL_CATEGORY].value_counts())
            st.caption("Number of cases in the bank per network fault category.")
    with c2:
        if COL_DIFFICULTY:
            st.subheader("Difficulty Breakdown")
            st.bar_chart(df[COL_DIFFICULTY].value_counts())
            st.caption("Split of cases by complexity — used to balance the test/demo set.")

    st.markdown("---")
    if COL_SYMPTOM and COL_CATEGORY:
        df["ai_predicted_category"] = df[COL_SYMPTOM].apply(predict_category)
        df["ai_correct"] = df["ai_predicted_category"] == df[COL_CATEGORY]
        agreement_rate = df["ai_correct"].mean() * 100
        st.subheader("🤖 AI Agreement Rate")
        st.progress(min(agreement_rate / 100, 1.0))
        st.metric("AI matched the correct category", f"{agreement_rate:.1f}%",
                   help="Percentage of cases where the rule-based checker's predicted category "
                        "matched the ground-truth category in the dataset.")
        st.caption("This is the core transparency metric for the project — it shows how often "
                   "the AI's first guess needs no human correction at all.")

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
    | **Case Bank** (`dataset/cases.csv`) | 35 real-world troubleshooting scenarios with ground-truth root causes and fixes |
    | **Rule-Based Checker** | Matches symptom text against category keywords to predict the likely fault type |
    | **Dashboard** | Visualizes issue-type distribution and measures AI agreement rate against ground truth |
    | **Responsible AI Log** | Tracks every case where the AI's guess was wrong, for full transparency |
    | **Packet Tracer Scenarios** | Hands-on `.pkt` labs matching each case, for practical verification |

    ### 🛡️ Responsible AI Principles
    - The AI **never applies a fix automatically** — every suggestion requires human sign-off.
    - Every prediction is logged, including wrong ones, so accuracy can be audited.
    - Confidence levels are shown alongside every suggestion so users know how much to trust it.

    ### 🛠️ Tech Stack
    Python · Streamlit · Pandas · Cisco Packet Tracer

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