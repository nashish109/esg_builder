import streamlit as st
import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

def get_companies():
    try:
        with open(DATA_DIR / "companies.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading companies: {e}")
        return []

def delete_company(company_id):
    try:
        companies = get_companies()
        companies = [c for c in companies if c["id"] != company_id]

        with open(DATA_DIR / "companies.json", "w") as f:
            json.dump(companies, f, indent=2)

        # Remove ESG scores for this company
        try:
            with open(DATA_DIR / "esg_scores.json", "r") as f:
                scores = json.load(f)
            scores = [s for s in scores if s["company_id"] != company_id]
            with open(DATA_DIR / "esg_scores.json", "w") as f:
                json.dump(scores, f, indent=2)
        except Exception as e:
            st.warning(f"Could not remove ESG scores: {e}")

        return True
    except Exception as e:
        st.error(f"Error deleting company: {e}")
        return False

def page():
    st.header("Delete a Company")

    all_companies = get_companies()
    if not all_companies:
        st.warning("No companies available to delete.")
        return

    company_options = {c["name"]: c["id"] for c in all_companies}

    company_to_delete_name = st.selectbox(
        "Select a company to delete:",
        options=[""] + list(company_options.keys()),
        key="delete_company_selectbox"
    )

    if st.button("Delete Company"):
        if not company_to_delete_name:
            st.warning("Please select a company to delete.")
            return

        company_id_to_delete = company_options.get(company_to_delete_name)
        msg = st.empty()

        if delete_company(company_id_to_delete):
            msg.success(f"✅ Company '{company_to_delete_name}' deleted successfully!")
            time.sleep(2.5)          # ⏳ show confirmation
            msg.empty()
            st.rerun()
        else:
            msg.error("❌ Failed to delete company.")

if __name__ == "__main__":
    page()
