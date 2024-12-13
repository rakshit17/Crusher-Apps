import streamlit as st
from Project_Costing import run_project_cost_calculator
from Average_Rate import run_rate_calculator
from Project_Insights import run_insights

st.title("Crusher Plant Tools")

option = st.sidebar.selectbox(
    "Choose a Tool",
    ["Project Cost Calculator", "Rate Calculator", "Insights"],
)

if option == "Project Cost Calculator":
    run_project_cost_calculator()
elif option == "Rate Calculator":
    run_rate_calculator()
elif option == "Insights":
    run_insights()