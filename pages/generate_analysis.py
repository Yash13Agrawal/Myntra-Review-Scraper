import pandas as pd
import streamlit as st
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.utils import fetch_product_names_from_cloud
from src.data_report.generate_data_report import DashboardGenerator

mongo_con = MongoIO()


def create_analysis_page(review_data: pd.DataFrame):
    if review_data is not None:
        with st.expander("📝 View Raw Scraped Data"):
            st.dataframe(review_data)
        if st.button("Generate Analysis"):
            dashboard = DashboardGenerator(review_data)

            # Display general information
            dashboard.display_general_info()

            # Display product-specific sections
            dashboard.display_product_sections()


# Load previously scraped products from MongoDB
try:
    product_names = fetch_product_names_from_cloud()
except Exception:
    product_names = []

# Determine the default selected product (if they just scraped one in the current session)
default_product = None
if "data" in st.session_state and st.session_state.data:
    default_product = st.session_state.get(SESSION_PRODUCT_KEY)

if product_names:
    options = ["-- Select a Product --"] + sorted(list(set(product_names)))
    default_index = 0
    if default_product in options:
        default_index = options.index(default_product)
        
    selected_product = st.selectbox(
        "Select a product to analyze:",
        options=options,
        index=default_index
    )
    
    if selected_product != "-- Select a Product --":
        data = mongo_con.get_reviews(product_name=selected_product)
        create_analysis_page(data)
    else:
        st.info("Please select a product from the dropdown above, or go to the search page to scrape a new one.")
else:
    st.warning("No scraped data found in MongoDB. Please go to the search page to scrape some reviews first!")


