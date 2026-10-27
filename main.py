import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="동역학 시뮬레이션", layout="centered")

st.title("🚀 공기저항을 고려한 포물선 궤적 시뮬레이터")
st.write("슬라이더를 조절하여 공기저항이 물체의 비행 궤적에 미치는 영향을 확인해 보세요.")

# 사이드바: 변수 입력 
st.sidebar.header("초기 조건 설정")
v0 = st.sidebar.slider("초기 속도 (m/s)", 10.0, 100.0, 50.0)
angle_deg = st.sidebar.slider("발사 각도 (도)", 0.0, 90.0, 45.0)
k = st.sidebar.slider("공기저항 계수 (k)", 0.0, 1.0, 0.1, step=0.05)
m = st.sidebar.slider("물체의 질량 (kg)", 1.0, 10.0, 5.0)
g = 9.81 # 중력가속도

# 각도 변환 (도 -> 라디안)
angle_rad = math.radians(angle_deg)

# 시뮬레이션 초기화
dt = 0.05 # 미소 시간
t = 0.0
x, y = 0.0, 0.0
vx = v0 * math.cos(angle_rad)
vy = v0 * math.sin(angle_rad)

x_list, y_list = [x], [y]

# 지면에 닿을 때(y >= 0)까지 위치 계산 (Euler Method)
while y >= 0:
    # 가속도 계산 (F = ma -> a = F/m)
    ax = -(k / m) * vx
    ay = -g - (k / m) * vy
    
    # 속도 업데이트
    vx += ax * dt
    vy += ay * dt
    
    # 위치 업데이트
    x += vx * dt
    y += vy * dt
    
    t += dt
    
    if y >= 0:
        x_list.append(x)
        y_list.append(y)

# 결과를 데이터프레임으로 변환 후 시각화
df = pd.DataFrame({'x (거리)': x_list, 'y (높이)': y_list})

st.subheader(f"비행 거리: {x_list[-1]:.2f}m | 비행 시간: {t:.2f}초")
st.line_chart(df, x='x (거리)', y='y (높이)')
