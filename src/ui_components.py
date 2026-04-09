import streamlit as st
import os

# Mapping giữa tên chuyên khoa và file ảnh trong folder map
MAP_MAPPING = {
    "Cơ xương khớp": "co-xuong-khop.png",
    "Da liễu": "da-lieu.png",
    "Nội Tiêu hóa": "noi-tieu-hoa.png",
    "Răng Hàm Mặt": "rang-ham-mat.png",
    "Sản khoa": "san.png",
    "EMERGENCY": None,
}


def render_map_image(chuyen_khoa):
    """Hiển thị bản đồ chỉ đường dựa trên chuyên khoa"""
    if chuyen_khoa in ["KHÁM TỔNG QUÁT", "QUẦY LỄ TÂN"]:
        st.info("**Gợi ý:** Để được hỗ trợ chính xác nhất cho triệu chứng này, mời bạn di chuyển đến **Sảnh chính Tầng 1 (Quầy Lễ Tân)** để nhân viên y tế hướng dẫn trực tiếp.")
        return

    file_name = MAP_MAPPING.get(chuyen_khoa)
    if file_name:
        map_path = os.path.join("map", file_name)
        if os.path.exists(map_path):
            st.write("---")
            st.info(f"**Bản đồ chỉ dẫn tới {chuyen_khoa}:**")
            st.image(
                map_path,
                caption=f"Sơ đồ di chuyển tới {chuyen_khoa}",
                use_container_width=True,
            )
        else:
            st.warning(f"Không tìm thấy file bản đồ: {map_path}")


def render_emergency_path(data):
    st.error("**CẢNH BÁO NGUY HIỂM**")
    st.write(
        data.get("giai_thich_ngan", "Dấu hiệu y tế khẩn cấp, vui lòng không chờ đợi!")
    )
    if st.button(
        "GỌI CẤP CỨU VINMEC (115) NGAY", type="primary", width="stretch"
    ):
        st.error("Đang kết nối tổng đài cấp cứu...")
    st.warning("Hệ thống AI đã tạm khóa luồng tư vấn thông thường để bảo đảm an toàn.")


def render_uncertain_path(data):
    st.warning(
        "**Hệ thống cần thêm thông tin** (Confidence: {:.0f}%)".format(
            data.get("confidence_score", 0) * 100
        )
    )
    st.write(
        "Trợ lý AI chưa đủ dữ kiện để phân khoa chính xác. Bác sĩ AI muốn hỏi bạn:"
    )
    cau_hoi = data.get("cau_hoi_them", "")
    if not cau_hoi:
        cau_hoi = "Vui lòng mô tả chi tiết hơn hoặc chọn các dấu hiệu bạn đang gặp phải bên dưới:"
    st.info(f"*{cau_hoi}*")


def render_happy_path(data):
    chuyen_khoa = data.get("chuyen_khoa")

    if chuyen_khoa == "QUẦY LỄ TÂN":
        st.info("**Hướng dẫn phân luồng:** Vui lòng tới Quầy Lễ Tân để được hỗ trợ trực tiếp.")
        st.write(f"**Lý do:** {data.get('giai_thich_ngan')}")
        
        render_map_image(chuyen_khoa)
            
        if st.button("Đã hiểu / Quay lại", width="stretch"):
            st.info("Vui lòng gõ vào ô chat để bắt đầu một hội thoại mới.")
    else:
        st.success(f"**Chuyên khoa đề xuất:** {chuyen_khoa}")
        st.progress(data.get("confidence_score", 0))
        st.caption(f"Độ tự tin của AI: {data.get('confidence_score', 0) * 100}%")
        st.write(f"**Lý do:** {data.get('giai_thich_ngan')}")

        # Luôn hiển thị sơ đồ đường đi tới chuyên khoa đã được đề xuất
        render_map_image(chuyen_khoa)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("ĐẶT LỊCH KHÁM NGAY", type="primary", width="stretch"):
                st.success("Ghi nhận lịch hẹn!")
        with col2:
            if st.button("Kết quả sai? Sửa triệu chứng", width="stretch"):
                st.info("Vui lòng gõ bổ sung đính chính vào ô chat bên dưới!")


def render_refuse_path(msg):
    st.info(f"**Phản hồi từ AI:** {msg}")


def render_error(error_msg):
    st.error(f"Lỗi hệ thống AI: {error_msg}")


def render_right_sidebar():
    """Injects a custom CSS/HTML right sidebar for instructions and tips"""

    # Clean string for Streamlit markdown
    html_code = (
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');"
        ".right-sidebar-container {"
        "position: fixed;"
        "right: 20px;"
        "top: 70px;"
        "width: 280px;"
        "height: 88vh;"
        "z-index: 999999;"
        "pointer-events: none;"
        "font-family: 'Inter', sans-serif;"
        "}"
        ".sidebar-content-wrapper {"
        "pointer-events: auto;"
        "background: rgba(15, 15, 26, 0.85);"
        "backdrop-filter: blur(24px) saturate(160%);"
        "-webkit-backdrop-filter: blur(24px) saturate(160%);"
        "border: 1px solid rgba(255, 255, 255, 0.08);"
        "border-radius: 20px;"
        "padding: 22px 18px;"
        "height: 100%;"
        "display: flex;"
        "flex-direction: column;"
        "box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);"
        "}"
        ".main-title {"
        "font-size: 1rem;"
        "font-weight: 700;"
        "background: linear-gradient(90deg, #60a5fa, #a78bfa);"
        "-webkit-background-clip: text;"
        "-webkit-text-fill-color: transparent;"
        "margin-bottom: 18px;"
        "text-align: center;"
        "letter-spacing: -0.2px;"
        "}"
        ".guide-section { margin-bottom: 20px; flex: 1; }"
        ".guide-label {"
        "font-size: 0.68rem;"
        "font-weight: 600;"
        "color: #6b7280;"
        "text-transform: uppercase;"
        "letter-spacing: 0.08em;"
        "margin-bottom: 10px;"
        "display: block;"
        "}"
        ".premium-card {"
        "background: rgba(255,255,255,0.04);"
        "border-radius: 12px;"
        "padding: 12px 14px;"
        "margin-bottom: 8px;"
        "border: 1px solid rgba(255,255,255,0.07);"
        "transition: transform 0.2s ease, background 0.2s ease;"
        "}"
        ".premium-card:hover {"
        "transform: translateY(-1px);"
        "background: rgba(255,255,255,0.07);"
        "}"
        ".card-title {"
        "font-weight: 600;"
        "color: #e5e7eb;"
        "font-size: 0.82rem;"
        "margin-bottom: 4px;"
        "display: flex;"
        "align-items: center;"
        "gap: 6px;"
        "}"
        ".card-desc {"
        "color: #9ca3af;"
        "font-size: 0.77rem;"
        "line-height: 1.5;"
        "}"
        ".slider-box {"
        "margin-top: auto;"
        "background: rgba(99,102,241,0.1);"
        "border: 1px solid rgba(99,102,241,0.2);"
        "border-radius: 10px;"
        "padding: 10px 12px;"
        "overflow: hidden;"
        "}"
        ".marquee {"
        "white-space: nowrap;"
        "overflow: hidden;"
        "display: inline-block;"
        "animation: marquee-scroll 12s linear infinite;"
        "}"
        ".marquee span {"
        "display: inline-block;"
        "padding-right: 40px;"
        "color: #818cf8;"
        "font-weight: 500;"
        "font-size: 0.78rem;"
        "}"
        "@keyframes marquee-scroll {"
        "0% { transform: translateX(0); }"
        "100% { transform: translateX(-50%); }"
        "}"
        "@media (max-width: 1400px) {"
        ".right-sidebar-container { display: none; }"
        "}"
        "</style>"
        "<div class='right-sidebar-container'>"
        "<div class='sidebar-content-wrapper'>"
        "<div class='guide-section'>"
        "<span class='guide-label'>Hướng dẫn nhập liệu</span>"
        "<div class='premium-card'>"
        "<div class='card-title'> Mô tả chi tiết</div>"
        "<div class='card-desc'>Hãy nói mô tả bệnh mà mình mắc phải, ví dụ: Tôi bị phát ban đỏ -> AI sẽ chỉ cho bạn tới đúng phòng khoa Da liễu.</div>"
        "</div>"
        "<div class='premium-card'>"
        "<div class='card-title'> Cung cấp ngữ cảnh</div>"
        "<div class='card-desc'>Nhập thêm các triệu chứng đi kèm như sốt, ho, hoặc buồn nôn,... để AI phân loại chính xác hơn.</div>"
        "</div>"
        "<div class='premium-card'>"
        "<div class='card-title'> Câu hỏi ví dụ</div>"
        "<div class='card-desc'>'Tôi bị nổi ban đỏ khắp người và ngứa ngáy, nên đi khám khoa nào?'</div>"
        "</div>"
        "</div>"
        "<div class='slider-box'>"
        "<div class='marquee'>"
        "<span>Số điện thoại cấp cứu: 115</span>"
        "</div>"
        "</div>"
        "</div>"
        "</div>"
    )
    st.markdown(html_code, unsafe_allow_html=True)
