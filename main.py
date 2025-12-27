import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Vật Lí AI - Thí nghiệm ảo", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .step-card {
        background-color: #1e2130; padding: 20px; border-radius: 15px;
        border-left: 5px solid #00f2ff; margin-bottom: 20px;
    }
    .step-number {
        background-color: #00f2ff; color: #1e2130;
        padding: 2px 8px; border-radius: 50%; font-weight: bold; margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 Phòng Thí Nghiệm Vật Lí AI")

# 2. THANH ĐIỀU KHIỂN SIDEBAR
st.sidebar.title("⚙️ Cấu hình thí nghiệm")
MODES = [
    "↕️ 1. Ném theo phương thẳng đứng",
    "➡️ 2. Ném theo phương ngang",
    "🏟️ 3. Ném xiên từ mặt đất",
    "🏀 4. Ném bóng rổ (Mục tiêu)"
]
selected_mode = st.sidebar.selectbox("🌟 Chọn loại chuyển động", MODES)

h0, v0, angle, target_x, target_y = 0.0, 10.0, 45.0, 10.0, 3.05

with st.sidebar.expander("📝 Nhập số liệu thí nghiệm", expanded=True):
    v0 = st.number_input("⚡ Vận tốc đầu v0 (m/s)", 1.0, 50.0, 12.0, 0.5)
    
    if selected_mode == MODES[0]: # 1. Thẳng đứng
        h0 = st.number_input("📏 Độ cao ban đầu (m)", 0.0, 100.0, 10.0, 1.0)
        direction = st.radio("Hướng ném", ["Ném lên trên", "Ném xuống dưới"])
        angle = 90.0 if direction == "Ném lên trên" else -90.0
    elif selected_mode == MODES[1]: # 2. Ném ngang
        h0 = st.number_input("📏 Độ cao ban đầu (m)", 0.5, 100.0, 15.0, 1.0)
        angle = 0.0
    elif selected_mode == MODES[2]: # 3. Ném xiên
        angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 1.0)
        h0 = 0.0
    elif selected_mode == MODES[3]: # 4. Ném rổ
        h0 = st.number_input("🧍 Độ cao tay ném (m)", 0.0, 5.0, 2.0, 0.1)
        angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 1.0)
        target_x = st.number_input("🚩 Khoảng cách rổ (m)", 1.0, 50.0, 8.0, 0.1)
        target_y = st.number_input("🥅 Chiều cao rổ (m)", 0.5, 5.0, 3.05, 0.05)

# --- 3. HƯỚNG DẪN KHÁM PHÁ THEO BƯỚC (PHỤ THUỘC VÀO CHẾ ĐỘ) ---
st.markdown("### 📖 Lộ trình khám phá dành cho học sinh")

if selected_mode == MODES[0]:
    instruct = [
        "<b>Quan sát gia tốc:</b> Chỉnh ném lên từ độ cao 10m. Nhận xét vận tốc thay đổi thế nào khi bóng đạt đỉnh.",
        "<b>So sánh:</b> Ném lên và ném xuống cùng vận tốc v0. Chạm đất bên nào vận tốc lớn hơn?",
        "<b>Nâng cao:</b> Rê chuột vào đường đỏ để xem giây thứ bao nhiêu thì vận tốc bằng 0."
    ]
elif selected_mode == MODES[1]:
    instruct = [
        "<b>Thí nghiệm:</b> Giữ nguyên độ cao 15m, thay đổi vận tốc ném v0.",
        "<b>Khám phá:</b> Quan sát <b>Thời gian rơi</b>. Tại sao v0 tăng mà thời gian rơi không đổi?",
        "<b>Kết luận:</b> Tầm xa tỉ lệ thuận với vận tốc ném ngang v0."
    ]
elif selected_mode == MODES[2]:
    instruct = [
        "<b>Tìm quy luật:</b> Thử ném với các góc 30°, 45°, 60°. Góc nào cho tầm xa lớn nhất?",
        "<b>Đối xứng:</b> So sánh tầm xa khi ném góc 30° và 60°. Bạn có thấy điều gì đặc biệt không?",
        "<b>Soi dữ liệu:</b> Kiểm tra vận tốc tại đỉnh quỹ đạo. Tại đó vận tốc có bằng 0 không?"
    ]
else: # Ném rổ
    instruct = [
        "<b>Ước lượng:</b> Điều chỉnh v0 và Góc sao cho đường dự báo đỏ đi qua vành rổ.",
        "<b>Thực hiện:</b> Nhấn <b>BẮT ĐẦU THÍ NGHIỆM</b> và quan sát bóng bay thực tế.",
        "<b>Tư duy:</b> Nếu bóng rơi ngắn, bạn sẽ tăng vận tốc hay tăng góc ném? Hãy thử cả hai!"
    ]

st.markdown(f"""
<div class="step-card">
    {"".join([f'<p><span class="step-number">{i+1}</span> {text}</p>' for i, text in enumerate(instruct)])}
</div>
""", unsafe_allow_html=True)

# --- 4. TÍNH TOÁN VẬT LÝ THỰC TẾ (60 FPS) ---
g = 9.81
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

if selected_mode == MODES[0] and angle == -90:
    t_flight = (-v0 + np.sqrt(v0**2 + 2*g*h0)) / g
else:
    discriminant = vy0**2 + 2 * g * h0
    t_flight = (vy0 + np.sqrt(max(0, discriminant))) / g

t_steps = np.linspace(0, t_flight, num=120)
x = vx0 * t_steps
if selected_mode == MODES[0]: x = x + 1e-9 
y = np.maximum(h0 + vy0 * t_steps - 0.5 * g * t_steps**2, 0)

vx_t = np.full_like(t_steps, vx0)
vy_t = vy0 - g * t_steps
v_inst = np.sqrt(vx_t**2 + vy_t**2)

# --- 5. ĐỒ THỊ ---
fig = go.Figure()
custom_data = np.stack((v_inst, t_steps, vx_t, vy_t), axis=-1)

# 
fig.add_trace(go.Scatter(
    x=x, y=y, mode='lines', name='Dự báo', 
    line=dict(color='#FF4B4B', width=2, dash='dash'),
    customdata=custom_data,
    hovertemplate="<b>Tầm xa:</b> %{x:.2f} m<br><b>Độ cao:</b> %{y:.2f} m<br><b>Vận tốc:</b> %{customdata[0]:.2f} m/s<br><b>Thời gian:</b> %{customdata[1]:.2f} s<extra></extra>"
))

fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='lines', name='Thực tế', line=dict(color='#00f2ff', width=4), hoverinfo='skip'))
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='Bóng', marker=dict(color='#FF6600', size=16, line=dict(color='white', width=1)), hoverinfo='skip'))

# CHỈ VẼ NGƯỜI VÀ RỔ Ở CHẾ ĐỘ NÉM RỔ
if selected_mode == MODES[3]:
    p_color = "#00f2ff"
    fig.add_shape(type="line", x0=0, y0=max(0, h0-1.5), x1=0, y1=h0-0.5, line=dict(color=p_color, width=6))
    fig.add_shape(type="circle", x0=-0.15, y0=h0-0.4, x1=0.15, y1=h0-0.1, fillcolor=p_color, line=dict(color=p_color))
    fig.add_shape(type="line", x0=0, y0=h0-0.5, x1=0.25 if angle >= 0 else -0.1, y1=h0, line=dict(color=p_color, width=4))
    fig.add_shape(type="line", x0=target_x, y0=0, x1=target_x, y1=target_y, line=dict(color="#555", width=3))
    fig.add_trace(go.Scatter(x=[target_x], y=[target_y], mode='markers', marker=dict(size=20, color='red', symbol='circle-open', line=dict(width=3)), hoverinfo='none'))

fig.update_layout(
    xaxis=dict(range=[-1, max(x) + 5], title="Tầm xa (m)", gridcolor='#333'),
    yaxis=dict(range=[-0.5, max(y) + 5], title="Độ cao (m)", gridcolor='#333'),
    template="plotly_dark", height=500, margin=dict(l=20, r=20, t=20, b=20),
    updatemenus=[{
        "type": "buttons", "showactive": False, "x": 0.5, "y": -0.15, "xanchor": "center",
        "buttons": [{"label": "🚀 BẮT ĐẦU THÍ NGHIỆM", "method": "animate", 
                     "args": [None, {"frame": {"duration": 16, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]}]
    }]
)

fig.frames = [go.Frame(data=[go.Scatter(x=x, y=y), go.Scatter(x=x[:i+1], y=y[:i+1]), go.Scatter(x=[x[i]], y=[y[i]])]) for i in range(len(t_steps))]

st.plotly_chart(fig, use_container_width=True)
st.info("💡 **Gợi ý:** Rê chuột hoặc chạm vào đường nét đứt để SOI thông số vận tốc và thời gian tại điểm đó.")

# 6. KẾT QUẢ
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("📏 Tầm xa tối đa", f"{max(x):.2f} m")
c2.metric("🔝 Độ cao cực đại", f"{max(y):.2f} m")
c3.metric("⏱️ Tổng thời gian", f"{t_flight:.2f} s")

if selected_mode == MODES[3]:
    idx = (np.abs(x - target_x)).argmin()
    if abs(y[idx] - target_y) < 0.4:
        st.balloons()
        st.success("🎯 TUYỆT VỜI! Bóng đã vào rổ.")
