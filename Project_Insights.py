import streamlit as st
import matplotlib.pyplot as plt

def run_insights():
    st.header("Insights")

    # Ensure data exists for analysis
    if "calculator_data" not in st.session_state or "materials" not in st.session_state:
        st.warning("Please ensure data is entered in both Project Cost Calculator and Rate Calculator.")
        return

    # Total Cost Per Ton from Project Cost Calculator
    total_cost_per_ton = sum(st.session_state.calculator_data.values())

    # Final Rate from Rate Calculator
    if st.session_state.materials:
        total_weighted_rate = sum(
            m["Rate (₹/Ton)"] * m["Production Percentage (%)"] for m in st.session_state.materials
        )
        total_percentage = sum(m["Production Percentage (%)"] for m in st.session_state.materials)
        selling_rate = total_weighted_rate / total_percentage if total_percentage > 0 else 0.0
    else:
        selling_rate = 0.0

    # Margin Calculations
    margin_rs_per_ton = selling_rate - total_cost_per_ton
    margin_percentage = (margin_rs_per_ton / selling_rate * 100) if selling_rate > 0 else 0.0

    # Display Insights
    st.subheader("Summary")
    st.write(f"**Total Cost Per Ton:** ₹{total_cost_per_ton:.2f}")
    st.write(f"**Selling Rate:** ₹{selling_rate:.2f}")
    st.write(f"**Margin (₹/Ton):** ₹{margin_rs_per_ton:.2f}")
    st.write(f"**Margin (%):** {margin_percentage:.2f}%")

    # Pie Chart: Cost Distribution
    st.subheader("Cost Distribution")
    fig1, ax1 = plt.subplots()
    cost_labels = list(st.session_state.calculator_data.keys())
    cost_values = list(st.session_state.calculator_data.values())
    ax1.pie(cost_values, labels=cost_labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig1)

    # Bar Chart: Cost vs Selling Rate
    st.subheader("Cost vs Selling Rate")
    fig2, ax2 = plt.subplots()
    categories = ["Total Cost Per Ton", "Selling Rate"]
    values = [total_cost_per_ton, selling_rate]
    ax2.bar(categories, values, color=["blue", "green"])
    ax2.set_ylabel("₹ per Ton")
    ax2.set_title("Cost vs Selling Rate Comparison")
    st.pyplot(fig2)
