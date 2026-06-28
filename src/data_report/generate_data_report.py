import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os, sys
from src.exception import CustomException


class DashboardGenerator:
    def __init__(self, data):
        self.data = data

    def display_general_info(self):
        st.header('General Information')

        # Convert 'Over_All_Rating' and 'Price' columns to numeric
        self.data['Over_All_Rating'] = pd.to_numeric(self.data['Over_All_Rating'], errors='coerce')
        self.data['Price'] = pd.to_numeric(
            self.data['Price'].apply(lambda x: x.replace("₹", "")),
            errors='coerce')

        self.data["Rating"] = pd.to_numeric(self.data['Rating'], errors='coerce')

        # Summary pie chart of average ratings by product
        product_ratings = self.data.groupby('Product Name', as_index=False)['Over_All_Rating'].mean().dropna()

        fig_pie = px.pie(product_ratings, values='Over_All_Rating', names='Product Name',
                         title='Average Ratings by Product')
        st.plotly_chart(fig_pie)

        # Bar chart comparing average prices of different products with different colors
        avg_prices = self.data.groupby('Product Name', as_index=False)['Price'].mean().dropna()
        fig_bar = px.bar(avg_prices, x='Product Name', y='Price', color='Product Name',
                         title='Average Price Comparison Between Products',
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_bar.update_xaxes(title='Product Name')
        fig_bar.update_yaxes(title='Average Price')
        st.plotly_chart(fig_bar)

    def display_product_sections(self):
        st.header('Detailed Product Analysis')

        product_names = self.data['Product Name'].unique()

        for i, product_name in enumerate(product_names):
            product_data = self.data[self.data['Product Name'] == product_name]

            # Create a clean container for each product
            with st.container():
                st.markdown("---")
                st.subheader(f"📦 {product_name}")

                # Display key metrics side-by-side
                col1, col2 = st.columns(2)
                with col1:
                    avg_price = product_data['Price'].mean()
                    if pd.isna(avg_price):
                        st.metric(label="Average Price", value="N/A")
                    else:
                        st.metric(label="Average Price", value=f"₹{avg_price:.2f}")
                with col2:
                    avg_rating = product_data['Over_All_Rating'].mean()
                    if pd.isna(avg_rating):
                        st.metric(label="Overall Rating", value="N/A")
                    else:
                        st.metric(label="Overall Rating", value=f"⭐ {avg_rating:.2f}")

                # Positive & Negative Reviews side-by-side
                rev_col1, rev_col2 = st.columns(2)
                
                with rev_col1:
                    st.markdown("### 🟢 Positive Reviews (Rating ≥ 4.5)")
                    positive_reviews = product_data[product_data['Rating'] >= 4.5].nlargest(5, 'Rating')
                    if not positive_reviews.empty:
                        for index, row in positive_reviews.iterrows():
                            comment_text = row['Comment'].strip() if isinstance(row['Comment'], str) else "No comment given"
                            st.info(f"**Rating: {row['Rating']}** (by {row['Name']})\n\n\"{comment_text}\"")
                    else:
                        st.write("*No positive reviews found for this product.*")

                with rev_col2:
                    st.markdown("### 🔴 Negative Reviews (Rating ≤ 2.0)")
                    negative_reviews = product_data[product_data['Rating'] <= 2.0].nsmallest(5, 'Rating')
                    if not negative_reviews.empty:
                        for index, row in negative_reviews.iterrows():
                            comment_text = row['Comment'].strip() if isinstance(row['Comment'], str) else "No comment given"
                            st.warning(f"**Rating: {row['Rating']}** (by {row['Name']})\n\n\"{comment_text}\"")
                    else:
                        st.write("*No negative reviews found for this product.*")

                # Rating Distribution Chart inside an expander
                with st.expander("📊 View Rating Distribution"):
                    rating_counts = product_data['Rating'].value_counts().sort_index(ascending=False)
                    if not rating_counts.empty:
                        chart_data = pd.DataFrame({
                            'Rating Star': [f"⭐ {str(r).rstrip('.0') if str(r).endswith('.0') else r}" for r in rating_counts.index],
                            'Review Count': rating_counts.values
                        })
                        fig = px.bar(
                            chart_data, 
                            x='Review Count', 
                            y='Rating Star', 
                            orientation='h',
                            title=f"Rating Distribution",
                            color='Rating Star',
                            color_discrete_sequence=px.colors.sequential.Blues_r
                        )
                        fig.update_layout(showlegend=False, height=250, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("*No rating data available.*")

