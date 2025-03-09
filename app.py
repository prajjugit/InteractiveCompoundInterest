import streamlit as st
import math
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Compound Interest Goal Calculator",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Compound Interest Goal Calculator")
st.markdown("*Calculate how long it will take to reach your financial goals with compound interest*")
    
# Initializing session state if not already set
if "P" not in st.session_state:
    st.session_state.P = 1000
if "r" not in st.session_state:
    st.session_state.r = 5.0
if "A_target" not in st.session_state:
    st.session_state.A_target = 10000000
if "compound_frequency" not in st.session_state:
    st.session_state.compound_frequency = 365  # Default to daily

# Function to update values from inputs
def update_from_input_P():
    st.session_state.P_slider = st.session_state.P_input
    st.session_state.P = st.session_state.P_input

def update_from_slider_P():
    st.session_state.P_input = st.session_state.P_slider
    st.session_state.P = st.session_state.P_slider

def update_from_input_r():
    st.session_state.r_slider = st.session_state.r_input
    st.session_state.r = st.session_state.r_input

def update_from_slider_r():
    st.session_state.r_input = st.session_state.r_slider
    st.session_state.r = st.session_state.r_slider

def update_from_input_A_target():
    st.session_state.A_target_slider = st.session_state.A_target_input
    st.session_state.A_target = st.session_state.A_target_input

def update_from_slider_A_target():
    st.session_state.A_target_input = st.session_state.A_target_slider
    st.session_state.A_target = st.session_state.A_target_slider

def calculate_growth_data(principal, rate, compound_frequency, days):
    """Calculate growth data for visualization"""
    results = []
    current_date = datetime.now()
    
    # Convert annual rate to the rate per compounding period
    rate_per_period = rate / 100 / (compound_frequency / 365)
    
    amount = principal
    for day in range(0, int(days) + 1, max(1, int(days / 100))):  # Sample points for smoother graph
        if day > 0:
            # Calculate compound interest for the period
            periods = day * (compound_frequency / 365)
            amount = principal * (1 + rate_per_period) ** periods
        
        future_date = current_date + timedelta(days=day)
        results.append({
            "Day": day,
            "Date": future_date.strftime("%Y-%m-%d"),
            "Amount": round(amount, 2),
            "Progress": min(100, (amount / st.session_state.A_target) * 100)
        })
    
    return pd.DataFrame(results)

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Calculator", "Visualization", "Comparison"])

with tab1:
    # Create columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Principal Amount
        st.number_input("Principal Amount (₹)", min_value=500, max_value=500000, value=st.session_state.P, step=500, key="P_input", on_change=update_from_input_P)
        st.slider("Adjust Principal", 100, 500000, st.session_state.P, 500, key="P_slider", on_change=update_from_slider_P)
        
        # Interest Rate
        st.number_input("Interest Rate (%)", min_value=0.1, max_value=50.0, value=st.session_state.r, step=0.1, key="r_input", on_change=update_from_input_r)
        st.slider("Adjust Interest Rate", 0.1, 50.0, st.session_state.r, 0.1, key="r_slider", on_change=update_from_slider_r)
        
        # Compounding Frequency
        compound_options = {
            "Daily (365/year)": 365,
            "Weekly (52/year)": 52,
            "Monthly (12/year)": 12,
            "Quarterly (4/year)": 4,
            "Semi-annually (2/year)": 2,
            "Annually (1/year)": 1
        }
        selected_compound = st.selectbox(
            "Compounding Frequency",
            options=list(compound_options.keys()),
            index=0  # Default to daily
        )
        st.session_state.compound_frequency = compound_options[selected_compound]
        
        # Target Amount
        st.number_input("Target Amount (₹)", min_value=1000, max_value=500000000, value=st.session_state.A_target, step=100000, key="A_target_input", on_change=update_from_input_A_target)
        st.slider("Adjust Target Amount", 1000, 500000000, st.session_state.A_target, 100000, key="A_target_slider", on_change=update_from_slider_A_target)
    
    with col2:
        st.subheader("Results")
        
        # Use updated session state values
        P = st.session_state.P
        r = st.session_state.r
        A_target = st.session_state.A_target
        compound_frequency = st.session_state.compound_frequency
        
        # Calculate Time to Reach Target
        if P > 0 and r > 0:
            # Adjust the formula based on compounding frequency
            rate_per_period = r / 100 / (compound_frequency / 365)
            periods = math.log(A_target / P) / math.log(1 + rate_per_period)
            days = periods / (compound_frequency / 365)
            
            years = days / 365
            months = (days % 365) / 30
            remaining_days = days % 30
            
            # Display results in a more visual way
            st.markdown("### Time to Reach Your Goal")
            
            # Create metrics for key values
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Initial Investment", f"₹{P:,.2f}")
            col_b.metric("Target Amount", f"₹{A_target:,.2f}")
            col_c.metric("Interest Rate", f"{r:.2f}% ({selected_compound})")
            
            # Display time in different formats
            st.markdown(f"#### 📅 Estimated Time Required:")
            st.markdown(f"""
            - **{days:.1f}** days
            - **{days/7:.1f}** weeks
            - **{days/30:.1f}** months
            - **{days/365:.2f}** years
            """)
            
            # Format as years, months, days
            years_int = int(years)
            months_int = int(months)
            days_int = int(remaining_days)
            
            time_str = ""
            if years_int > 0:
                time_str += f"**{years_int}** years"
            if months_int > 0:
                time_str += f", **{months_int}** months"
            if days_int > 0 or (years_int == 0 and months_int == 0):
                time_str += f", **{days_int}** days"
            
            st.markdown(f"#### 🗓️ In other words: {time_str.strip(', ')}")
            
            # Calculate the future date
            future_date = datetime.now() + timedelta(days=days)
            st.markdown(f"#### 📆 Target date: **{future_date.strftime('%B %d, %Y')}**")
            
            # Progress visualization
            if P < A_target:
                progress = P / A_target * 100
                st.progress(progress / 100)
                st.caption(f"You're currently at {progress:.2f}% of your goal")
            else:
                st.success("🎉 Congratulations! Your principal already exceeds your target amount.")
            
            # Calculate data for visualization
            growth_data = calculate_growth_data(P, r, compound_frequency, days)
            
        else:
            st.error("Please enter valid positive values for Principal and Interest Rate!")

with tab2:
    # Use updated session state values
    P = st.session_state.P
    r = st.session_state.r
    A_target = st.session_state.A_target
    compound_frequency = st.session_state.compound_frequency
    
    if P > 0 and r > 0:
        # Calculate time to reach target
        rate_per_period = r / 100 / (compound_frequency / 365)
        periods = math.log(A_target / P) / math.log(1 + rate_per_period)
        days = periods / (compound_frequency / 365)
        
        # Calculate growth data
        growth_data = calculate_growth_data(P, r, compound_frequency, days)
        
        st.subheader("Growth Visualization")
        
        # Create line chart
        fig = px.line(
            growth_data, 
            x="Day", 
            y="Amount",
            title=f"Growth of ₹{P:,.2f} at {r}% Interest ({selected_compound})",
            labels={"Amount": "Amount (₹)", "Day": "Days"},
            color_discrete_sequence=["#0068c9"]
        )
        
        # Add target line
        fig.add_hline(
            y=A_target, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Target: ₹{A_target:,.2f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show milestone table
        st.subheader("Key Milestones")
        
        milestones = [0.25, 0.5, 0.75, 1.0]
        milestone_data = []
        
        for milestone in milestones:
            milestone_amount = P + milestone * (A_target - P)
            milestone_periods = math.log(milestone_amount / P) / math.log(1 + rate_per_period)
            milestone_days = milestone_periods / (compound_frequency / 365)
            milestone_date = datetime.now() + timedelta(days=milestone_days)
            
            milestone_data.append({
                "Milestone": f"{int(milestone * 100)}%",
                "Amount": f"₹{milestone_amount:,.2f}",
                "Days Required": f"{milestone_days:.1f}",
                "Estimated Date": milestone_date.strftime("%B %d, %Y")
            })
        
        st.table(pd.DataFrame(milestone_data))
        
        # Add download option for growth data
        csv = growth_data.to_csv(index=False)
        st.download_button(
            label="Download Growth Data as CSV",
            data=csv,
            file_name="compound_interest_growth.csv",
            mime="text/csv",
            help="Download the detailed growth data as a CSV file"
        )
    else:
        st.error("Please enter valid positive values for Principal and Interest Rate!")

with tab3:
    st.subheader("Compare Different Scenarios")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create comparison scenarios
        st.markdown("#### Adjust Comparison Parameters")
        
        # Interest rate comparison
        base_rate = r
        rate_min = st.number_input("Minimum Interest Rate (%)", min_value=0.1, max_value=50.0, value=max(0.1, base_rate-2), step=0.1)
        rate_max = st.number_input("Maximum Interest Rate (%)", min_value=0.1, max_value=50.0, value=min(50.0, base_rate+2), step=0.1)
        num_rates = st.number_input("Number of comparison points", min_value=2, max_value=5, value=3, step=1)
        compare_rates = np.linspace(rate_min, rate_max, num_rates)
        
        # Show selected rates
        st.caption(f"Comparing rates: {', '.join([f'{rate:.1f}%' for rate in compare_rates])}")
        
        # Principal comparison
        compare_principal = st.checkbox("Compare different principal amounts", value=False)
        if compare_principal:
            principal_min = st.number_input("Minimum Principal Multiplier", min_value=0.5, max_value=1.0, value=0.5, step=0.1)
            principal_max = st.number_input("Maximum Principal Multiplier", min_value=1.0, max_value=2.0, value=1.5, step=0.1)
            num_principals = st.number_input("Number of principal points", min_value=2, max_value=3, value=3, step=1)
            principal_multiplier = np.linspace(principal_min, principal_max, num_principals)
            st.caption(f"Comparing principal multipliers: {', '.join([f'{m:.1f}x' for m in principal_multiplier])}")
        
        # Compounding frequency comparison
        compare_frequency = st.checkbox("Compare different compounding frequencies", value=True)
    
    with col2:
        # Generate comparison data
        comparison_data = []
        
        # Base values
        base_P = st.session_state.P
        base_A_target = st.session_state.A_target
        
        # Compare interest rates
        for rate in compare_rates:
            # For each compounding frequency if selected
            if compare_frequency:
                frequencies = [1, 4, 12, 365]  # Annual, quarterly, monthly, daily
                freq_names = ["Annual", "Quarterly", "Monthly", "Daily"]
            else:
                frequencies = [st.session_state.compound_frequency]
                freq_names = [selected_compound.split(" ")[0]]
            
            # For each principal if selected
            if compare_principal:
                principals = [base_P * m for m in principal_multiplier]
            else:
                principals = [base_P]
            
            for p_idx, principal in enumerate(principals):
                for f_idx, freq in enumerate(frequencies):
                    # Calculate time to reach target
                    rate_per_period = rate / 100 / (freq / 365)
                    try:
                        periods = math.log(base_A_target / principal) / math.log(1 + rate_per_period)
                        days = periods / (freq / 365)
                        years = days / 365
                        
                        # Skip if result is infinity or too large
                        if not math.isfinite(days) or days > 36500:  # Cap at 100 years
                            continue
                            
                        # Create scenario name
                        scenario = f"{rate:.2f}% "
                        if compare_principal:
                            scenario += f"(₹{principal:,.0f}) "
                        if compare_frequency:
                            scenario += f"({freq_names[f_idx]})"
                        
                        comparison_data.append({
                            "Scenario": scenario,
                            "Interest Rate": rate,
                            "Principal": principal,
                            "Compounding": freq_names[f_idx],
                            "Days Required": days,
                            "Years Required": years,
                            "Target Amount": base_A_target
                        })
                    except (ValueError, ZeroDivisionError):
                        continue
        
        # Create DataFrame and sort by days
        if comparison_data:
            df_comparison = pd.DataFrame(comparison_data)
            df_comparison = df_comparison.sort_values("Days Required")
            
            # Create bar chart
            fig = px.bar(
                df_comparison,
                x="Scenario",
                y="Years Required",
                title="Time to Reach Target: Scenario Comparison",
                color="Interest Rate",
                hover_data=["Principal", "Compounding", "Days Required"],
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display comparison table
            st.subheader("Detailed Comparison")
            
            # Format the table for display
            display_df = df_comparison.copy()
            display_df["Principal"] = display_df["Principal"].apply(lambda x: f"₹{x:,.2f}")
            display_df["Target Amount"] = display_df["Target Amount"].apply(lambda x: f"₹{x:,.2f}")
            display_df["Interest Rate"] = display_df["Interest Rate"].apply(lambda x: f"{x:.2f}%")
            display_df["Days Required"] = display_df["Days Required"].apply(lambda x: f"{x:.1f}")
            display_df["Years Required"] = display_df["Years Required"].apply(lambda x: f"{x:.2f}")
            
            # Reorder and select columns for display
            display_df = display_df[["Scenario", "Principal", "Interest Rate", "Compounding", "Days Required", "Years Required"]]
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("No valid comparison scenarios found. Try adjusting your parameters.")

# Footer
st.markdown("---")
st.markdown("""
### How Compound Interest Works
Compound interest is calculated using the formula: A = P(1 + r/n)^(nt), where:
- A = Final amount
- P = Principal (initial investment)
- r = Annual interest rate (decimal)
- n = Number of times compounded per year
- t = Time in years

To solve for time (t), we rearrange the formula: t = log(A/P) / [n * log(1 + r/n)]
""")

# Add a sidebar with additional information
with st.sidebar:
    st.header("About This Calculator")
    st.markdown("""
    This calculator helps you determine how long it will take to reach your financial goals through compound interest.
    
    **Features:**
    - Calculate time to reach target amount
    - Visualize growth over time
    - Compare different interest rates and scenarios
    - Track milestones along the way
    
    **Tips:**
    - Higher interest rates dramatically reduce the time needed
    - More frequent compounding slightly improves results
    - Small increases in your initial investment can make a big difference
    """)
    
    st.markdown("---")
    st.caption("Created with Streamlit • v1.0")
