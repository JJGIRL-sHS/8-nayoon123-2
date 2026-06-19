import streamlit as st
import json
import serial

ser = st.session_state.ser

if st.button("On",
             icon=":material/lightbulb:",
             use_container_width=True,
             disabled=(ser is None or not ser.is_open),
             ):
    payload = {
        "type": "led",
        "status": "on",
    }
    try:
        ser.write((json.dumps(payload) + "\n").encode())
        st.session_state.led_status = "on"
        st.session_state.last_command = json.dumps(payload, ensure_ascii=False)
    except serial.SerialException:
        st.session_state.ser = None
        st.warning("아두이노 연결이 끊어졌습니다.")


if st.button("Off",
             icon=":material/power_off:",
             use_container_width=True,
             disabled=(ser is None or not ser.is_open),
             ):
    payload = {
        "type": "led",
        "status": "off",
    }
    try:
        ser.write((json.dumps(payload) + "\n").encode())
        st.session_state.led_status = "off"
        st.session_state.last_command = json.dumps(payload, ensure_ascii=False)
    except serial.SerialException:
        st.session_state.ser = None
        st.warning("아두이노 연결이 끊어졌습니다.")


if ser and ser.is_open:
    st.subheader("JSON")
    st.code(st.session_state.last_command, language="json")
