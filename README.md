# IRR & NPV Calculator (Investment Advisor)

# Overview
This project is a simple **Investment Evaluation Tool** built using **Python and Streamlit**. It helps users analyze investment decisions by calculating **Net Present Value (NPV)** and **Internal Rate of Return (IRR)** based on given cash flows and a required rate of return.

# Features
- Calculates **Net Present Value (NPV)**
- Calculates **Internal Rate of Return (IRR)**
- Provides a clear **investment decision** (Accept / Reject / Breakeven)
- Interactive and user-friendly **Streamlit web interface**
- Handles multiple cash flows including initial outflow

# Technologies Used
- Python
- Streamlit
- numpy-financial

# Project Structure
- NPV calculation function
- IRR calculation function
- Investment decision logic
- Streamlit-based user interface

# How It Works
- User enters cash flows (negative for investment, positive for returns)
- User enters required rate of return
- App computes NPV and IRR
- App gives an investment recommendation based on financial rules

# Investment Decision Logic
- Accept investment if NPV > 0 and IRR > Required Rate
- Breakeven if NPV = 0
- Reject investment otherwise

# Installation
- Install required libraries
- Run the Streamlit app

# Required Libraries
- streamlit
- numpy-financial

# How to Run
- Run the Streamlit app using the command line
- Open the local Streamlit URL in your browser

# Example Input
- Cash Flows: -1000 200 4990 3000 1200 1000
- Required Rate of Return: 0.10

# Output
- Net Present Value (NPV)
- Internal Rate of Return (IRR)
- Investment Decision

# Use Case
- Finance students
- Investment analysis practice
- Capital budgeting projects
- Learning financial decision-making using Python

# Author
- Syed Muhammad Hayyan Hasan

# Disclaimer
This tool is for educational purposes only and should not be used as professional financial advice.
