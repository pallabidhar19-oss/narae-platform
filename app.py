import streamlit as st
import openai
from datetime import date, timedelta, datetime

# Page config
st.set_page_config(
    page_title="Narae — K-Entertainment Intelligence Platform",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a14 0%, #0d0d1a 50%, #080810 100%);
    color: #e8e8f0;
}

.narae-header {
    background: linear-gradient(135deg, #1a0533 0%, #0d1544 50%, #001a2e 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.narae-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.narae-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0;
}

.narae-tagline {
    color: rgba(167, 139, 250, 0.8);
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}

.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #a78bfa;
    margin: 0;
}

.metric-label {
    font-size: 12px;
    color: rgba(232,232,240,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

.result-box {
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
}

.risk-high {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #fca5a5;
}

.risk-medium {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #fcd34d;
}

.risk-low {
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #6ee7b7;
}

.score-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1px;
}

.tab-section {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 28px;
    margin-top: 16px;
}

/* Override streamlit defaults */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: rgba(232,232,240,0.6);
    font-weight: 500;
    border-radius: 8px;
    padding: 8px 20px;
}

.stTabs [aria-selected="true"] {
    background: rgba(139, 92, 246, 0.25) !important;
    color: #a78bfa !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 24px;
    width: 100%;
    transition: all 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    box-shadow: 0 4px 20px rgba(139,92,246,0.4);
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e8e8f0;
    border-radius: 8px;
}

.stTextInput > div > div > input, .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e8e8f0;
    border-radius: 8px;
}

.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e8e8f0;
    border-radius: 8px;
}

div[data-testid="stMarkdownContainer"] p { color: rgba(232,232,240,0.85); }
h1, h2, h3 { color: #e8e8f0; }
label { color: rgba(232,232,240,0.7) !important; }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
try:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

# Header
st.markdown("""
<div class="narae-header">
    <p class="narae-logo">나래 Narae</p>
    <p class="narae-tagline">K-Entertainment Intelligence Platform · AI-Powered Logistics & Operations</p>
</div>
""", unsafe_allow_html=True)

# Platform metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div class="metric-card"><p class="metric-number">150+</p><p class="metric-label">Countries</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><p class="metric-number">5000+</p><p class="metric-label">HS Codes</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><p class="metric-number">Real-time</p><p class="metric-label">AI Analysis</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><p class="metric-number">6</p><p class="metric-label">AI Modules</p></div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="metric-card"><p class="metric-number">Big 4</p><p class="metric-label">Target Clients</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎁 Customs Intelligence",
    "✈️ Shipping Optimizer",
    "🎤 Artist Tour Planner",
    "🛡️ IP & Brand Risk",
    "📊 Shipment Readiness",
    "🗺️ Platform Vision"
])

# ============================================================
# TAB 1 — CUSTOMS INTELLIGENCE
# ============================================================
with tab1:
    st.markdown("### 🎁 K-Entertainment Customs Intelligence Engine")
    st.markdown("*AI-powered HS code classification, duty estimation, documentation requirements, and customs risk analysis*")

    col1, col2 = st.columns([2, 1])
    with col1:
        product = st.text_input("Product Description", placeholder="e.g. BTS Map of the Soul cotton hoodie, 380gsm, with embroidered logo")
        country = st.selectbox("Destination Country", [
            "United States", "United Kingdom", "Germany", "France", "Japan",
            "Australia", "Canada", "Brazil", "Argentina", "India", "Singapore",
            "Mexico", "Netherlands", "Spain", "Italy", "South Korea"
        ])
    with col2:
        value = st.number_input("Shipment Value (USD)", min_value=0.0, value=500.0, step=50.0)
        quantity = st.number_input("Quantity (units)", min_value=1, value=100)
        artist = st.text_input("Artist/IP Name (optional)", placeholder="e.g. BTS, Stray Kids")

    if st.button("🔍 Run Customs Analysis", key="customs_btn"):
        if not client:
            st.error("OpenAI API key not configured")
        elif product:
            with st.spinner("Running AI customs classification..."):
                prompt = f"""You are a senior customs classification expert specialising in K-entertainment merchandise.

Analyse this shipment:
- Product: {product}
- Destination: {country}
- Value: ${value} USD
- Quantity: {quantity} units
- Artist/IP: {artist if artist else 'Not specified'}

Provide a comprehensive analysis with these exact sections:

**1. HS/HTS CLASSIFICATION**
- Primary HS Code (6-digit international)
- HTS Code for {country} (if applicable, 8-10 digit)
- Classification reasoning
- Alternative codes to consider

**2. IMPORT DUTY ESTIMATE**
- Duty rate (%)
- Estimated duty on stated value: $X
- Total landed cost estimate
- Any preferential rates available (FTA, GSP)

**3. REQUIRED DOCUMENTATION**
List each document required for this shipment to {country}

**4. CUSTOMS RISKS**
Rate each risk as HIGH/MEDIUM/LOW:
- Misclassification risk
- Under-valuation risk
- IP/brand authenticity risk (especially for licensed artist merchandise)
- Labelling compliance risk
- Import restriction risk

**5. IP & BRAND CONSIDERATIONS**
Specific risks for licensed {artist if artist else 'K-entertainment'} merchandise

**6. RECOMMENDED NEXT STEPS**
Prioritised action list

Be specific, accurate, and practical."""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1200
                )

            result = response.choices[0].message.content
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                "📥 Download Analysis Report",
                data=f"NARAE CUSTOMS ANALYSIS\n{'='*50}\nProduct: {product}\nDestination: {country}\nValue: ${value}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{result}",
                file_name=f"narae_customs_{country.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter a product description")

# ============================================================
# TAB 2 — SHIPPING OPTIMIZER
# ============================================================
with tab2:
    st.markdown("### ✈️ Shipping Cost Optimizer")
    st.markdown("*Compare air vs sea freight with timeline analysis and cost optimization*")

    AIR_RATES = {
        "United States": {"rate": 6.5, "transit": 3, "customs": 4},
        "United Kingdom": {"rate": 7.0, "transit": 4, "customs": 3},
        "Germany": {"rate": 7.0, "transit": 4, "customs": 3},
        "France": {"rate": 7.0, "transit": 4, "customs": 3},
        "Japan": {"rate": 4.5, "transit": 2, "customs": 3},
        "Australia": {"rate": 8.0, "transit": 5, "customs": 4},
        "Canada": {"rate": 6.5, "transit": 3, "customs": 3},
        "Brazil": {"rate": 9.0, "transit": 6, "customs": 15},
        "Argentina": {"rate": 9.5, "transit": 7, "customs": 18},
        "India": {"rate": 5.5, "transit": 3, "customs": 7},
        "Singapore": {"rate": 5.0, "transit": 2, "customs": 2},
        "Mexico": {"rate": 7.0, "transit": 4, "customs": 5},
    }

    SEA_RATES = {
        "United States": {"rate": 1.2, "transit": 18, "min": 800},
        "United Kingdom": {"rate": 1.0, "transit": 25, "min": 900},
        "Germany": {"rate": 1.0, "transit": 28, "min": 900},
        "France": {"rate": 1.0, "transit": 28, "min": 900},
        "Japan": {"rate": 0.8, "transit": 5, "min": 600},
        "Australia": {"rate": 1.3, "transit": 22, "min": 1000},
        "Canada": {"rate": 1.2, "transit": 20, "min": 800},
        "Brazil": {"rate": 1.5, "transit": 32, "min": 1200},
        "Argentina": {"rate": 1.6, "transit": 35, "min": 1300},
        "India": {"rate": 1.0, "transit": 12, "min": 700},
        "Singapore": {"rate": 0.9, "transit": 6, "min": 650},
        "Mexico": {"rate": 1.1, "transit": 15, "min": 750},
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        ship_dest = st.selectbox("Destination", list(AIR_RATES.keys()), key="ship_dest")
        weight = st.number_input("Total Weight (kg)", min_value=1.0, value=100.0)
    with col2:
        required_date = st.date_input("Required Arrival Date", value=date.today() + timedelta(days=30))
        today = date.today()
        days_available = (required_date - today).days
    with col3:
        cargo_value = st.number_input("Cargo Value (USD)", min_value=0.0, value=5000.0)
        event_type = st.selectbox("Event Type", ["Concert Tour", "Pop-up Store", "Fan Meeting", "Album Release", "General Retail"])

    if st.button("🚀 Calculate Optimal Shipping", key="ship_btn"):
        if ship_dest in AIR_RATES and ship_dest in SEA_RATES:
            air = AIR_RATES[ship_dest]
            sea = SEA_RATES[ship_dest]

            air_cost = weight * air["rate"]
            air_total = air["transit"] + air["customs"]
            air_ship_by = required_date - timedelta(days=air_total)
            air_viable = days_available >= air_total

            sea_cost = max(weight * sea["rate"], sea["min"])
            sea_total = sea["transit"] + air["customs"]
            sea_ship_by = required_date - timedelta(days=sea_total)
            sea_viable = days_available >= sea_total

            savings = abs(air_cost - sea_cost)

            st.markdown("---")
            col_air, col_sea = st.columns(2)

            with col_air:
                status = "✅ VIABLE" if air_viable else "❌ NOT VIABLE"
                color = "#34d399" if air_viable else "#ef4444"
                st.markdown(f"### ✈️ Air Freight — {status}")
                st.metric("Estimated Cost", f"${air_cost:,.0f}")
                st.metric("Transit Time", f"{air['transit']} days")
                st.metric("Customs Clearance", f"{air['customs']} days")
                st.metric("Total Days Needed", f"{air_total} days")
                if air_viable:
                    st.success(f"Ship by: {air_ship_by.strftime('%B %d, %Y')}")
                else:
                    st.error(f"Deadline missed — needed to ship by {air_ship_by.strftime('%B %d, %Y')}")

            with col_sea:
                status = "✅ VIABLE" if sea_viable else "❌ NOT VIABLE"
                st.markdown(f"### 🚢 Sea Freight — {status}")
                st.metric("Estimated Cost", f"${sea_cost:,.0f}")
                st.metric("Transit Time", f"{sea['transit']} days")
                st.metric("Customs Clearance", f"{air['customs']} days")
                st.metric("Total Days Needed", f"{sea_total} days")
                if sea_viable:
                    st.success(f"Ship by: {sea_ship_by.strftime('%B %d, %Y')} — saves ${savings:,.0f} vs air")
                else:
                    st.error(f"Too slow — needed to ship by {sea_ship_by.strftime('%B %d, %Y')}")

            st.markdown("---")
            st.markdown("#### 💡 Narae Recommendation")
            if sea_viable:
                st.success(f"**Use Sea Freight.** Save ${savings:,.0f} on this shipment. Ship by {sea_ship_by.strftime('%B %d')}.")
            elif air_viable:
                st.warning(f"**Air Freight only viable option.** Cost: ${air_cost:,.0f}. Ship by {air_ship_by.strftime('%B %d')}.")
            else:
                st.error("**Neither method meets your deadline.** Consider local sourcing or expedited courier (DHL/FedEx Premium).")

            if ship_dest in ["Brazil", "Argentina"]:
                st.markdown('<div class="risk-high">⚠️ HIGH-DUTY MARKET: Brazil/Argentina require CFO-level customs strategy. Contact your customs broker before shipping.</div>', unsafe_allow_html=True)

# ============================================================
# TAB 3 — ARTIST TOUR PLANNER
# ============================================================
with tab3:
    st.markdown("### 🎤 Artist Tour Merchandise Logistics Planner")
    st.markdown("*Plan merchandise logistics across tour dates with AI-powered timeline intelligence*")

    CUSTOMS_DAYS_TOUR = {
        "United States": 4, "United Kingdom": 3, "Germany": 3,
        "France": 3, "Japan": 3, "Australia": 4, "Canada": 3,
        "Brazil": 15, "Argentina": 18, "Mexico": 5, "Singapore": 2,
        "Indonesia": 7, "Thailand": 5, "Philippines": 6
    }

    col1, col2 = st.columns(2)
    with col1:
        tour_artist = st.text_input("Artist / Group Name", placeholder="e.g. Stray Kids")
        tour_name = st.text_input("Tour Name", placeholder="e.g. DOMINATEWORLD Tour 2027")
        production_date = st.date_input("Merchandise Production Completion Date", value=date.today() + timedelta(days=14))

    with col2:
        merch_weight = st.number_input("Total Merch Weight per City (kg)", value=200.0)
        merch_value = st.number_input("Merch Value per City (USD)", value=20000.0)
        air_rate = st.number_input("Air Freight Rate ($/kg)", value=6.5)

    st.markdown("#### Tour Dates")
    st.markdown("*Add your tour cities and dates below*")

    tour_cities = []
    num_cities = st.number_input("Number of Tour Cities", min_value=1, max_value=15, value=5)

    city_options = list(CUSTOMS_DAYS_TOUR.keys())

    for i in range(int(num_cities)):
        col1, col2 = st.columns(2)
        with col1:
            city = st.selectbox(f"City {i+1}", city_options, key=f"city_{i}")
        with col2:
            tour_date = st.date_input(f"Show Date {i+1}", value=date.today() + timedelta(days=30 + i*7), key=f"date_{i}")
        tour_cities.append({"city": city, "date": tour_date})

    if st.button("🗓️ Generate Tour Logistics Plan", key="tour_btn"):
        st.markdown("---")
        st.markdown(f"### {tour_artist} — {tour_name} — Logistics Intelligence Report")

        all_viable = True
        results = []

        for stop in tour_cities:
            city = stop["city"]
            tour_date = stop["date"]
            customs_days = CUSTOMS_DAYS_TOUR.get(city, 5)
            air_transit = 3
            total_days_needed = air_transit + customs_days
            ship_by = tour_date - timedelta(days=total_days_needed)
            prod_to_ship = (ship_by - production_date).days
            freight_cost = merch_weight * air_rate

            if prod_to_ship < 0:
                status = "🔴 CRITICAL"
                all_viable = False
            elif prod_to_ship < 3:
                status = "🟡 AT RISK"
                all_viable = False
            else:
                status = "🟢 ON TRACK"

            results.append({
                "city": city,
                "tour_date": tour_date,
                "ship_by": ship_by,
                "prod_buffer": prod_to_ship,
                "freight_cost": freight_cost,
                "status": status,
                "customs_days": customs_days
            })

        for r in results:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.markdown(f"**{r['city']}**")
                st.caption(f"Show: {r['tour_date'].strftime('%b %d, %Y')}")
            with col2:
                st.markdown(f"Ship by: **{r['ship_by'].strftime('%b %d')}**")
                st.caption(f"Customs: {r['customs_days']} days")
            with col3:
                st.markdown(f"Freight: **${r['freight_cost']:,.0f}**")
                st.caption(f"Buffer: {r['prod_buffer']} days")
            with col4:
                st.markdown(r['status'])
            st.divider()

        total_cost = sum(r['freight_cost'] for r in results)
        st.markdown(f"**Total Estimated Freight Cost: ${total_cost:,.0f}**")

        if all_viable:
            st.success("✅ All tour dates are achievable with current production timeline.")
        else:
            st.error("⚠️ Some dates are at risk. Consider earlier production start or local sourcing for critical markets.")

        if any(r['city'] in ["Brazil", "Argentina"] for r in results):
            st.markdown('<div class="risk-high">🚨 High-duty markets detected (Brazil/Argentina). These require advance customs strategy and CFO approval. Narae recommends engaging a local customs broker 8 weeks before each show date.</div>', unsafe_allow_html=True)

# ============================================================
# TAB 4 — IP & BRAND RISK
# ============================================================
with tab4:
    st.markdown("### 🛡️ IP & Brand Risk Analyzer")
    st.markdown("*AI-powered intellectual property and brand risk assessment for K-entertainment merchandise*")

    col1, col2 = st.columns(2)
    with col1:
        ip_product = st.text_input("Product Description", placeholder="e.g. Stray Kids MIROH graphic tee with member faces")
        ip_artist = st.text_input("Artist / Intellectual Property", placeholder="e.g. Stray Kids, JYP Entertainment")
        ip_country = st.selectbox("Target Market", [
            "United States", "European Union", "United Kingdom", "Japan",
            "Australia", "Brazil", "India", "Southeast Asia"
        ])
    with col2:
        license_status = st.selectbox("License Status", [
            "Officially Licensed (direct from agency)",
            "Officially Licensed (through distributor)",
            "Fan-made / Unofficial",
            "License status unknown",
            "Seeking license"
        ])
        seller_type = st.selectbox("Seller Type", [
            "Official agency merchandise",
            "Authorized third-party retailer",
            "Independent online seller",
            "Fan community organizer",
            "Wholesale distributor"
        ])
        platform = st.text_input("Sales Platform", placeholder="e.g. Weverse Shop, Amazon, Shopify store")

    if st.button("🔍 Analyze IP & Brand Risk", key="ip_btn"):
        if not client:
            st.error("OpenAI API key not configured")
        elif ip_product and ip_artist:
            with st.spinner("Running IP risk analysis..."):
                prompt = f"""You are an intellectual property expert specialising in K-entertainment merchandise and Korean agency rights.

Analyze the IP and brand risk for:
- Product: {ip_product}
- Artist/IP Owner: {ip_artist}
- Market: {ip_country}
- License Status: {license_status}
- Seller Type: {seller_type}
- Platform: {platform if platform else 'Not specified'}

Provide analysis in these sections:

**1. IP RISK ASSESSMENT**
Rate overall risk as: CRITICAL / HIGH / MEDIUM / LOW
Explain the primary IP concerns

**2. CUSTOMS SEIZURE RISK**
- Probability of customs detention for IP/brand reasons
- What customs officers look for
- Documentation that reduces seizure risk

**3. AGENCY ENFORCEMENT RISK**
- How aggressively does {ip_artist}'s agency pursue IP violations
- Known enforcement actions in {ip_country}
- Risk of cease-and-desist or legal action

**4. PLATFORM POLICY RISK**
- Risk of listing removal on major platforms
- DMCA/takedown exposure

**5. REQUIRED DOCUMENTATION**
What documents prove legitimacy and reduce risk

**6. MITIGATION RECOMMENDATIONS**
Specific steps to reduce risk for this shipment

**7. VERDICT**
Clear GO / PROCEED WITH CAUTION / DO NOT SHIP recommendation"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter product and artist information")

# ============================================================
# TAB 5 — SHIPMENT READINESS SCORE
# ============================================================
with tab5:
    st.markdown("### 📊 Shipment Readiness Intelligence Score")
    st.markdown("*Comprehensive go/no-go decision engine for K-entertainment merchandise shipments*")

    col1, col2, col3 = st.columns(3)
    with col1:
        sr_product = st.text_input("Product", placeholder="e.g. Photo cards set, official", key="sr_product")
        sr_destination = st.selectbox("Destination", ["United States", "United Kingdom", "Germany", "Japan", "Brazil", "Australia", "Canada", "Singapore"], key="sr_dest")
        sr_value = st.number_input("Total Shipment Value (USD)", min_value=0.0, value=2000.0, key="sr_val")

    with col2:
        sr_weight = st.number_input("Weight (kg)", min_value=0.1, value=20.0, key="sr_wt")
        sr_deadline = st.date_input("Hard Deadline", value=date.today() + timedelta(days=21), key="sr_dl")
        sr_licensed = st.selectbox("License Status", ["Officially Licensed", "Unauthorized", "Unknown"], key="sr_lic")

    with col3:
        sr_docs = st.multiselect("Documents Ready", [
            "Commercial Invoice",
            "Packing List",
            "Certificate of Origin",
            "License Agreement",
            "Bill of Lading / AWB",
            "Customs Bond (US)"
        ], key="sr_docs")
        sr_broker = st.selectbox("Customs Broker", ["Engaged", "Not yet engaged", "Not needed"], key="sr_broker")

    if st.button("⚡ Calculate Readiness Score", key="readiness_btn"):
        score = 0
        max_score = 100
        issues = []
        warnings = []
        good = []

        days_until = (sr_deadline - date.today()).days

        if days_until >= 21:
            score += 20
            good.append("✅ Sufficient lead time")
        elif days_until >= 14:
            score += 12
            warnings.append("⚠️ Tight timeline — 14-21 days")
        elif days_until >= 7:
            score += 5
            issues.append("🔴 Very tight timeline — under 14 days")
        else:
            issues.append("🔴 CRITICAL: Less than 7 days — shipment at serious risk")

        if sr_licensed == "Officially Licensed":
            score += 25
            good.append("✅ Official license — customs risk minimized")
        elif sr_licensed == "Unknown":
            score += 10
            warnings.append("⚠️ License status unknown — obtain documentation")
        else:
            score += 0
            issues.append("🔴 Unauthorized merchandise — high seizure risk")

        doc_score = len(sr_docs) * 5
        score += min(doc_score, 25)
        if len(sr_docs) >= 4:
            good.append(f"✅ Strong documentation ({len(sr_docs)} documents ready)")
        elif len(sr_docs) >= 2:
            warnings.append(f"⚠️ Partial documentation ({len(sr_docs)}/6 documents ready)")
        else:
            issues.append("🔴 Insufficient documentation")

        if sr_destination in ["Brazil", "Argentina"]:
            score -= 10
            issues.append("🔴 High-duty market — expect customs delays and additional costs")
        elif sr_destination in ["United States", "Germany", "Japan"]:
            score += 10
            good.append(f"✅ {sr_destination} — efficient customs processing")

        if sr_broker == "Engaged":
            score += 15
            good.append("✅ Customs broker engaged")
        elif sr_broker == "Not yet engaged":
            score += 5
            warnings.append("⚠️ Engage customs broker before shipping")

        if sr_value > 2500:
            score += 5
            good.append("✅ Commercial shipment value — proper customs handling required")

        score = max(0, min(100, score))

        st.markdown("---")

        if score >= 75:
            verdict = "🟢 GO"
            verdict_color = "#34d399"
            verdict_text = "Shipment is ready to proceed"
        elif score >= 50:
            verdict = "🟡 PROCEED WITH CAUTION"
            verdict_color = "#fcd34d"
            verdict_text = "Address warnings before shipping"
        else:
            verdict = "🔴 NOT READY"
            verdict_color = "#ef4444"
            verdict_text = "Resolve critical issues before proceeding"

        col_score, col_verdict = st.columns([1, 2])
        with col_score:
            st.markdown(f"""
            <div style="text-align:center; background:rgba(139,92,246,0.1); border:2px solid rgba(139,92,246,0.3); border-radius:16px; padding:32px;">
                <div style="font-size:64px; font-weight:800; color:#a78bfa; font-family:'Space Grotesk',sans-serif;">{score}</div>
                <div style="font-size:14px; color:rgba(232,232,240,0.5); text-transform:uppercase; letter-spacing:2px;">Readiness Score</div>
                <div style="margin-top:16px; font-size:20px; font-weight:700; color:{verdict_color};">{verdict}</div>
                <div style="font-size:12px; color:rgba(232,232,240,0.5); margin-top:4px;">{verdict_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_verdict:
            if good:
                st.markdown("**✅ Strengths**")
                for g in good:
                    st.markdown(f'<div class="risk-low">{g}</div>', unsafe_allow_html=True)
            if warnings:
                st.markdown("**⚠️ Warnings**")
                for w in warnings:
                    st.markdown(f'<div class="risk-medium">{w}</div>', unsafe_allow_html=True)
            if issues:
                st.markdown("**🔴 Critical Issues**")
                for issue in issues:
                    st.markdown(f'<div class="risk-high">{issue}</div>', unsafe_allow_html=True)

# ============================================================
# TAB 6 — PLATFORM VISION
# ============================================================
with tab6:
    st.markdown("### 🗺️ Narae Platform Vision")
    st.markdown("*Building the AI intelligence layer for the entire K-entertainment ecosystem*")

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(79,70,229,0.15)); border:1px solid rgba(139,92,246,0.3); border-radius:16px; padding:32px; margin-bottom:24px;">
        <h3 style="color:#a78bfa; margin:0 0 16px 0;">The Problem Narae Solves</h3>
        <p style="color:rgba(232,232,240,0.8); font-size:16px; line-height:1.7;">
        K-entertainment is a $10B+ global industry. Behind every world tour, album release, and fan event is a complex 
        logistics operation spanning 150+ countries — customs compliance, HS classification, duty calculation, IP verification, 
        shipping optimization, and tour timeline planning. This is currently done manually, expensively, and inaccurately.
        </p>
        <p style="color:rgba(232,232,240,0.8); font-size:16px; line-height:1.7;">
        Narae is building the AI intelligence layer that K-entertainment companies have been waiting for.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align:left; padding:24px;">
            <div style="font-size:24px; margin-bottom:12px;">🎁</div>
            <div style="font-weight:600; color:#a78bfa; margin-bottom:8px;">Phase 1 — Logistics Intelligence</div>
            <div style="font-size:13px; color:rgba(232,232,240,0.7); line-height:1.6;">
            • HS/HTS customs classification<br>
            • Import duty estimation<br>
            • Documentation requirements<br>
            • IP & brand risk analysis<br>
            • Shipment readiness scoring
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align:left; padding:24px;">
            <div style="font-size:24px; margin-bottom:12px;">🎤</div>
            <div style="font-weight:600; color:#60a5fa; margin-bottom:8px;">Phase 2 — Tour Operations AI</div>
            <div style="font-size:13px; color:rgba(232,232,240,0.7); line-height:1.6;">
            • Multi-city tour planning<br>
            • Production timeline optimizer<br>
            • Local sourcing intelligence<br>
            • Venue requirements database<br>
            • Cost optimization engine
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align:left; padding:24px;">
            <div style="font-size:24px; margin-bottom:12px;">🤖</div>
            <div style="font-weight:600; color:#34d399; margin-bottom:8px;">Phase 3 — Full Industry OS</div>
            <div style="font-size:13px; color:rgba(232,232,240,0.7); line-height:1.6;">
            • Fan demand prediction<br>
            • AI fan interaction system<br>
            • Content localisation engine<br>
            • Revenue forecasting by market<br>
            • Artist schedule optimisation
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 🎯 Target Clients")
    col1, col2, col3, col4 = st.columns(4)
    clients = [
        ("HYBE", "BTS, Stray Kids, NewJeans", "Active conversation"),
        ("JYP Entertainment", "Stray Kids, TWICE, ITZY", "Outreach initiated"),
        ("SM Entertainment", "aespa, EXO, NCT", "Identified"),
        ("YG Entertainment", "BLACKPINK, BIGBANG", "Identified"),
    ]
    for col, (name, artists, status) in zip([col1, col2, col3, col4], clients):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:16px;">
                <div style="font-weight:700; color:#a78bfa;">{name}</div>
                <div style="font-size:11px; color:rgba(232,232,240,0.5); margin:4px 0;">{artists}</div>
                <div style="font-size:11px; color:#34d399;">● {status}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25); border-radius:12px; padding:20px;">
        <strong style="color:#34d399;">Research Context</strong>
        <p style="color:rgba(232,232,240,0.7); margin:8px 0 0 0; font-size:14px;">
        Narae is built on peer-reviewed research published on SSRN examining AI reliability in structured classification tasks 
        (SSRN Top 10 Downloads — Labor Markets category). The LLM Customs Classifier evaluation framework benchmarks 
        hallucination rates in HS code classification — directly addressing alignment challenges in high-stakes AI deployments.
        This positions Narae not just as a product but as applied AI research in the entertainment logistics domain.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px; color:rgba(232,232,240,0.3); font-size:12px;">
    나래 Narae · K-Entertainment Intelligence Platform · Built by Pallabi Dhar · Fanomenon<br>
    narae-import-assistant.streamlit.app · github.com/pallabidhar19-oss
</div>
""", unsafe_allow_html=True)
