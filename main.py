import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="AI Physics Pro", page_icon="🏀", layout="centered")

# CSS tùy chỉnh để làm giao diện bắt mắt (Neon Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stNumberInput, .stSelectbox { border-radius: 10px; }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Phòng Thí Nghiệm Vật Lí AI")
st.write("Mô phỏng quỹ đạo ném bóng rổ tương tác dành cho THPT.")

# 2. BẢNG ĐIỀU KHIỂN SIDEBAR
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("🎮 Trung tâm điều khiển")

# Sử dụng danh sách cố định để tránh lỗi so khớp chữ tiếng Việt
OPTIONS = ["🏟️ Ném từ mặt đất", "🏀 Ném bóng rổ (Độ cao h)"]
mode = st.sidebar.selectbox("🌟 Chọn chế độ", OPTIONS)

# Khởi tạo các biến mặc định
h0 = 0.0
target_x = 10.0
target_y = 3.05

with st.sidebar.expander("📝 Nhập thông số chi tiết", expanded=True):
    v0 = st.number_input("⚡ Vận tốc đầu v0 (m/s)", 1.0, 100.0, 15.0, 0.1)
    angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 0.1)
    
    # Nếu chọn chế độ ném bóng rổ (mục thứ 2 trong danh sách)
    if mode == OPTIONS[1]:
        h0 = st.number_input("🧍 Chiều cao người ném (m)", 0.0, 5.0, 2.0, 0.1)
        target_x = st.number_input("🚩 Khoảng cách rổ (m)", 1.0, 50.0, 10.0, 0.1)
        target_y = st.number_input("🥅 Chiều cao rổ (m)", 0.5, 5.0, 3.05, 0.05)

g = 9.8

# 3. THUẬT TOÁN TÍNH TOÁN VẬT LÍ
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

# Tính thời gian bay t_flight
# Công thức: h = h0 + vy0*t - 0.5*g*t^2 = 0
discriminant = vy0**2 + 2 * g * h0
if discriminant >= 0:
    t_flight = (vy0 + np.sqrt(discriminant)) / g
else:
    t_flight = 0

t_range = np.linspace(0, t_flight, num=200)
x = vx0 * t_range
y = h0 + vy0 * t_range - 0.5 * g * t_range**2
# Tính vận tốc tức thời tại mỗi điểm
v_instant = np.sqrt(vx0**2 + (vy0 - g * t_range)**2)

# 4. VẼ ĐỒ THỊ NEON
fig = go.Figure()

# Vẽ quỹ đạo (Scatter plot)
fig.add_trace(go.Scatter(
    x=x, y=y, 
    mode='lines', 
    name='Quỹ đạo bóng',
    line=dict(color='#00f2ff', width=5),
    fill='tozeroy', 
    fillcolor='rgba(0, 242, 255, 0.1)',
    customdata=v_instant,
    hovertemplate="<b>Tầm xa:</b> %{x:.2f}m<br><b>Độ cao:</b> %{y:.2f}m<br><b>Vận tốc:</b> %{customdata:.2f}m/s<extra></extra>"
))

# Hiển thị điểm ném và mục tiêu nếu ở chế độ bóng rổ
if mode == OPTIONS[1]:
    # Điểm xuất phát (Người ném)
    fig.add_trace(go.Scatter(x=[0], y=[h0], mode='markers', name='Người ném',
                             marker=dict(size=12, color='#FF007F', symbol='diamond')))
    # Vị trí cái rổ
    fig.add_trace(go.Scatter(x=[target_x], y=[target_y], mode='markers+text', name='Mục tiêu',
                             marker=dict(size=20, color='#FFD700', symbol='circle-open', line=dict(width=3)),
                             text=["RỔ"], textposition="top center"))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Khoảng cách (m)", gridcolor='#333', range=[0, max(x) + 2] if len(x) > 0 else [0, 10]),
    yaxis=dict(title="Độ cao (m)", gridcolor='#333', range=[0, max(y) + 2] if len(y) > 0 else [0, 10]),
    font=dict(color="white"),
    margin=dict(l=0, r=0, t=20, b=0),
    hovermode="closest"
)

st.plotly_chart(fig, use_container_width=True)

# 5. KHU VỰC PHÂN TÍCH KẾT QUẢ
st.markdown("### 📊 Thông số chi tiết từ AI")
col1, col2, col3 = st.columns(3)
col1.metric("📏 Tầm xa", f"{max(x):.2f} m")
col2.metric("🔝 Độ cao max", f"{max(y):.2f} m")
col3.metric("⏱️ Thời gian", f"{t_flight:.2f} s")

# Nhận xét thông minh từ hệ thống
if mode == OPTIONS[1]:
    # Tìm tung độ y khi bóng bay đến hoành độ của rổ
    idx = (np.abs(x - target_x)).argmin()
    y_at_target = y[idx]
    error = abs(y_at_target - target_y)
    
    if error < 0.4: # Khoảng cách sai số chấp nhận được để coi là trúng rổ
        st.balloons()
        st.success("🎯 **AI NHẬN XÉT:** Một cú ném tuyệt vời! Bóng đã đi vào rổ.")
    else:
        st.warning(f"⚡ **AI NHẬN XÉT:** Bóng đang lệch mục tiêu {error:.2f}m. Hãy điều chỉnh góc hoặc lực!")

st.info("💡 **Gợi ý:** Chạm tay vào bất kỳ điểm nào trên quỹ đạo để xem Vận tốc tại thời điểm đó.")