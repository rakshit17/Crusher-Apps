import streamlit as st
import matplotlib.pyplot as plt

def run_insights():
    

    # Total Cost Per Ton from Project Cost Calculator
    total_cost_per_ton = sum(st.session_state.calculator_data.values()) if "calculator_data" in st.session_state else 0.0

    # Final Rate from Rate Calculator
    if "materials" in st.session_state and st.session_state.materials:
        total_weighted_rate = sum(
            m["Rate (₹/Ton)"] * m["Production Percentage (%)"] for m in st.session_state.materials
        )
        total_percentage = sum(m["Production Percentage (%)"] for m in st.session_state.materials)
        selling_rate = total_weighted_rate / total_percentage if total_percentage > 0 else 0.0
    else:
        selling_rate = 0.0

    # Total Production from Project Cost Calculator
    total_production = st.session_state.total_quantity if "total_quantity" in st.session_state else 0.0

    # Total Expenditure and Total Expected Sale
    total_expenditure = total_cost_per_ton * total_production
    total_expected_sale = selling_rate * total_production

    # Profit/Loss
    profit_loss = total_expected_sale - total_expenditure

    # Margin Calculations
    margin_rs_per_ton = selling_rate - total_cost_per_ton
    margin_percentage = (margin_rs_per_ton / selling_rate * 100) if selling_rate > 0 else 0.0

    # Display Insights in Required Format
    st.subheader("Summary")
    st.markdown(f"""
    - **Cost Per Ton:** ₹{total_cost_per_ton:.2f}
    - **Selling Rate:** ₹{selling_rate:.2f}
    - **Total Production:** {total_production:.2f} Tons
    - **Total Expenditure:** ₹{total_expenditure:.2f}
    - **Total Expected Sale:** ₹{total_expected_sale:.2f}
    - **Profit / Loss:** ₹{profit_loss:.2f}
    - **Margin (₹/Ton):** ₹{margin_rs_per_ton:.2f}
    - **Margin (%):** {margin_percentage:.2f}%
    """)

    if total_cost_per_ton > 0:
        # Pie Chart: Cost Distribution
        st.subheader("Cost Distribution")
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        cost_labels = list(st.session_state.calculator_data.keys())
        cost_values = list(st.session_state.calculator_data.values())
        ax1.pie(cost_values, labels=cost_labels, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
        ax1.set_title("Cost Distribution", fontsize=14, color="darkblue")
        st.pyplot(fig1)
