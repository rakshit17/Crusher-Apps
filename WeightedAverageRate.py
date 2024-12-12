import streamlit as st

class WeightedAverageCalculator:
    def __init__(self):
        self.materials = []

    def add_material(self, material_type, rate, production_percentage):
        """Add material details to the calculator."""
        self.materials.append({
            'material_type': material_type,
            'rate': rate,
            'production_percentage': production_percentage
        })

    def calculate_weighted_average(self):
        """Calculate the weighted average based on the inputs."""
        if not self.materials:
            raise ValueError("No materials added for calculation.")

        total_weighted_rate = 0
        total_percentage = 0

        for material in self.materials:
            total_weighted_rate += material['rate'] * material['production_percentage']
            total_percentage += material['production_percentage']

        if total_percentage == 0:
            raise ValueError("Total production percentage cannot be zero.")

        return total_weighted_rate / total_percentage


# Initialize calculator in session state
if "calculator" not in st.session_state:
    st.session_state.calculator = WeightedAverageCalculator()

# Streamlit App
st.title("Weighted Average Calculator for Crusher Plants")

# Input Section
st.header("Enter Material Details")
material_type = st.text_input("Material Type")
rate = st.number_input("Rate", min_value=0.0, format="%.2f")
production_percentage = st.number_input("Production Percentage", min_value=0.0, format="%.2f")

if st.button("Add Material"):
    if material_type and production_percentage > 0:
        st.session_state.calculator.add_material(material_type, rate, production_percentage)
        st.success(f"Added: {material_type} with Rate {rate} and Production Percentage {production_percentage}%")
    else:
        st.error("Please provide valid inputs.")

# Calculate Weighted Average
if st.button("Calculate Weighted Average"):
    try:
        weighted_average = st.session_state.calculator.calculate_weighted_average()
        st.success(f"The Weighted Average Rate is: {weighted_average:.2f}")
    except ValueError as e:
        st.error(e)

# Display Materials Added
if st.session_state.calculator.materials:
    st.header("Materials Added")
    for i, material in enumerate(st.session_state.calculator.materials, 1):
        st.write(f"{i}. {material['material_type']} - Rate: {material['rate']}, Production Percentage: {material['production_percentage']}%")
