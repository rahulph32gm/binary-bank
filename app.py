import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

# --- 1. CLEAN BACKEND IMPORT ENGINE ---
# --- 1. CLEAN BACKEND IMPORT ENGINE ---
import sys
import os

# Ensuring local path lookup structure
try:
    import main
    Bank = main.Bank
except Exception as e:
    st.error(f"❌ Core engine configuration error: {str(e)}")
    st.info("💡 Solution: Ensure 'main.py' contains the 'Bank' class and has no internal code syntax compilation drops.")
    st.stop()  # Standard Streamlit execution halts if backend core fails

# Page Configuration
st.set_page_config(page_title="Binary Bank (BB)", page_icon="🏦", layout="centered")

# Backend Instance setup
if 'bank' not in st.session_state:
    st.session_state.bank = Bank()

bank = st.session_state.bank

# --- 2. UI SIDEBAR NAVIGATION ---
st.sidebar.title("🏦 BB Navigation")
menu = ["Home", "📜 T&C", "🆕 Create Account", "💸 Transactions", "🔍 View Details", "⚙️ Update/Delete", "📊 Admin Analytics"]
choice = st.sidebar.radio("Go to", menu)

if choice == "Home":
    st.title("Welcome to Binary Bank (BB) 🙏🏻")
    st.markdown("---")
    st.write("Hubballi's most secure digital bank powered by OOPs.")
    st.image("https://img.icons8.com/clouds/200/bank.png")
    st.info("Navigate through the sidebar to explore our services.")

elif choice == "📜 T&C":
    st.subheader("Terms and Conditions")
    for key, rule in Bank.tc_rules.items():
        st.write(f"✅ {rule}")

elif choice == "🆕 Create Account":
    st.subheader("Fill details to join BB Society")
    with st.form("reg_form", clear_on_submit=True):
        f_name = st.text_input("First Name (as in Identity Card)")
        l_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth", min_value=datetime(1950,1,1), max_value=datetime.today())
        pin = st.number_input("Set 4-Digit PIN", min_value=1000, max_value=9999)
        email = st.text_input("Email (@gmail.com)")
        phone = st.text_input("Phone Number")
        gender = st.selectbox("Gender", ["M", "F", "O"])
        
        if st.form_submit_button("Register"):
            if bank.valid_mail(email) and bank.valid_contect(phone):
                info = {
                    "First_Name": f_name, 
                    "Last_Name": l_name,
                    "DOB": dob.strftime("%d-%m-%Y"), 
                    "PIN": int(pin),
                    "Email": email, 
                    "Phone_num": int(phone),
                    "gender": gender
                }
                acc_no = bank.creatAccount_logic(info)
                st.success(f"🎉 Account Created Successfully! Your A/C No: {acc_no}")
                st.balloons()
            else:
                st.error("❌ Validation Failed! Please check Email or Phone format.")

elif choice == "💸 Transactions":
    st.subheader("Deposit or Withdraw")
    acc_no = st.number_input("Enter Account Number", step=1)
    pin_no = st.number_input("Enter PIN", min_value=1000, max_value=9999, step=1)
    
    if st.button("Verify Account"):
        user = bank.varification_logic(acc_no, pin_no)
        if user:
            st.session_state.current_user = user
            st.success(f"Verified: Namaste {user['First_Name']}!")
        else:
            st.error("Invalid Account Number or PIN")

    if 'current_user' in st.session_state:
        user = st.session_state.current_user
        st.write(f"**Current Balance:** ₹{user['Balance']}")
        
        t_type = st.selectbox("Transaction Type", ["Deposit", "Withdraw"])
        amt = st.number_input("Amount", min_value=1.0)
        
        if st.button("Confirm Transaction"):
            if t_type == "Deposit":
                if amt <= 50000:
                    user["Balance"] += amt
                    bank._Bank__update()
                    st.success(f"₹{amt} Deposited! New Balance: ₹{user['Balance']}")
                else: st.warning("Deposit limit is ₹50,000")
            else:
                if amt <= 25000 and amt <= user["Balance"]:
                    user["Balance"] -= amt
                    bank._Bank__update()
                    st.success(f"₹{amt} Withdrawn! Remaining: ₹{user['Balance']}")
                else: st.error("Insufficient Funds or Limit Exceeded (Max ₹25,000)")

elif choice == "🔍 View Details":
    st.subheader("Check Account Statement")
    acc = st.number_input("A/C Number", step=1)
    p = st.number_input("4-Digit PIN", min_value=1000, max_value=9999, step=1)
    
    if st.button("Fetch Details"):
        user = bank.varification_logic(acc, p)
        if user:
            st.write("### Account Summary")
            st.json(user)
        else:
            st.error("Access Denied!")

elif choice == "⚙️ Update/Delete":
    st.subheader("Manage Your Account")
    acc = st.number_input("Enter A/C Number", step=1)
    p = st.number_input("Enter 4-Digit PIN", min_value=1000, max_value=9999, step=1)
    
    if acc and p:
        user = bank.varification_logic(acc, p)
        if user:
            st.success(f"Verified: {user['First_Name']}")
            
            st.markdown("### 📝 Update Details")
            st.info(bank.tc_rules["update_policy"])
            
            with st.form("update_form"):
                new_mail = st.text_input("New Email", value=user["Email"])
                new_phone = st.text_input("New Phone", value=str(user["Phone_num"]))
                new_pin = st.number_input("New PIN", min_value=1000, max_value=9999, value=user["PIN"])
                
                if st.form_submit_button("Save Changes"):
                    if bank.valid_mail(new_mail) and bank.valid_contect(new_phone):
                        user["Email"] = new_mail
                        user["Phone_num"] = int(new_phone)
                        user["PIN"] = int(new_pin)
                        bank._Bank__update()
                        st.success("✅ Details Updated Successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Format!")

            st.markdown("---")
            
            st.markdown("### ⚠️ Danger Zone")
            if st.button("❌ Delete My Account"):
                Bank._Bank__data.remove(user)
                bank._Bank__update()
                st.warning("Account Deleted! Redirecting...")
                st.balloons()
                st.rerun()
        else:
            st.error("Invalid Credentials")

elif choice == "📊 Admin Analytics":
    st.subheader("Bank Performance Insights")
    df = pd.DataFrame(Bank._Bank__data)
    
    if not df.empty:
        total_val = df['Balance'].sum()
        st.metric("Total Bank Deposits", f"₹{total_val}")
        
        fig = px.pie(df, names='gender', title='Gender Distribution')
        st.plotly_chart(fig)
        
        fig2 = px.histogram(df, x="Age", title="User Age Groups")
        st.plotly_chart(fig2)
    else:
        st.warning("No data available for analytics.")
