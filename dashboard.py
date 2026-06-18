from datetime import datetime

import streamlit as st
import pandas as pd
import json
import serial

STALE_AFTER = 2.0   # 초: 마지막 센서 수신이 이보다 오래되면 "오래된 값"으로 간주


def _is_fresh():
    last = st.session_state.get("last_update")
    return last is not None and (datetime.now() - last).total_seconds() <= STALE_AFTER


@st.fragment(run_every="0.3s")
def display_data():

    if not st.session_state.sonar_data:
        return
    
    df = pd.DataFrame(st.session_state.sonar_data)
    
    if "time" in df.columns:
        df = df.set_index("time")
    
    if "distance" in df.columns:
        df["distance_ma"] = df["distance"].rolling(window=20).mean()

    df = df.tail(60)

    df_plot = df[["distance", "distance_ma"]].copy()
    df_plot = df_plot.rename(columns={
        "distance" : "거리",
        "distance_ma": "이동 평균"
    })

    st.line_chart(
        df_plot, 
        color=["#989898", "#8917E0"], 
        y_label="cm"
    )
    
    current_value = df["distance"].values[-1]
    max_value = df["distance"].max()
    min_value = df["distance"].min()
    avg_value = df["distance"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("현재", current_value)
    col2.metric("최대", max_value)
    col3.metric("최소", min_value)
    col4.metric("평균", f"{avg_value:0.0f}")

    with st.expander("원본 데이터 보기"):
        st.dataframe(df.sort_index(ascending=False))

display_data()


st.session_state.threshold = st.number_input("임계값 (cm)", placeholder="임계값을 입력해주세요.", value=st.session_state.threshold, min_value=1)

is_auto = st.toggle("자동 제어")

def _send_led(status):
    ser = st.session_state.ser
    if not (ser and ser.is_open):
        return
    payload = {"type": "led", "status": status}
    try:
        ser.write((json.dumps(payload) + "\n").encode())
        st.session_state.led_status = status
        st.toast("LED를 켰습니다." if status == "on" else "LED를 껐습니다.")
    except serial.SerialException:
        st.session_state.ser = None
        st.warning("아두이노 연결이 끊어졌습니다.")


@st.fragment(run_every="0.3s")
def control_traffic():

    # [4] 센서 데이터가 오래되면 안전을 위해 LED를 끈다 (fail-safe)
    if not _is_fresh():
        if st.session_state.led_status != "off":
            _send_led("off")
        st.warning("센서 데이터가 오래되었습니다. 안전을 위해 LED를 껐습니다.")
        return

    # 임계값보다 현재 측정 거리가 작다면 사람이 있다고 판단합니다.
    desired = "on" if st.session_state.current_distance < st.session_state.threshold else "off"

    # 상태가 바뀔 때만 전송 (0.3초마다 같은 명령 반복 방지)
    if desired == st.session_state.led_status:
        return

    _send_led(desired)


if is_auto:
    control_traffic()

