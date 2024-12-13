import streamlit as st

class ProjectCostCalculator:
    def __init__(self):
        self.cost_components = {}

    def add_cost(self, cost_name, cost_per_ton):
        """Add a cost component with its value in Rs/Ton."""
        self.cost_components[cost_name] = cost_per_ton

    def calculate_total_cost(self, total_quantity):
        """Calculate the total project cost based on the total quantity in tons."""
        if total_quantity <= 0:
            raise ValueError("Total quantity must be greater than zero.")

        breakdown = {
            name: round(value * total_quantity, 2) for name, value in self.cost_components.items()
        }
        total_cost_per_ton = round(sum(self.cost_components.values()), 2)
        total_project_cost = round(total_cost_per_ton * total_quantity, 2)
        return total_project_cost, breakdown, total_cost_per_ton

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

        return round(total_weighted_rate / total_percentage, 2)

# Initialize calculators in session state
if "project_cost_calculator" not in st.session_state:
    st.session_state.project_cost_calculator = ProjectCostCalculator()

if "weighted_average_calculator" not in st.session_state:
    st.session_state.weighted_average_calculator = WeightedAverageCalculator()

# Streamlit App
st.title("Cost Management Tools")

# Main Menu
option = st.selectbox("Choose a Tool", ["Project Cost Calculator", "Weighted Average Calculator"])

if option == "Project Cost Calculator":
    st.header("Project Cost Calculator (Rs/Ton)")

    # Input Section: Costs
    st.subheader("Enter Cost Components (Rs/Ton)")
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

    for cost_name in cost_inputs:
        cost_value = st.number_input(f"{cost_name} (Rs/Ton)", min_value=0.0, format="%.2f")
        if cost_value > 0:
            st.session_state.project_cost_calculator.add_cost(cost_name, cost_value)

    # Customizable Cost Input
    st.subheader("Add Custom Cost Component")
    custom_cost_name = st.text_input("Enter Custom Cost Name")
    custom_cost_value = st.number_input("Enter Custom Cost Value (Rs/Ton)", min_value=0.0, format="%.2f")
    if st.button("Add Custom Cost"):
        if custom_cost_name:
            st.session_state.project_cost_calculator.add_cost(custom_cost_name, custom_cost_value)
            st.success(f"Added Custom Cost: {custom_cost_name} - ₹{custom_cost_value:.2f} per Ton")
        else:
            st.error("Please enter a name for the custom cost.")

    # Input Section: Total Quantity
    st.subheader("Enter Production Details")
    total_quantity = st.number_input("Total Material Quantity (Tons)", min_value=0.0, format="%.2f")

    # Calculate Total Project Cost
    if st.button("Calculate Total Project Cost"):
        try:
            total_cost, breakdown, total_cost_per_ton = st.session_state.project_cost_calculator.calculate_total_cost(total_quantity)
            st.success(f"The Total Project Cost is: ₹{total_cost:,.2f}")
            st.info(f"The Total Cost Per Ton is: ₹{total_cost_per_ton:.2f}")

            # Display Breakdown Table
            st.header("Cost Breakdown")
            breakdown_table = {
                "Cost Component": list(breakdown.keys()) + ["Total"],
                "Cost (Rs)": [f"₹{value:,.2f}" for value in breakdown.values()] + [f"₹{round(sum(breakdown.values()), 2):,.2f}"]
            }
            st.table(breakdown_table)
        except ValueError as e:
            st.error(e)

    # Display Entered Costs
    if st.session_state.project_cost_calculator.cost_components:
        st.header("Entered Cost Components")
        entered_costs_table = {
            "Cost Component": list(st.session_state.project_cost_calculator.cost_components.keys()) + ["Total"],
            "Cost (Rs/Ton)": [f"₹{value:,.2f}" for value in st.session_state.project_cost_calculator.cost_components.values()] + [f"₹{round(sum(st.session_state.project_cost_calculator.cost_components.values()), 2):,.2f}"]
        }
        st.table(entered_costs_table)

elif option == "Weighted Average Calculator":
    st.header("Weighted Average Calculator")

    # Input Section: Material Details
    st.subheader("Enter Material Details")
    material_type = st.text_input("Material Type")
    rate = st.number_input("Rate (Rs)", min_value=0.0, format="%.2f")
    production_percentage = st.number_input("Production Percentage (%)", min_value=0.0, max_value=100.0, format="%.2f")

    if st.button("Add Material"):
        if material_type and production_percentage > 0:
            st.session_state.weighted_average_calculator.add_material(material_type, rate, production_percentage)
            st.success(f"Added: {material_type} with Rate ₹{rate:.2f} and Production Percentage {production_percentage:.2f}%")
        else:
            st.error("Please provide valid inputs.")

    # Calculate Weighted Average
    if st.button("Calculate Weighted Average"):
        try:
            weighted_average = st.session_state.weighted_average_calculator.calculate_weighted_average()
            st.success(f"The Weighted Average Rate is: ₹{weighted_average:.2f}")
        except ValueError as e:
            st.error(e)

    # Display Entered Materials
    if st.session_state.weighted_average_calculator.materials:
        st.header("Materials Added")
        for i, material in enumerate(st.session_state.weighted_average_calculator.materials, 1):
            st.write(f"{i}. {material['material_type']} - Rate: ₹{material['rate']:.2f}, Production Percentage: {material['production_percentage']:.2f}%")
