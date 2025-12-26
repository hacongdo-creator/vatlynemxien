import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Cấu hình trang - Sử dụng Emoji để tăng độ thân thiện
st.set_page_config(page_title="AI Physics Pro", page_icon="🏀", layout="centered")

# CSS tùy chỉnh để làm giao diện bắt mắt hơn
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stNumberInput, .stSelectbox {
        border-radius: 10px;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Phòng Thí Nghiệm Vật Lí AI")
st.write("Khám phá thế giới chuyển động thông qua trí tuệ nhân tạo.")

# 2. Bảng điều khiển Sidebar với biểu tượng
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("🎮 Trung tâm điều khiển")

mode = st.sidebar.selectbox("🌟 Chọn chế độ", ["🏟️ Ném từ mặt đất", "🏀 Ném bóng rổ (Độ cao h)"])

with st.sidebar.expander("📝 Nhập thông số chi tiết", expanded=True):
    v0 = st.number_input("⚡ Vận tốc đầu v0 (m/s)", 1.0, 100.0, 15.0, 0.1)
    angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 0.1)
    
    if "Bóng rổ" in mode:
        h0 = st.number_input("🧍 Chiều cao người ném (m)", 0.0, 5.0, 2.0, 0.1)
        target_x = st.number_input("🚩 Khoảng cách rổ (m)", 1.0, 50.0, 10.0, 0.1)
        target_y = st.number_input("🥅 Chiều cao rổ (m)", 0.5, 5.0, 3.05, 0.05)
    else:
        h0 = 0.0

g = 9.8

# 3. Tính toán thuật toán
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)
t_flight = (vy0 + np.sqrt(vy0**2 + 2 * g * h0)) / g
t_range = np.linspace(0, t_flight, num=200)
x = vx0 * t_range
y = h0 + vy0 * t_range - 0.5 * g * t_range**2
v_instant = np.sqrt(vx0**2 + (vy0 - g * t_range)**2)

# 4. Đồ thị Neon hiện đại
fig = go.Figure()

# Thêm vùng không gian (Skyline)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Quỹ đạo bóng',
                         line=dict(color='#00f2ff', width=5, dash='solid'),
                         fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.1)', # Đổ bóng phía dưới
                         customdata=v_instant,
                         hovertemplate="<b>Tầm xa:</b> %{x:.2f}m<br><b>Độ cao:</b> %{y:.2f}m<br><b>Vận tốc:</b> %{customdata:.2f}m/s<extra></extra>"))

if "Bóng rổ" in mode:
    # Điểm ném
    fig.add_trace(go.Scatter(x=[0], y=[h0], mode='markers', name='Người ném',
                             marker=dict(size=12, color='#FF007F', symbol='diamond')))
    # Cái rổ
    fig.add_trace(go.Scatter(x=[target_x], y=[target_y], mode='markers+text', name='Mục tiêu',
                             marker=dict(size=20, color='#FFD700', symbol='circle-open', line=dict(width=3)),
                             text=["RỔ"], textposition="top center"))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Khoảng cách (m)", gridcolor='#333', zeroline=False),
    yaxis=dict(title="Độ cao (m)", gridcolor='#333', zeroline=False),
    font=dict(color="white"),
    margin=dict(l=0, r=0, t=20, b=0),
    hovermode="closest"
)

st.plotly_chart(fig, use_container_width=True)

# 5. Khu vực phân tích dữ liệu AI (Dashboard)
st.markdown("### 📊 Phân tích hệ thống")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📏 Tầm xa", f"{max(x):.2f} m", "Khoảng cách")
with col2:
    st.metric("🔝 Độ cao", f"{max(y):.2f} m", "Đỉnh cao nhất")
with col3:
    st.metric("⏱️ Thời gian", f"{t_flight:.2f} s", "Tổng thời gian")

# Thông báo kết quả thông minh
if "Bóng rổ" in mode:
    idx = (np.abs(x - target_x)).argmin()
    y_at_target = y[idx]
    error = abs(y_at_target - target_y)
    
    if error < 0.3:
        st.balloons() # Hiệu ứng bóng bay khi trúng đích
        st.success("🎯 **AI NHẬN XÉT:** Cú ném hoàn hảo! Bóng đã đi vào rổ.")
    else:
        st.warning(f"⚡ **AI NHẬN XÉT:** Cần điều chỉnh lực hoặc góc. Bóng đang lệch rổ {error:.2f}m.")


st.info("💡 **Mẹo khám phá:** Hãy thử đổi chiều cao ném sang 3.0m (ném từ tầng 2) để xem quỹ đạo thay đổi thế nào!")
