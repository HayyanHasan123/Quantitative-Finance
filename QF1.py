
def npv(cf,r):
    npv = 0
    for i in range(len(cf)):
        pv = cf[i]/(1+r)**i
        npv += pv
    return npv

def irr(cf):
    import numpy_financial as npf
    internal_rr = npf.irr(cf)
    return internal_rr
    

def investment_decision(npv_value, irr_value, req_rate):
    if npv_value > 0 and irr_value > req_rate:
        return "Accept this investment"
    elif npv_value == 0:
        return "We will be at a breakeven with this investment"
    else:
        return "Do not Invest Here!!!"

# ---- Streamlit Interface ---- #
import streamlit as st

st.set_page_config(page_title="IRR & NPV Calculator",layout="centered")

st.title("💸 IRR & NPV Calculator (Investmet Advisor)")
st.markdown("Enter your **cash flows** (negative for outflow, positive for inflows) and the **required rate of return** to evaluate your investment.")

# User input section
cash_flows_input = st.text_input("Enter all Cash Flows (separated by spaces):", "-1000 200 4990 3000 1200 1000")
req_rate = st.number_input("Enter the Required Rate of Return (e.g. 0.1 for 10%):", min_value=0.0, step=0.01, format="%.4f")

# Compute when user clicks button
if st.button("CALCULATE"):
    try:
        cf = list(map(float, cash_flows_input.split()))
        npv_value = npv(cf, req_rate)
        irr_value = irr(cf)
        
        st.success(f"**Net Present Value (NPV):** ${npv_value:,.2f}")
        st.success(f"**Internal Rate of Return (IRR):** {irr_value*100:.2f}%")
        
        decision = investment_decision(npv_value, irr_value, req_rate)
        st.markdown(f"### Investment Decision: {decision}")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by Syed Muhammad Hayyan Hasan")