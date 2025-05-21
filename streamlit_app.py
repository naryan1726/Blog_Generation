import streamlit as st
from agents import FinancialAdvisorCrew
from pdf_generator import PDFReportGenerator

def show_personal_info():
    st.header("Personal Information")
    basic_info = {
        'name': st.text_input("Full Name"),
        'age': st.number_input("Age", min_value=18, max_value=100),
        'occupation': st.text_input("Occupation"),
        'marital_status': st.selectbox("Marital Status", 
            ["Single", "Married", "Divorced", "Widowed"]),
        'dependents': st.number_input("Number of Dependents", min_value=0),
        'phone': st.text_input("Phone Number"),
        'salary': st.number_input("Monthly Salary ($)", min_value=0.0, step=100.0),
        'savings': st.number_input("Monthly Savings ($)", min_value=0.0, step=100.0),
        'spendings': st.number_input("Monthly Expenses ($)", min_value=0.0, step=100.0)
    }
    
    st.header("Financial Goals")
    short_term_goals = st.multiselect(
        "Short-term Goals (1-2 years)",
        ["Emergency Fund", "Vacation", "Car Purchase", "Wedding", "Home Renovation", 
         "Debt Repayment", "Education", "Other"]
    )
    
    long_term_goals = st.multiselect(
        "Long-term Goals (5+ years)",
        ["Home Purchase", "Retirement", "Children's Education", "Business Startup",
         "Investment Portfolio", "Early Retirement", "Other"]
    )
    
    financial_goals = {
        'short_term': short_term_goals,
        'short_term_amount': st.number_input("Short-term Goals Target Amount ($)", 
            min_value=0.0, step=1000.0),
        'short_term_timeline': st.number_input("Short-term Goals Timeline (months)", 
            min_value=1, max_value=24),
        'long_term': long_term_goals,
        'long_term_amount': st.number_input("Long-term Goals Target Amount ($)", 
            min_value=0.0, step=5000.0),
        'long_term_timeline': st.number_input("Long-term Goals Timeline (years)", 
            min_value=5, max_value=40)
    }
    
    if st.button("Next →"):
        st.session_state.page = "financial_info"
        st.session_state.basic_info = basic_info
        st.session_state.financial_goals = financial_goals
        st.rerun()

def show_financial_info():
    st.header("Loan Information")
    loan_info = {
        'total_amount': st.number_input("Total Loan Amount ($)", min_value=0.0, step=1000.0),
        'monthly_payment': st.number_input("Monthly Loan Payment ($)", min_value=0.0, step=100.0),
        'interest_rate': st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
    }
    
    st.header("Investment Information")
    investment_types = st.multiselect(
        "Investment Types",
        ["Stocks", "Bonds", "Mutual Funds", "Real Estate", "Cryptocurrency", 
         "Fixed Deposits", "ETFs", "Index Funds", "401(k)", "IRA"]
    )
    investment_info = {
        'types': investment_types,
        'risk_profile': st.select_slider(
            "Risk Profile",
            options=["Conservative", "Moderate-Conservative", "Moderate", 
                    "Moderate-Aggressive", "Aggressive"]
        ),
        'monthly_investment': st.number_input("Monthly Investment Amount ($)", 
            min_value=0.0, step=100.0)
    }

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.page = "personal_info"
            st.rerun()
    with col2:
        if st.button("Generate Report", type="primary"):
            with st.spinner("Creating your financial report..."):
                crew = FinancialAdvisorCrew(
                    st.session_state.basic_info,
                    st.session_state.financial_goals,
                    loan_info,
                    investment_info
                )
                report = crew.run()
                pdf = PDFReportGenerator()
                pdf_file = pdf.create_report(
                    report,
                    basic_info=st.session_state.basic_info,
                    financial_goals=st.session_state.financial_goals
                )
                
                with open(pdf_file, "rb") as file:
                    st.download_button(
                        "📥 Download Financial Report",
                        data=file,
                        file_name="financial_report.pdf",
                        mime="application/pdf"
                    )

def main():
    st.set_page_config(page_title="AI Financial Advisor", page_icon="💰")
    st.title("🤖 AI Financial Advisor")
    
    if "page" not in st.session_state:
        st.session_state.page = "personal_info"
        
    if st.session_state.page == "personal_info":
        show_personal_info()
    else:
        show_financial_info()

if __name__ == "__main__":
    main()