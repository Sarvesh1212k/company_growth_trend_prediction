

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import plotly.express as px
import yfinance as yf
import re
import urllib.parse


def save_session():
    # Placeholder for session saving logic
    pass

def show(user_dict):
    st.header("📊 Company Growth Dashboard")

    # ----------------- SESSION INIT -----------------
    if "dashboard_link" not in user_dict:
        user_dict["dashboard_link"] = ""
    if "dashboard_df" not in user_dict:
        user_dict["dashboard_df"] = None
    if "dashboard_symbol" not in user_dict:
        user_dict["dashboard_symbol"] = None
    if "dashboard_name" not in user_dict:
        user_dict["dashboard_name"] = None
    if "dashboard_history" not in user_dict:
        user_dict["dashboard_history"] = []

    # ----------------- INPUT -----------------
    link = st.text_input(
        "Paste Yahoo Finance Company Link:",
        value=user_dict["dashboard_link"],
        key="dashboard_link_input"
    )

    # Clear state if input empty
    if link.strip() == "":
        user_dict["dashboard_link"] = ""
        user_dict["dashboard_df"] = None
        user_dict["dashboard_symbol"] = None
        user_dict["dashboard_name"] = None
        save_session()

    def extract_symbol_from_link(_link: str):
        decoded_link = urllib.parse.unquote(_link)
        match = re.search(r"quote/([A-Za-z0-9\.\-\=]+)/?", decoded_link)
        return match.group(1) if match else None

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_financial_data(symbol: str):
        try:
            ticker = yf.Ticker(symbol)
            try:
                info = ticker.info or {}
            except Exception:
                info = {}
            company_name = info.get("shortName", symbol)

            # ✅ Try financials first, then fallback to income_stmt
            financials = ticker.financials.T
            if financials is None or financials.empty:
                financials = ticker.income_stmt.T

            if financials is None or financials.empty:
                return None, company_name

            # Debug info (see what Yahoo returns)
            # st.write("DEBUG: Available columns →", list(financials.columns))

            # ✅ Handle multiple possible column names
            possible_revenue = ["Total Revenue", "TotalRevenue", "Revenue"]
            possible_profit = ["Gross Profit", "GrossProfit", "Operating Income", "Net Income"]

            revenue = None
            for col in possible_revenue:
                if col in financials.columns:
                    revenue = financials[col]
                    break

            profit = None
            for col in possible_profit:
                if col in financials.columns:
                    profit = financials[col]
                    break

            if revenue is None or profit is None:
                return None, company_name

            if isinstance(revenue.index, pd.DatetimeIndex):
                years = revenue.index.year
            else:
                base_year = datetime.now().year - len(revenue) + 1
                years = np.array([base_year + i for i in range(len(revenue))])

            df_local = pd.DataFrame({
                "Year": years.astype(int),
                "Revenue": pd.to_numeric(revenue.values, errors="coerce"),
                "Profit": pd.to_numeric(profit.values, errors="coerce")
            }).dropna()

            df_local = df_local.sort_values("Year").reset_index(drop=True)
            return df_local, company_name
        except Exception:
            return None, symbol

    def format_number(num: float) -> str:
        sign = "-" if num < 0 else ""
        n = abs(float(num))
        if n >= 1e9:
            return f"{sign}{n/1e9:.1f}B"
        elif n >= 1e7:
            return f"{sign}{n/1e7:.1f}CR"
        elif n >= 1e5:
            return f"{sign}{n/1e5:.1f}L"
        elif n >= 1e3:
            return f"{sign}{n/1e3:.1f}K"
        else:
            return f"{sign}{int(n)}"

    # ----------------- FETCH DATA -----------------
    if link and link != user_dict["dashboard_link"]:
        # New link entered
        user_dict["dashboard_link"] = link
        try:
            get_financial_data.clear()
        except Exception:
            pass
        symbol = extract_symbol_from_link(link)
        if not symbol:
            st.error("⚠️ Could not extract company symbol from link. Please check the URL.")
            user_dict["dashboard_df"] = None
            user_dict["dashboard_symbol"] = None
            user_dict["dashboard_name"] = None
            save_session()
        else:
            with st.spinner("⏳ Fetching company financials..."):
                df, name = get_financial_data(symbol)
            user_dict["dashboard_symbol"] = symbol
            user_dict["dashboard_name"] = name
            user_dict["dashboard_df"] = df
            user_dict["dashboard_history"].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "name": name,
                "link": link
            })
            save_session()

    # ✅ Reload after refresh if df missing but link exists
    if user_dict["dashboard_link"] and user_dict["dashboard_df"] is None:
        symbol = extract_symbol_from_link(user_dict["dashboard_link"])
        if symbol:
            with st.spinner("⏳ Reloading company financials..."):
                df, name = get_financial_data(symbol)
            user_dict["dashboard_symbol"] = symbol
            user_dict["dashboard_name"] = name
            user_dict["dashboard_df"] = df

    # ----------------- SHOW DATA -----------------
    df = user_dict.get("dashboard_df")
    symbol = user_dict.get("dashboard_symbol")
    name = user_dict.get("dashboard_name")

    if symbol:
        st.success(f"✅ Company Symbol: **{symbol}**")
    if name:
        st.info(f"🏢 Company Name: **{name}**")

    if df is not None and not df.empty:
        st.subheader("📈 Revenue Over Years")
        fig1 = px.bar(df, x="Year", y="Revenue", text=[format_number(v) for v in df["Revenue"]])
        fig1.update_xaxes(type="category")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("💰 Profit Over Years")
        fig2 = px.line(df, x="Year", y="Profit", markers=True, text=[format_number(v) for v in df["Profit"]])
        fig2.update_traces(textposition="top center")
        fig2.update_xaxes(type="category")
        st.plotly_chart(fig2, use_container_width=True)

        predicted_dashboard(df)
    elif link:
        st.error("⚠️ No financial data found for this company.")

# ---------------- Predicted Dashboard ----------------
def predicted_dashboard(df: pd.DataFrame):
    st.subheader("🔮 Predicted Revenue & Profit Dashboard")

    def predict_future(df_in: pd.DataFrame, column="Revenue", years_ahead=1) -> pd.DataFrame:
        years = df_in["Year"].values.reshape(-1, 1)
        values = df_in[column].values.reshape(-1, 1)
        mask = ~np.isnan(values).flatten() & np.isfinite(values).flatten()
        years = years[mask]
        values = values[mask]
        if len(values) == 0:
            return pd.DataFrame(columns=["Year", "Prediction"])
        model = LinearRegression()
        model.fit(years, values)
        future_years = np.arange(df_in["Year"].max() + 1, df_in["Year"].max() + years_ahead + 1).reshape(-1, 1)
        predictions = model.predict(future_years).flatten()
        return pd.DataFrame({"Year": future_years.flatten(), "Prediction": predictions.astype(int)})

    def format_number(num: float) -> str:
        sign = "-" if num < 0 else ""
        n = abs(float(num))
        if n >= 1e9:
            return f"{sign}{n/1e9:.1f}B"
        elif n >= 1e7:
            return f"{sign}{n/1e7:.1f}CR"
        elif n >= 1e5:
            return f"{sign}{n/1e5:.1f}L"
        elif n >= 1e3:
            return f"{sign}{n/1e3:.1f}K"
        else:
            return f"{sign}{int(n)}"

    revenue_future = predict_future(df, "Revenue", 1)
    profit_future = predict_future(df, "Profit", 1)

    if revenue_future.empty or profit_future.empty:
        st.warning("⚠️ Not enough valid data to predict.")
        return

    st.markdown(f"""
        <div style='display:flex; justify-content:space-around; margin-top:20px; gap:16px;'>
            <div style='background:linear-gradient(135deg,#89f7fe,#66a6ff); padding:20px; border-radius:15px; width:45%; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.2);'>
                <h3>📈 Predicted Revenue (Next Year)</h3>
                <h2 style='color:#004080;'>{format_number(float(revenue_future['Prediction'].iloc[-1]))}</h2>
            </div>
            <div style='background:linear-gradient(135deg,#f6d365,#fda085); padding:20px; border-radius:15px; width:45%; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.2);'>
                <h3>💰 Predicted Profit (Next Year)</h3>
                <h2 style='color:#803300;'>{format_number(float(profit_future['Prediction'].iloc[-1]))}</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)