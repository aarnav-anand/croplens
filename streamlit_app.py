import streamlit as st

st.set_page_config(
    page_title="Redirecting to CropLens...",
    page_icon="🌱",
    layout="centered"
)

# Immediate HTML/JS redirection to croplens-web.vercel.app
st.markdown(
    """
    <meta http-equiv="refresh" content="0; url=https://croplens-web.vercel.app">
    <script>
        window.location.replace("https://croplens-web.vercel.app");
    </script>
    <div style="text-align: center; padding: 40px 20px; font-family: system-ui, -apple-system, sans-serif;">
        <h1 style="color: #059669; font-size: 2rem; margin-bottom: 12px;">🌱 CropLens</h1>
        <h3 style="color: #374151; font-weight: 500; margin-bottom: 24px;">Redirecting you to the modern CropLens web app...</h3>
        <p style="color: #6b7280; font-size: 15px; margin-bottom: 20px;">
            If you are not redirected automatically, please click below:
        </p>
        <a href="https://croplens-web.vercel.app" 
           style="display: inline-block; background-color: #059669; color: white; padding: 12px 28px; border-radius: 12px; font-weight: 600; text-decoration: none; font-size: 16px; box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3);">
            Open CropLens Web App →
        </a>
        <p style="color: #9ca3af; font-size: 13px; margin-top: 24px;">
            https://croplens-web.vercel.app
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
