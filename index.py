import streamlit as st
from datetime import date
import plotly.express as px
from SMA import SMABacktester


st.title("Forex Strategy Playground")

if 'data' not in st.session_state:
    st.session_state.data = None

def run_test():
    tester = SMABacktester(currency_pair, SMA_S, SMA_L, start, end)
    tester.test_strategy()
    st.session_state.data = tester.results

def optimize_params():
    tester = SMABacktester(currency_pair, SMA_S, SMA_L, start, end)
    tester.optimize_parameters()
    st.session_state.data = tester.results
    

st.write("Select Currency and Strategy")
col1, col2 = st.columns(2)
currency_mapping = {"Pick a Currency":"1", "EURUSD": "EURUSD=X", "AUDEUR": "AUDEUR=X", "USDGBP": "USDGBP=X"}
currency = col1.selectbox(
    "Select Currency",
    ("Pick a Currency", "EURUSD", "AUDEUR", "USDGBP")
)

if currency != "Pick a Currency":
    currency_pair = currency_mapping[currency]

strategy = col2.selectbox(
    "Select Strategy",
    ("Select a Strategy", "Buy & Hold", "Moving Average Cross"),
    placeholder="Choose an option"
)

with col1.container():
    st.write("Select Start date and End date")
    start = st.date_input("start date", date(2004, 7, 1))
    end = st.date_input("end date", date(2020, 8, 30))


if strategy == "Moving Average Cross":
    with col2.expander("Adjust Strategy"):
        SMA_S = st.number_input("SMA_S", value=None, step=1, placeholder="input value")
        SMA_L = st.number_input("SMA_L", value=None, step=1, placeholder="input value")
        st.button("Set")
        st.button("Find Optimal Setting", type="primary", on_click=optimize_params)

st.button("Run Test", type="primary", on_click=run_test)

if st.session_state.data is not None:
    data = st.session_state.data
    fig = px.line(data, x=data.index, y=['price', 'SMA_S', 'SMA_L'], labels={'value': 'Price'}, title="Forex Price with Moving Average Cross")
    # Customize legend labels
    fig.for_each_trace(lambda trace: trace.update(name={'price': 'Forex Price', 
                                                        'SMA_S': f'{SMA_S}-Day SMA (Short)', 
                                                        'SMA_L': f'{SMA_L}-Day SMA (Long)'}[trace.name]))
    
    fig2 = px.line(data, x=data.index, y=['creturns', 'cstrategy'], labels={'value': 'Price'}, title="Cummulative Returns of Strategy againts Buy and Hold")
    # Customize legend labels
    fig2.for_each_trace(lambda trace: trace.update(name={'creturns': 'Cummulative Returns', 
                                                         'cstrategy': 'Cummulative Strategy Returns'}[trace.name]))

    # Display the Plotly chart in Streamlit
    st.info('Expand chart for full view', icon="ℹ️")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)