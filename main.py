import streamlit as st

st.set_page_config(page_title="안전계수 및 응력 계산기", layout="centered")

st.title("⚙️ 기계 부품 안전계수 및 응력 계산기")
st.write("하중과 단면적을 입력하여 부품에 걸리는 응력을 계산하고, 재료별로 안전한지 확인해 보세요.")

# 재료별 항복강도 (Yield Strength) 데이터 (단위: MPa)
material_properties = {
    "구조용 강철 (Steel)": 250.0,
    "알루미늄 합금 (Aluminum 6061-T6)": 276.0,
    "티타늄 합금 (Titanium Ti-6Al-4V)": 830.0
}

# 사이드바: 변수 입력 
st.sidebar.header("설계 조건 입력")
force_n = st.sidebar.number_input("작용 하중 (F) [단위: N]", min_value=0.0, value=10000.0, step=500.0)
area_mm2 = st.sidebar.number_input("부품 단면적 (A) [단위: mm²]", min_value=1.0, value=100.0, step=10.0)
selected_material = st.sidebar.selectbox("재료 선택", list(material_properties.keys()))

yield_strength = material_properties[selected_material]

# 물리량 계산
# 응력 (Stress) = 힘 / 단면적 (N/mm² = MPa)
stress = force_n / area_mm2

# 안전계수 (Safety Factor) = 항복강도 / 발생 응력
# 응력이 0일 경우의 에러 방지
if stress > 0:
    safety_factor = yield_strength / stress
else:
    safety_factor = float('inf')

# 결과 출력
st.subheader("📊 계산 결과")
col1, col2, col3 = st.columns(3)
col1.metric("발생 응력", f"{stress:.2f} MPa")
col2.metric("항복 강도", f"{yield_strength:.1f} MPa")

# 안전계수가 무한대(inf)가 아닐 때만 숫자 표시
if safety_factor == float('inf'):
    col3.metric("안전 계수", "측정 불가")
else:
    col3.metric("안전 계수", f"{safety_factor:.2f}")

# 안전성 평가 로직
st.markdown("---")
st.subheader("🛠️ 안전성 평가")

if stress == 0:
    st.info("하중을 입력해 주세요.")
elif safety_factor >= 2.0:
    st.success("✅ 안전합니다! (안전계수 2.0 이상: 충분한 설계 여유가 있습니다.)")
elif safety_factor >= 1.0:
    st.warning("⚠️ 주의! (파괴되지는 않지만, 안전 여유가 부족합니다. 기계 설계에서는 보통 2.0 이상을 권장합니다.)")
else:
    st.error("🚨 위험! (발생 응력이 항복강도를 초과하여 부품에 영구적인 변형이나 파괴가 일어납니다.)")
