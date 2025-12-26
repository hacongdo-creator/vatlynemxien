import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="AI Physics Pro", page_icon="🏀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; border-radius: 20px;
        background: linear-gradient(45deg, #FF3131, #FF914D);
        color: white; font-weight: bold; border: none; height: 3.5em;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 Mô phỏng Ném bóng AI")
st.write("Quỹ đạo dự đoán màu đỏ nét đứt. Nhấn nút để bắt đầu ném.")

# 2. THANH ĐIỀU KHIỂN
st.sidebar.title("⚙️ Cấu hình ném")
OPTIONS = ["🏟️ Ném từ mặt đất", "🏀 Ném bóng rổ (Độ cao h)"]
mode = st.sidebar.selectbox("🌟 Chọn chế độ", OPTIONS)

with st.sidebar.expander("📝 Thông số vật lý", expanded=True):
    v0 = st.number_input("⚡ Vận tốc đầu v0 (m/s)", 1.0, 50.0, 12.0, 0.1)
    angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 0.1)
    if mode == OPTIONS[1]:
        h0 = st.number_input("🧍 Chiều cao ném (m)", 0.0, 5.0, 2.0, 0.1)
        target_x = st.number_input("🚩 Khoảng cách rổ (m)", 1.0, 50.0, 8.0, 0.1)
        target_y = st.number_input("🥅 Chiều cao rổ (m)", 0.5, 5.0, 3.05, 0.05)
    else:
        h0 = 0.0

g = 9.8

# 3. TÍNH TOÁN VẬT LÝ
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)
t_flight = (vy0 + np.sqrt(vy0**2 + 2 * g * h0)) / g

# Tạo 60 khung hình cho chuyển động thực tế
t_steps = np.linspace(0, t_flight, num=60)
x = vx0 * t_steps
y = h0 + vy0 * t_steps - 0.5 * g * t_steps**2

# 4. KHỞI TẠO ĐỒ THỊ
fig = go.Figure()

# Lớp 1: Quỹ đạo dự đoán (MÀU ĐỎ NÉT ĐỨT)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Dự đoán',
                         line=dict(color='#FF0000', width=2, dash='dash')))

# Lớp 2: Quỹ đạo thực tế (Màu Xanh Neon - Sẽ vẽ ra khi bóng bay qua)
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='lines', name='Đã đi qua',
                         line=dict(color='#00f2ff', width=4)))

# Lớp 3: Quả bóng
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='Bóng',
                         marker=dict(color='#FF6600', size=18, line=dict(color='white', width=2))))

# Thêm rổ
if mode == OPTIONS[1]:
    fig.add_trace(go.Scatter(x=[target_x], y=[target_y], mode='markers', name='Rổ',
                             marker=dict(size=15, color='red', symbol='circle-open', line=dict(width=3))))

# 5. THIẾT LẬP NÚT VÀ ANIMATION
fig.update_layout(
    xaxis=dict(range=[0, max(x) + 2], title="Tầm xa (m)", gridcolor='#333'),
    yaxis=dict(range=[0, max(y) + 2], title="Độ cao (m)", gridcolor='#333'),
    template="plotly_dark",
    updatemenus=[{
        "type": "buttons",
        "showactive": False,
        "x": 0.5, "y": -0.2, "xanchor": "center",
        "buttons": [{
            "label": "🚀 BẮT ĐẦU NÉM",
            "method": "animate",
            "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]
        }]
    }]
)

# Tạo khung hình chuyển động (Cập nhật đường dẫn màu xanh chạy theo bóng)
frames = []
for i in range(len(t_steps)):
    frames.append(go.Frame(data=[
        go.Scatter(x=x, y=y),             # Giữ nguyên đường đỏ nét đứt
        go.Scatter(x=x[:i+1], y=y[:i+1]),   # Đường xanh Neon vẽ dần ra
        go.Scatter(x=[x[i]], y=[y[i]])      # Quả bóng
    ]))

fig.frames = frames

st.plotly_chart(fig, use_container_width=True)

# 6. KẾT QUẢ
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("📏 Tầm xa", f"{max(x):.2f} m")
c2.metric("🔝 Độ cao max", f"{max(y):.2f} m")
c3.metric("⏱️ Thời gian", f"{t_flight:.2f} s")

if mode == OPTIONS[1]:
    idx = (np.abs(x - target_x)).argmin()
    error = abs(y[idx] - target_y)
    if error < 0.4:
        st.balloons()
        st.success("🎯 TUYỆT VỜI! Bóng đã vào rổ.")
    else:
        st.warning(f"⚠️ Chưa chính xác. Lệch {error:.2f}m")
