import streamlit as st

def show():
    st.markdown("<h2 style='text-align:center; color:#4B0082;'>🏠 Project Overview</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .card-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        margin-top: 20px;
    }
    .card {
        background-color: #f5f5f5;
        border-radius: 12px;
        padding: 20px;
        width: 45%; /* two cards per row */
        min-width: 250px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .card h3 {
        color: #4B0082;
        font-size: 22px;
        margin-bottom: 10px;
    }
    .card p {
        color: #333;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # All 6 cards
    cards_html = """
    <div class="card-container">
        <div class="card">
            <h3>Project Overview</h3>
            <p>Company Dashboard & Growth Prediction System using Python, Streamlit, and MySQL.</p>
        </div>
        <div class="card">
            <h3>Features</h3>
            <p>Multi-user login, secure password handling, dashboards, chat system, and growth predictions.</p>
        </div>
        <div class="card">
            <h3>Technologies</h3>
            <p>Python, Streamlit, MySQL, Pandas, Plotly, scikit-learn, and HTML/CSS,JS.</p>
        </div>
        <div class="card">
            <h3>Navigation</h3>
            <p>Sidebar to explore dashboards, view company data, and interact with features.</p>
        </div>
   
    <div class="card">
    <h3>Data Sources</h3>
    <p>Financial data obtained from Yahoo Finance and company Excel records.</p>
    </div>
    <div class="card">
    <h3>Future Enhancements</h3>
    <p>Expand the system with trend forecasting and automated report generation.</p>
    </div>

    """
    st.markdown(cards_html, unsafe_allow_html=True)

 #     <div class="card">
    #         <h3>Data Sources</h3>
    #         <p>Data from user inputs, company , an.</p>
    #     </div>
    #     <div class="card">
    #         <h3>Future Enhancements</h3>
    #         <p>AI-based analytics, automated reports, and .</p>
    #     </div>
    # </div>