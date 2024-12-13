import streamlit as st
import pandas as pd

def run_rate_calculator():
    st.header("Rate Calculator")

    # Initialize session state for materials
    if "materials" not in st.session_state:
        st.session_state.materials = []

    # Input Section for Material Details
    st.subheader("Add Material Details")
    material_type = st.text_input("Material Type")
    rate = st.number_input("Rate (₹/Ton)", min_value=0.0, format="%.2f")
    production_percentage = st.number_input("Production Percentage (%)", min_value=0.0, max_value=100.0, format="%.2f")

    if st.button("Add Material"):
        if material_type and rate > 0 and production_percentage > 0:
            st.session_state.materials.append({
                "Material Type": material_type,
                "Rate (₹/Ton)": round(rate, 2),
                "Production Percentage (%)": round(production_percentage, 2),
            })
            st.success(f"Material '{material_type}' added successfully!")
        else:
            st.error("Please provide valid inputs for all fields.")

    # Display Materials Table
    if st.session_state.materials:
        st.subheader("Materials Added")
        materials_df = pd.DataFrame(st.session_state.materials)
        st.table(materials_df.style.format({"Rate (₹/Ton)": "₹{:.2f}", "Production Percentage (%)": "{:.2f}%"}))

    # Calculate Final Rate
    if st.button("Calculate Final Rate"):
        try:
            total_weighted_rate = sum(
                m["Rate (₹/Ton)"] * m["Production Percentage (%)"] for m in st.session_state.materials
            )
            total_percentage = sum(m["Production Percentage (%)"] for m in st.session_state.materials)

            if total_percentage > 0:
                final_rate = total_weighted_rate / total_percentage
                st.success(f"Final Rate: ₹{final_rate:.2f}")
            else:
                st.error("Total production percentage must be greater than 0.")
        except Exception as e:
            st.error(f"Error: {e}")
