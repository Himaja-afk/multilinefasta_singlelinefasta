# streamlit_launcher.py
import streamlit as st
import subprocess
import time

st.set_page_config(page_title="Convert Multi-line FASTA to Single-line FASTA", layout="wide")

st.title("Convert Multi-line FASTA to Single-line FASTA")

# Launch Flask app in the background
if "flask_started" not in st.session_state:
    st.session_state.flask_started = False

if not st.session_state.flask_started:
    st.info("Starting Flask app in the background...")
    # Launch Flask app in a separate process
    subprocess.Popen(["python", "app.py"])
    st.session_state.flask_started = True
    time.sleep(2)  # give Flask some time to start
    st.success("Flask app launched!")

# Embed the Flask app in an iframe
st.markdown(
    """
    <iframe src="http://localhost:5000" width="100%" height="900px" style="border:none;"></iframe>
    """,
    unsafe_allow_html=True
)