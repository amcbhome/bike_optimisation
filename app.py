# app.py

import streamlit as st
import numpy as np
from scipy.optimize import linprog

def solve_linear_program(c, A_ub, b_ub):
    """
    Solves a linear programming problem using scipy's linprog.
    
    Args:
        c (array-like): The coefficients of the objective function to be minimized.
        A_ub (array-like): The inequality constraint matrix.
        b_ub (array-like): The inequality constraint vector.
        
    Returns:
        A tuple containing the optimal values for the variables and the maximum profit.
    """
    # Linprog minimizes by default, so we multiply the objective function coefficients by -1
    c_neg = [-1 * val for val in c]
    
    # Solve the linear program
    result = linprog(c_neg, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
    
    # Extract the results
    optimal_x = result.x
    max_profit = -result.fun
    
    return optimal_x, max_profit

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Mountain and Road Bike Production Optimizer")

    st.write("This app determines the optimal number of mountain and road bikes to produce to maximize profit, given a set of constraints.")

    st.subheader("Problem Definition")
    [cite_start]st.write("A company produces mountain bikes and road bikes[cite: 1].")
    st.write("Profit from mountain bikes: £100")
    st.write("Profit from road bikes: £200")
    [cite_start]st.write("Assembly time for a mountain bike: 3 hours [cite: 1]")
    [cite_start]st.write("Assembly time for a road bike: 4 hours [cite: 1]")
    [cite_start]st.write("Total assembly time available: 60 hours [cite: 2]")
    [cite_start]st.write("The company wants at least twice as many mountain bikes as road bikes[cite: 3].")
    
    # Define the linear programming problem
    # Objective function: Maximize P = 100x + 200y
    c = [100, 200]

    # Constraints:
    # 1. 3x + 4y <= 60
    # 2. x >= 2y  => x - 2y >= 0  => -x + 2y <= 0
    # 3. x >= 0
    # 4. y >= 0
    A_ub = [
        [3, 4],   # Time constraint
        [-1, 2]   # Ratio constraint
    ]
    b_ub = [60, 0]

    st.subheader("Solution")
    
    if st.button("Calculate Optimal Production"):
        try:
            optimal_production, max_profit = solve_linear_program(c, A_ub, b_ub)
            
            mountain_bikes = round(optimal_production[0])
            road_bikes = round(optimal_production[1])
            
            st.success("Calculation complete!")
            st.write(f"To maximize profit, the company should produce:")
            st.write(f"**{mountain_bikes} Mountain Bikes**")
            st.write(f"**{road_bikes} Road Bikes**")
            st.write(f"This will result in a maximum profit of **£{max_profit:.2f}**.")
            
            st.write("---")
            st.write("Breakdown of the solution:")
            st.write(f"**Profit Function:** Maximize P = 100x + 200y")
            st.write("**Constraints:**")
            st.write(f"1. Assembly time: 3x + 4y <= 60")
            st.write(f"2. Production ratio: x >= 2y  (or -x + 2y <= 0)")
            st.write(f"3. Non-negativity: x >= 0, y >= 0")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
