import streamlit as st
import pandas as pd

def run_project_cost_calculator():
    st.header("Project Cost Calculator")

    # Cost Components Input
    cost_inputs = [
        "Mining Cost",
        "Royalty",
        "Transport Cost",
        "Crushing Cost",
        "Loading Cost",
        "Office Cost",
        "Departmental Expense",
        "Land Rent",
        "Miscellaneous Expense",
    ]

    # Initialize a dictionary to store cost inputs
    if "calculator_data" not in st.session_state:
        st.session_state.calculator_data = {cost: 0.0 for cost in cost_inputs}

    # Display inputs in table-like format using a loop
    st.subheader("Enter Costs (₹/Ton)")
    for cost in cost_inputs:
        st.session_state.calculator_data[cost] = st.number_input(
            f"{cost}", min_value=0.0, format="%.2f", value=st.session_state.calculator_data[cost]
        )

    # Custom Cost Input
    st.subheader("Add Custom Cost Component")
    custom_cost_name = st.text_input("Enter Custom Cost Name")
    custom_cost_value = st.number_input("Enter Custom Cost Value (₹/Ton)", min_value=0.0, format="%.2f")

    if st.button("Add Custom Cost"):
        if custom_cost_name:
            st.session_state.calculator_data[custom_cost_name] = custom_cost_value
            st.success(f"Custom cost '{custom_cost_name}' added successfully!")
        else:
            st.error("Please enter a name for the custom cost.")

    # Quantity Input
    total_quantity = st.number_input("Enter Total Material Quantity (Tons)", min_value=0.0, format="%.2f")
    st.session_state.total_quantity = total_quantity  # Save total quantity to session state

    # Calculate Total Cost
    if st.button("Calculate Total Project Cost"):
        try:
            total_cost_per_ton = sum(st.session_state.calculator_data.values())
            total_cost = total_cost_per_ton * total_quantity

            # Display Breakdown Table with Total
            st.header("Cost Breakdown")
            breakdown_data = pd.DataFrame({
                "Cost Component": list(st.session_state.calculator_data.keys()) + ["Total"],
                "Cost (₹/Ton)": [f"₹{value:.2f}" for value in st.session_state.calculator_data.values()] + [f"₹{total_cost_per_ton:.2f}"]
            })
            st.table(breakdown_data)

        except Exception as e:
            st.error(f"Error: {e}")
