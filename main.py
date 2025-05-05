import streamlit as st
import pandas as pd
import altair as alt

# Streamlit UI
st.title("Gabor-Granger Price Optimization")

# File uploader for the dataset
uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file is not None:
    # Read the dataset
    df = pd.read_excel(uploaded_file)

    # Function to calculate the likelihood of purchase
    def purchase_likelihood(purchase_intent):
        mapping = {
            "Definitely would buy": 1,
            "Probably would buy": 0.8,
            "Might or might not buy": 0.5,
            "Probably would not buy": 0.2,
            "Definitely would not buy": 0
        }
        return mapping[purchase_intent]

    # Apply the mapping to the dataset
    df['likelihood'] = df['purchase_intent'].apply(purchase_likelihood)

    # Calculate average likelihood of purchase at each price point
    price_analysis = df.groupby('price')['likelihood'].mean().reset_index()

    # Calculate estimated revenue at each price point
    price_analysis['estimated_revenue'] = price_analysis['price'] * price_analysis['likelihood']

    # Determine the optimal price point
    optimal_price = price_analysis.loc[price_analysis['estimated_revenue'].idxmax()]

    st.write("### Survey Data")
    st.write(df.head())

    st.write("### Price Analysis")
    st.write(price_analysis)

    st.write(f"### Optimal Price Point")
    st.write(f"Optimal price point: ${optimal_price['price']:.2f}")
    st.write(f"Estimated revenue: ${optimal_price['estimated_revenue']:.2f}")

    st.write("### Likelihood and Estimated Revenue vs. Price")

    # Create the chart using Altair
    chart = alt.Chart(price_analysis).transform_fold(
        fold=['likelihood', 'estimated_revenue'],
        as_=['Metric', 'Value']
    ).mark_line().encode(
        x=alt.X('price', title='Price ($)'),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('Metric:N', title='Metric', scale=alt.Scale(domain=['likelihood', 'estimated_revenue'], range=['blue', 'green']))
    ).properties(
        width=600,
        height=400
    ).interactive()

    # Display the chart
    st.altair_chart(chart)
else:
    st.write("Please upload an Excel file.")
