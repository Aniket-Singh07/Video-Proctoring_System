import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.set_page_config(layout="wide")
st.title("Video Proctoring System")

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if not st.session_state.interview_started:
    st.write("Click the button below to start your interview session.")
    if st.button("Start Interview"):
        st.session_state.interview_started = True
        st.rerun()

if st.session_state.interview_started:
    st.success("Your interview session has started. Please look into the camera.")
    
    webrtc_streamer(
        key="live_interview",
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]
        }
    )

    st.warning("Click the button below to end your session.")
    if st.button("Stop Interview"):
        st.session_state.interview_started = False
        st.info("Your interview session has ended. Thank you.")
        # We don't generate a report here, as no processing was done.
        st.rerun()