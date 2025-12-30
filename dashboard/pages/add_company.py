import streamlit as st
import json
import time
import random
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent.parent.parent / "data"

def get_companies():
    try:
        with open(DATA_DIR / "companies.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_company(company_data):
    companies = get_companies()
    existing = next((c for c in companies if c["name"] == company_data["name"]), None)

    if existing:
        existing.update(company_data)
        action = "updated"
    else:
        company_data["id"] = max([c["id"] for c in companies], default=0) + 1
        companies.append(company_data)
        action = "added"

    with open(DATA_DIR / "companies.json", "w") as f:
        json.dump(companies, f, indent=2)

    return action

def generate_initial_esg_scores(company_id):
    """Generate initial ESG scores for a new company."""
    try:
        with open(DATA_DIR / "esg_scores.json", "r") as f:
            esg_scores = json.load(f)
    except:
        esg_scores = []

    # Generate scores for the past 4 quarters
    base_date = datetime.now().replace(day=1, month=((datetime.now().month - 1) // 3) * 3 + 1)
    for i in range(4):
        score_date = base_date - timedelta(days=90 * (3 - i))
        # Generate random scores for each pillar between 60-95, similar to existing data
        environmental_score = round(random.uniform(60, 95), 1)
        social_score = round(random.uniform(60, 95), 1)
        governance_score = round(random.uniform(60, 95), 1)
        total_score = round((environmental_score + social_score + governance_score) / 3, 1)

        esg_scores.append({
            "company_id": company_id,
            "rating_date": score_date.strftime("%Y-%m-%d"),
            "environmental_score": environmental_score,
            "social_score": social_score,
            "governance_score": governance_score,
            "total_score": total_score,
            "source": "Generated"
        })

    try:
        with open(DATA_DIR / "esg_scores.json", "w") as f:
            json.dump(esg_scores, f, indent=2)
    except Exception as e:
        st.error(f"Error saving ESG scores: {e}")

def page():
    st.header("Add / Update Company")

    companies = get_companies()
    company_map = {c["name"]: c for c in companies}

    sectors = sorted({c["sector"] for c in companies if c.get("sector")})
    regions = sorted({c["region"] for c in companies if c.get("region")})

    selected_company = st.selectbox(
        "Select Existing Company (optional)",
        options=[""] + list(company_map.keys())
    )

    prefill = company_map.get(selected_company, {})

    with st.form("company_form", clear_on_submit=True):
        name = st.text_input("Company Name", value=prefill.get("name", ""))
        ticker = st.text_input("Ticker (e.g., TSLA)", value=prefill.get("ticker", ""))

        # -------- SECTOR --------
        sector_dropdown = st.selectbox(
            "Sector (choose existing)",
            options=[""] + sectors
        )
        sector_text = st.text_input("Or enter new sector")

        # -------- REGION --------
        region_dropdown = st.selectbox(
            "Region (choose existing)",
            options=[""] + regions
        )
        region_text = st.text_input("Or enter new region")

        submitted = st.form_submit_button("Add / Update Company")

        if submitted:
            # ---- REQUIRED CHECK ----
            if not name or not ticker:
                st.warning("Company Name and Ticker are required.")
                return

            # ---- HARD EXCLUSIVITY CHECK ----
            if sector_dropdown and sector_text:
                st.error("❌ Please either select a Sector OR enter a new one — not both.")
                return

            if region_dropdown and region_text:
                st.error("❌ Please either select a Region OR enter a new one — not both.")
                return

            sector = sector_text or sector_dropdown or "N/A"
            region = region_text or region_dropdown or "N/A"

            company_data = {
                "name": name.strip(),
                "ticker": ticker.strip(),
                "sector": sector.strip(),
                "region": region.strip()
            }

            action = save_company(company_data)

            # Generate initial ESG scores for new companies
            if action == "added":
                generate_initial_esg_scores(company_data["id"])

            msg = st.empty()
            if action == "added":
                msg.success(f"✅ Company '{name}' added successfully!")
            else:
                msg.success(f"🔄 Company '{name}' updated successfully!")

            time.sleep(2.5)
            msg.empty()
            st.rerun()

if __name__ == "__main__":
    page()
