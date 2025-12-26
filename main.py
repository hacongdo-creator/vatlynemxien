import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Vật Lí AI - Khám phá chuyển động", page_icon="🏀", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; border-radius: 20px;
        background: linear-gradient(45deg, #00f2ff, #0066ff);
        color: white; font-weight: bold; border: none; height: 3.5em; font-size: 18px;
    }
    .step-card {
        background-color: #1e2130;
        padding: 20px; border-radius: 15px;
        border-left: 5px solid #00f2ff;
        margin-bottom: 20px;
    }
    .step-number {
        background-color: #00f2ff; color: #1e2130;
        padding: 2px 8px; border-radius: 50%;
        font-weight: bold; margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Phòng Thí Nghiệm Vật Lí AI")

# 2. THANH ĐIỀU KHIỂN SIDEBAR
st.sidebar.title("⚙️ Cấu hình thí nghiệm")
OPTIONS = ["🏟️ Ném từ mặt đất", "🏀 Ném bóng rổ (Độ cao h)"]
mode = st.sidebar.selectbox("🌟 Chọn chế độ ném", OPTIONS)

h0, target_x, target_y = 0.0, 10.0, 3.05

with st.sidebar.expander("📝 Nhập số liệu thí nghiệm", expanded=True):
    v0 = st.number_input("⚡ Vận tốc đầu v0 (m/s)", 1.0, 50.0, 12.0, 0.1)
    angle = st.number_input("📐 Góc ném (độ)", 0.0, 90.0, 45.0, 0.1)
    if mode == OPTIONS[1]:
        h0 = st.number_input("🧍 Chiều cao tay ném (m)", 0.0, 5.0, 2.0, 0.1)
        target_x = st.number_input("🚩 Khoảng cách rổ (m)", 1.0, 50.0, 8.0, 0.1)
        target_y = st.number_input("🥅 Chiều cao rổ (m)", 0.5, 5.0, 3.05, 0.05)

# --- PHẦN HƯỚNG DẪN KHÁM PHÁ THEO BƯỚC (DYNAMIC) ---
st.markdown("### 📖 Lộ trình khám phá dành cho học sinh")

if mode == OPTIONS[0]:
    # Hướng dẫn cho chế độ ném mặt đất
    with st.container():
        st.markdown(f"""
        <div class="step-card">
            <p><span class="step-number">1</span> <b>Thiết lập lực:</b> Hãy thử chỉnh vận tốc <b>v0 = 15m/s</b> và <b>Góc = 30°</b> ở bảng bên trái.</p>
            <p><span class="step-number">2</span> <b>Dự đoán:</b> Nhìn đường nét đứt màu đỏ trên đồ thị. Bạn đoán bóng sẽ bay xa bao nhiêu mét?</p>
            <p><span class="step-number">3</span> <b>Thực hiện:</b> Nhấn nút <b>BẮT ĐẦU NÉM</b> để kiểm tra dự đoán của mình.</p>
            <p><span class="step-number">4</span> <b>Thử thách:</b> Giữ nguyên v0, thay đổi Góc ném thành <b>45°</b> rồi <b>60°</b>. Ở góc nào bóng bay xa nhất?</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Hướng dẫn cho chế độ ném rổ
    with st.container():
        st.markdown(f"""
        <div class="step-card">
            <p><span class="step-number">1</span> <b>Thông số mục tiêu:</b> Chỉnh <b>Khoảng cách rổ = 8m</b> và <b>Chiều cao rổ = 3.05m</b>.</p>
            <p><span class="step-number">2</span> <b>Ước lượng:</b> Thay đổi <b>v0</b> và <b>Góc</b> sao cho đường nét đứt màu đỏ đi xuyên qua vành rổ màu đỏ.</p>
            <p><span class="step-number">3</span> <b>Ghi điểm:</b> Nhấn <b>BẮT ĐẦU NÉM</b>. Nếu lệch, hãy quan sát bóng rơi ngắn hay quá đà để điều chỉnh vận tốc.</p>
            <p><span class="step-number">4</span> <b>Nâng cao:</b> Thử thay đổi <b>Chiều cao tay ném (h)</b> của bạn học sinh và xem góc ném có cần thay đổi không?</p>
        </div>
        """, unsafe_allow_html=True)

# 3. TÍNH TOÁN VẬT LÝ
g = 9.8
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)
t_flight = (vy0 + np.sqrt(vy0**2 + 2 * g * h0)) / g
t_steps = np.linspace(0, t_flight, num=60)
x = vx0 * t_steps
y = h0 + vy0 * t_steps - 0.5 * g * t_steps**2
v_instant = np.sqrt(vx0**2 + (vy0 - g * t_steps)**2)

# 4. ĐỒ THỊ
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Dự báo',
                         line=dict(color='#FF0000', width=2, dash='dash'),
                         customdata=np.stack((v_instant, t_steps), axis=-1),
                         hovertemplate="<b>Tầm xa:</b> %{x:.2f} m<br><b>Độ cao:</b> %{y:.2f} m<br><b>Vận tốc:</b> %{customdata[0]:.2f} m/s<extra></extra>"))
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='lines', name='Đã ném',
                         line=dict(color='#00f2ff', width=4), hoverinfo='skip'))
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='Bóng',
                         marker=dict(color='#FF6600', size=18, line=dict(color='white', width=2)), hoverinfo='skip'))

# Vẽ nhân vật màu xanh cải tiến và rổ
p_color = "#00f2ff"
if mode == OPTIONS[1]:
    # Vẽ bạn học sinh
    fig.add_shape(type="line", x0=0, y0=0.1, x1=0, y1=h0-0.6, line=dict(color=p_color, width=8))
    fig.add_shape(type="circle", x0=-0.15, y0=h0-0.25, x1=0.15, y1=h0+0.1, fillcolor=p_color, line=dict(color=p_color))
    fig.add_shape(type="line", x0=0, y0=h0-0.5, x1=0.35, y1=h0, line=dict(color=p_color, width=5))
    # Vẽ chân
    fig.add_shape(type="line", x0=0, y0=0.1, x1=-0.2, y1=-0.4, line=dict(color=p_color, width=5))
    fig.add_shape(type="line", x0=0, y0=0.1, x1=0.2, y1=-0.4, line=dict(color=p_color, width=5))
    # Vẽ rổ
    fig.add_shape(type="line", x0=target_x, y0=0, x1=target_x, y1=target_y, line=dict(color="#555", width=4))
    fig.add_trace(go.Scatter(x=[target_x], y=[target_y], mode='markers', name='Rổ',
                             marker=dict(size=22, color='red', symbol='circle-open', line=dict(width=3)), hoverinfo='none'))

fig.update_layout(
    xaxis=dict(range=[-1, max(x) + 2], title="Tầm xa (m)", gridcolor='#333'),
    yaxis=dict(range=[-0.5, max(y) + 2], title="Độ cao (m)", gridcolor='#333'),
    template="plotly_dark",
    updatemenus=[{
        "type": "buttons", "showactive": False, "x": 0.5, "y": -0.2, "xanchor": "center",
        "buttons": [{
            "label": "🚀 BẮT ĐẦU NÉM",
            "method": "animate",
            "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]
        }]
    }]
)

# Cấu hình Frames
frames = [go.Frame(data=[go.Scatter(x=x, y=y), go.Scatter(x=x[:i+1], y=y[:i+1]), go.Scatter(x=[x[i]], y=[y[i]])]) for i in range(len(t_steps))]
fig.frames = frames

st.plotly_chart(fig, use_container_width=True)

# 5. KẾT QUẢ
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
        st.warning(f"⚠️ Bóng lệch rổ {error:.2f} m.")
