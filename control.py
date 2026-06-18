import streamlit as st
import json

ser = st.session_state.ser

message = ""
if st.button("On",
             icon=":material/lightbulb:",
             use_container_width=True,
             disabled=(ser is None or not ser.is_open),
             ):
             
    payload = {
        "type": "led",
        "status": "on",
    }
    message = json.dumps(payload) + "\n"
    ser.write(message.encode())

    
if st.button("Off",
             icon=":material/power_off:",
             use_container_width=True,
             disabled=(ser is None or not ser.is_open),
             ):
    payload = {
        "type": "led",
        "status": "off",
    }
    message = json.dumps(payload) + "\n"
    ser.write(message.encode())


if ser and ser.is_open:
    st.subheader("JSON")
    st.code(message, language="json")
