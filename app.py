import streamlit as st
import requests

st.set_page_config(page_title="Budget Trip Planner", layout="centered")

st.title("💸 Budget Trip Planner")

st.markdown("Plan your trip budget wisely by selecting your destination, trip duration, and budget.")

# --- DESTINATIONS ---
destinations = [
    "Paris", "New York", "Tokyo", "Sydney", "London", "Dubai", "Rome", "Bangkok", "Barcelona", "Cape Town"
]

# --- CURRENCY CONVERSION ---
def get_exchange_rate(base_currency, target_currency):
    """Fetch the exchange rate from the ExchangeRate API."""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error("Failed to fetch exchange rates. Please try again later.")
        return None
    
    data = response.json()
    
    # Check if the target currency is in the response
    if target_currency in data['rates']:
        return data['rates'][target_currency]
    else:
        st.error(f"Currency conversion failed: {target_currency} not found.")
        return None

# --- FORM ---
with st.form("trip_form"):
    destination = st.selectbox("Destination", destinations)
    days = st.number_input("Number of Days", min_value=1, step=1)
    budget = st.number_input("Total Budget (in your currency)", min_value=0.0, step=10.0)
    base_currency = st.selectbox("Base Currency", ["USD", "EUR", "JPY", "AUD", "GBP"])  # Add more currencies as needed
    target_currency = st.selectbox("Target Currency", ["USD", "EUR", "JPY", "AUD", "GBP"])  # Add more currencies as needed

    submitted = st.form_submit_button("Plan My Trip")

# --- AFTER SUBMISSION ---
if submitted and destination:
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    
    if exchange_rate is not None:  # Proceed only if exchange rate is valid
        converted_budget = budget * exchange_rate
        daily_budget = converted_budget / days
        accommodation = converted_budget * 0.4
        food = converted_budget * 0.3
        transport = converted_budget * 0.2
        misc = converted_budget * 0.1

        st.subheader(f"🗺️ Trip Plan for {destination}")
        st.write(f"**Duration:** {days} days")
        st.write(f"**Total Budget in {target_currency}:** {converted_budget:.2f}")

        st.write(f"**Daily Budget:** {daily_budget:.2f}")

        st.markdown("### 🧾 Budget Breakdown")
        col1, col2 = st.columns(2)

        with col1:
            st.success(f"🏨 Accommodation: {accommodation:.2f}")
            st.warning(f"🚗 Transport: {transport:.2f}")
        with col2:
            st.info(f"🍽️ Food: {food:.2f}")
            st.error(f"🎁 Miscellaneous: {misc:.2f}")

elif submitted:
    st.warning("Please select a destination to generate your plan.")