# Dành cho Agent/Thành viên: Leader / Project Manager

# Lịch sử commit gợi ý:"feat: integrate AI triage & Streamlit UI for Demo"

import streamlit as st
import time
import json
from ai_engine import get_triage_result, transcribe_audio_bytes
from ui_components import (
    render_emergency_path,
    render_uncertain_path,
    render_happy_path,
    render_error,
    render_refuse_path,
    render_right_sidebar,
)

st.set_page_config(page_title="V-Triage AI", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Page background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Main content max-width centering ── */
.block-container {
    max-width: 780px !important;
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
}

/* ── App title & subtitle ── */
h1 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 4px !important;
}
[data-testid="stMarkdown"] em {
    color: #6b7280 !important;
    font-size: 0.82rem !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 12px 0 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: rgba(96, 165, 250, 0.08) !important;
}
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background: rgba(255,255,255,0.03) !important;
}

/* ── Success / Warning / Error / Info banners ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    font-size: 0.9rem !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    border-radius: 99px !important;
}
[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 99px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    height: 44px !important;
    min-height: 44px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}
[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #d1d5db !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(255,255,255,0.22) !important;
}

/* ── Input bar: text + mic + send ── */
div[data-testid="stTextInput"] input {
    height: 44px !important;
    min-height: 44px !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #f3f4f6 !important;
    font-size: 0.92rem !important;
    padding: 0 16px !important;
    transition: border-color 0.2s ease !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #6b7280 !important;
}
div[data-testid="stAudioInput"],
div[data-testid="stAudioInput"] > div,
div[data-testid="stAudioInput"] > div > div {
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stAudioInput"] button {
    height: 44px !important;
    width: 44px !important;
    min-height: 44px !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
    flex-shrink: 0 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stAudioInput"] button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.22) !important;
}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

/* ── Form submit button ── */
[data-testid="stFormSubmitButton"] button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    height: 44px !important;
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p {
    color: #9ca3af !important;
    font-size: 0.86rem !important;
}

/* ── Caption / small text ── */
[data-testid="stCaptionContainer"] {
    color: #6b7280 !important;
    font-size: 0.78rem !important;
}

/* ── Warning / error message tweaks ── */
.stWarning, .stError, .stSuccess, .stInfo {
    border-radius: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("V-TRIAGE · TRỢ LÝ SÀNG LỌC VINMEC")
st.markdown(
    "*Hệ thống AI chỉ mang tính chất hỗ trợ gợi ý — không thay thế chẩn đoán của bác sĩ.*"
)
# Render right sidebar instructions
render_right_sidebar()
st.write("---")

# Mảng lưu lịch sử chat đơn giản
if "messages" not in st.session_state:
    st.session_state.messages = []
if "draft_input" not in st.session_state:
    st.session_state.draft_input = ""
if "pending_draft_text" not in st.session_state:
    st.session_state.pending_draft_text = None
if "last_audio_sig" not in st.session_state:
    st.session_state.last_audio_sig = None

if st.session_state.pending_draft_text is not None:
    st.session_state.draft_input = st.session_state.pending_draft_text
    st.session_state.pending_draft_text = None


def submit_prompt_from_input(show_warning=False):
    candidate = st.session_state.draft_input.strip()
    if candidate:
        st.session_state.messages.append({"role": "user", "content": candidate})
        st.session_state.pending_draft_text = ""
        return candidate
    if show_warning:
        st.warning("Vui lòng nhập hoặc nói triệu chứng trước khi gửi.")
    return None


for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        # Chỉ render giao diện rich UI (như nút bấm, form chọn) cho câu hỏi Bác Sĩ cuối cùng
        if msg["role"] == "assistant" and idx == len(st.session_state.messages) - 1:
            try:
                data = json.loads(msg["content"])
                khoa = data.get("chuyen_khoa")
                conf = float(data.get("confidence_score", 0))

                if data.get("error"):
                    st.markdown(msg.get("display"))
                elif khoa == "EMERGENCY":
                    render_emergency_path(data)
                elif khoa == "TỪ CHỐI":
                    render_refuse_path(
                        data.get("giai_thich_ngan", "Yêu cầu bị từ chối.")
                    )
                elif khoa == "UNKNOWN" or conf < 0.7:
                    render_uncertain_path(data)

                    # Hiện form gợi ý triệu chứng thay vì bắt user gõ
                    options = data.get("cac_lua_chon_goi_y", [])
                    if options:
                        with st.form(key=f"symptom_form_{idx}"):
                            selected = st.multiselect(
                                "Vui lòng đánh dấu các triệu chứng có liên quan:",
                                options,
                            )
                            if st.form_submit_button("Gửi lựa chọn", type="primary"):
                                if selected:
                                    ans = (
                                        "Tôi gặp các triệu chứng bổ sung: "
                                        + ", ".join(selected)
                                    )
                                else:
                                    ans = "Tôi không gặp triệu chứng nào ở trên."
                                st.session_state.messages.append(
                                    {"role": "user", "content": ans}
                                )
                                st.rerun()
                else:
                    render_happy_path(data)
            except:
                st.markdown(msg.get("display", msg["content"]))
        else:
            # Các tin nhắn lịch sử thì chỉ hiển thị chữ gọn nhẹ
            st.markdown(msg.get("display", msg["content"]))

# Thanh nhập: text + mic + gửi trên cùng 1 hàng
input_cols = st.columns([11, 1, 1], vertical_alignment="center")
with input_cols[0]:
    st.text_input(
        "Mô tả chi tiết triệu chứng của bạn",
        key="draft_input",
        placeholder="Ví dụ: Tôi bị đau răng khôn",
        label_visibility="collapsed",
        on_change=submit_prompt_from_input,
    )
with input_cols[1]:
    audio_input = st.audio_input("Mic", label_visibility="collapsed")
with input_cols[2]:
    submitted = st.button("➤", type="primary", width="stretch", help="Gửi")

if audio_input is not None:
    audio_bytes = audio_input.getvalue()
    audio_sig = hash(audio_bytes)
    if audio_sig != st.session_state.last_audio_sig:
        with st.spinner("Đang chuyển giọng nói thành văn bản..."):
            transcribed = transcribe_audio_bytes(audio_bytes)

        if "error" in transcribed:
            st.warning("Không thể chuyển giọng nói: " + transcribed["error"])
        else:
            st.session_state.pending_draft_text = transcribed.get("text", "")
            st.toast("Đã điền nội dung nói vào ô prompt.")

        st.session_state.last_audio_sig = audio_sig
        st.rerun()

submitted_input = None
if submitted:
    submitted_input = submit_prompt_from_input(show_warning=True)

# Xử lý Trigger AI
if (
    len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):
    # Nếu tin nhắn user vừa được add qua ô nhập (chưa đc render trong vòng for), thì vẽ tạm ra
    if submitted_input:
        with st.chat_message("user"):
            st.markdown(submitted_input)

    with st.chat_message("assistant"):
        with st.spinner("AI đang phân tích triệu chứng..."):
            result = get_triage_result(st.session_state.messages)
            time.sleep(1)  # Fake loading

            raw_json_str = json.dumps(result, ensure_ascii=False)

            if "error" in result:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(
                            {"chuyen_khoa": "TỪ CHỐI", "error": result["error"]}
                        ),
                        "display": "Lỗi: " + result["error"],
                    }
                )
            else:
                khoa = result.get("chuyen_khoa")
                if khoa == "EMERGENCY":
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": raw_json_str,
                            "display": f"**[CẢNH BÁO NGUY HIỂM]** {result.get('giai_thich_ngan', '')}",
                        }
                    )
                elif khoa == "TỪ CHỐI":
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": raw_json_str,
                            "display": f"{result.get('giai_thich_ngan', '')}",
                        }
                    )
                elif (
                    khoa == "UNKNOWN" or float(result.get("confidence_score", 0)) < 0.7
                ):
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": raw_json_str,
                            "display": f"{result.get('cau_hoi_them', '')}",
                        }
                    )
                else:
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": raw_json_str,
                            "display": f"Gợi ý khoa: **{khoa}** - {result.get('giai_thich_ngan', '')}",
                        }
                    )

            st.rerun()  # Refresh màn hình để kích hoạt vòng lặp vẽ rich UI ở trên cùng form checkbox
