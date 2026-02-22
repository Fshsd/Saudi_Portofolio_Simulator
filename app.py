import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

#Streamlit for interface, yfinance for Yahoo Finance data, plotly for interactive charts, pandas for DataFrame , datetime for handling dates and time intervals

st.set_page_config(page_title="Tarmeez Portfolio Simulator", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { 
        background-color: #0e1117; 
    }
    
    [data-testid="stMetricValue"] { 
        color: #f9a602 !important; 
        font-size: 28px; 
    }
    
    [data-testid="stMetricDelta"] { 
        font-size: 16px; 
    }
    
    .stHeader { 
        color: #f9a602; 
    }

    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            filter: brightness(0);
        }
        .main {
            background-color: #ffffff;
        }
    }

    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    
    @media (prefers-color-scheme: light) {
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 محاكي المحفظة الاستثمارية الذكي")
st.markdown("---")

# --- Sidebar: User Inputs & Settings ---

#Logo and settings in the sidebar
st.sidebar.image("img/tarmeezlogo2.png", width=250) 
# st.sidebar.divider()
st.sidebar.header("⚙️ إعدادات الاستثمار")

#user inputs for investment amount and time period
investment_amount = st.sidebar.number_input("رأس المال المستثمر (SAR)", min_value=1000, value=100000, step=1000)
time_period = st.sidebar.selectbox("الفترة الزمنية", ["سنة واحدة", "سنتين", "5 سنوات"])

#dictionary mapping Saudi company names to their Yahoo Finance tickers (ending in .SR)
stock_dict = {
    "مصرف الراجحي": "1120.SR",
    "أرامكو السعودية": "2222.SR",
    "اس تي سي (stc)": "7010.SR",
    "سابك": "2010.SR",
    "البنك الأهلي (SNB)": "1180.SR",
    "معادن": "1211.SR",
    "سلوشنز": "7202.SR",
    "أكوا باور": "2082.SR",
    "كهرباء السعودية": "5110.SR",
    "لوبريف": "2223.SR"
}

#user can select multiple stocks from the sidebar multiselect
selected_stocks = st.sidebar.multiselect(
    "اختر الأسهم لمحفظتك", 
    list(stock_dict.keys()), 
    default=["مصرف الراجحي", "أرامكو السعودية", "سلوشنز"]
)

#calculating start date based on user selection for time period
end_date = datetime.now()
if time_period == "سنة واحدة":
    start_date = end_date - timedelta(days=365)
elif time_period == "سنتين":
    start_date = end_date - timedelta(days=365*2)
else:
    start_date = end_date - timedelta(days=365*5)

# --- Data Processing Section ---

#start data fetching and processing if user has selected stocks
if selected_stocks:
    with st.spinner('جاري تحليل البيانات المالية من السوق...'):
        tickers = [stock_dict[s] for s in selected_stocks]
        # Comparing the selected stocks with the overall market performance (TASI) to see if our portfolio outperforms the market
        all_tickers = tickers + ["^TASI.SR"]
        data = yf.download(all_tickers, start=start_date, end=end_date)['Close']


    if not data.empty:
        # We use an Equal Weight strategy, dividing the total investment equally among all chosen stocks
        weights = 1.0 / len(selected_stocks)
        stock_data = data[tickers]
        tasi_data = data["^TASI.SR"]

        #Normalization because we want all stocks start from 1
        normalized_stocks = stock_data / stock_data.iloc[0]

        # Calculate the total portfolio value based on the initial investment amount
        portfolio_returns = (normalized_stocks * weights).sum(axis=1)
        portfolio_value_series = portfolio_returns * investment_amount

        #same thing for market index
        tasi_returns = (tasi_data / tasi_data.iloc[0]) * investment_amount


        # --- Dashboard Metrics ---

        current_val = portfolio_value_series.iloc[-1] # Current Value
        profit_loss = current_val - investment_amount # Profit or Loss
        profit_pct = (profit_loss / investment_amount) * 100 
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("القيمة الحالية", f"{current_val:,.0f} SAR")
        col2.metric("صافي الربح/الخسارة", f"{profit_loss:,.0f} SAR", f"{profit_pct:.2f}%")
        col3.metric("أعلى قيمة وصل لها", f"{portfolio_value_series.max():,.0f} SAR")
        
        # calculating final return of TASI to compare with our portfolio performance
        tasi_final_return = ((tasi_data.iloc[-1] / tasi_data.iloc[0]) - 1) * 100
        diff = profit_pct - tasi_final_return
        col4.metric("أداء السوق (TASI)", f"{tasi_final_return:.2f}%", f"{diff:.2f}% vs Market")
        
        # --- Visualizations ---

        # Main Line Chart: Tracking portfolio growth vs. the market index
        st.subheader("📈 تتبع نمو المحفظة مقابل مؤشر السوق (TASI)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=portfolio_value_series.index, y=portfolio_value_series, name='محفظتك', line=dict(color='#f9a602', width=3)))
        fig.add_trace(go.Scatter(x=tasi_returns.index, y=tasi_returns, name='مؤشر السوق (TASI)', line=dict(color="#006aff", dash='dash')))
        fig.update_layout(template="plotly_dark", hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader("🥧 توزيع الأصول")
            pie_df = pd.DataFrame({"السهم": selected_stocks, "النسبة": [100/len(selected_stocks)]*len(selected_stocks)})
            fig_pie = px.pie(pie_df, values='النسبة', names='السهم', hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_pie)

        with c2:
            st.subheader("🏆 أفضل الأسهم أداءً في محفظتك")
            individual_returns = ((stock_data.iloc[-1] / stock_data.iloc[0]) - 1) * 100
            perf_df = pd.DataFrame({"السهم": selected_stocks, "العائد (%)": individual_returns.values}).sort_values(by="العائد (%)", ascending=False)
            fig_bar = px.bar(perf_df, x="العائد (%)", y="السهم", orientation='h', color="العائد (%)", color_continuous_scale="Viridis")
            st.plotly_chart(fig_bar)

else:
    # Display warning message if no stocks are selected
    st.warning("⚠️ الرجاء اختيار أسهم من القائمة الجانبية للبدء.")

st.markdown("---")
st.caption("تم تطوير هذا المشروع كجزء من التقييم العملي لشركة ترميز المالية.")