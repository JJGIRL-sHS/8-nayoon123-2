import streamlit as st
import pandas as pd
import json

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

@st.fragment(run_every="0.3s")
def control_traffic():
    
    if st.session_state.current_distance is None:
        return
    
    # 임계값보다 현재 측정 거리가 작다면 사람이 있다고 판단합니다.

    if st.session_state.current_distance < st.session_state.threshold :
        ser = st.session_state.ser
        if ser and ser.is_open:
            payload = {
                "type": "led",
                "status": "on",
            }

            message = json.dumps(payload) + "\n"
            ser.write(message.encode())
            st.toast("LED를 켰습니다.")

    else:
        ser = st.session_state.ser
        if ser and ser.is_open:
            payload = {
                "type": "led",
                "status": "off",
            }

            message = json.dumps(payload) + "\n"
            ser.write(message.encode())
            st.toast("LED를 껐습니다.")


if is_auto:
    control_traffic()

