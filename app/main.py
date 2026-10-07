import json
import streamlit as st
from core.config import settings
from services.helpdesk_service import HelpdeskService

st.set_page_config(page_title="AI Chat Assistant · Mini Helpdesk", page_icon="🎓", layout="wide")
st.markdown("""<style>
:root { --blue:#2735fe; --ink:#060827; }
.stApp { background:#f0f2fd; color:var(--ink); }
.block-container { max-width:1120px; padding-top:2rem; padding-bottom:5rem; }
h1,h2,h3 { letter-spacing:-.035em; }
[data-testid="stSidebar"] { background:#fff; border-right:1px solid #e4e6f3; }
.brand { font-size:17px; font-weight:750; margin-bottom:24px; }
.brand span { display:inline-block; background:var(--blue); color:#fff; border-radius:10px; padding:8px 10px; margin-right:8px; }
.workspace { color:#4b4d5b; background:#f0f2fd; padding:15px; border-radius:12px; font-size:14px; line-height:1.6; }
.topbar { display:flex; justify-content:space-between; align-items:center; gap:16px; border-bottom:1px solid #dde1f3; padding-bottom:18px; margin-bottom:30px; }
.topbar strong { font-size:21px; letter-spacing:-.03em; }
.topbar small { color:#4b4d5b; display:block; font-size:13px; margin-top:5px; }
.topbar .badge { background:#e4e7ff; color:#2735fe; padding:8px 12px; border-radius:8px; font-size:12px; white-space:nowrap; }
.welcome { text-align:center; padding:40px 10px 28px; }
.welcome .symbol { display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; background:var(--blue); color:#fff; font-size:23px; font-weight:750; border-radius:20px; margin-bottom:22px; box-shadow:0 12px 28px #2735fe25; }
.welcome h1 { font-size:clamp(28px,4vw,42px); line-height:1.2; margin:0 0 14px; }
.welcome p { color:#4b4d5b; font-size:16px; line-height:1.7; max-width:530px; margin:0 auto; }
.section-label { font-size:12px; color:#4b4d5b; font-weight:650; margin:18px 0 12px; }
[data-testid="stChatMessage"] { background:#fff; border:1px solid #e5e8f5; border-radius:16px; padding:22px; margin-bottom:16px; }
[data-testid="stChatInput"] { border-radius:14px; background:#fff; }
.stButton button { min-height:46px; border-radius:10px; border-color:#dfe3f3; background:#fff; color:#060827; }
.stButton button:hover { border-color:#2735fe; color:#2735fe; background:#f8f9ff; }
.stButton button[kind="primary"] { background:#2735fe; color:#fff; border-color:#2735fe; }
.stButton button:focus-visible { outline:3px solid #a9afff; outline-offset:2px; }
[data-testid="stInfo"] { background:#f0f2fd; border-radius:12px; }
@media(max-width:700px) { .block-container { padding-top:1rem; } .welcome { padding:20px 0; } .topbar { align-items:flex-start; } }
</style>""", unsafe_allow_html=True)

CATEGORIES = {"machine_learning":"Machine Learning", "technical":"Lỗi kỹ thuật", "academic":"Học vụ", "other":"Hỗ trợ khác"}
STATUSES = {"answered":"Đã trả lời", "needs_clarification":"Cần thêm thông tin", "escalate":"Cần xác nhận từ người phụ trách", "fallback":"Chưa nhận được câu trả lời"}
SUGGESTIONS = [
    ("01 · Hiểu kiến thức", "Vì sao chỉ fit StandardScaler trên train?"),
    ("02 · Gỡ lỗi code", "Em gặp NameError: X_val_scaled is not defined. Nguyên nhân và cách kiểm tra là gì?"),
    ("03 · Đọc kết quả", "Accuracy cao nhưng recall thấp: em cần kiểm tra gì trước khi kết luận?"),
]

@st.cache_resource
def service():
    return HelpdeskService()

if "history" not in st.session_state:
    st.session_state.history = []

def clear_history():
    st.session_state.history = []

def choose_question(prompt):
    st.session_state.pending_question = prompt

with st.sidebar:
    st.markdown('<div class="brand"><span>AI</span> Student Helpdesk</div>', unsafe_allow_html=True)
    st.markdown('<div class="workspace"><strong>Không gian sinh viên</strong><br>Machine Learning<br>Diabetes Prediction</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**Cuộc hội thoại**")
    st.caption(f"{len(st.session_state.history)} lượt đang lưu trong phiên này")
    st.button("＋ Hội thoại mới", type="primary", use_container_width=True, disabled=not st.session_state.history, on_click=clear_history)
    if st.session_state.history:
        st.download_button("Tải hội thoại", data=json.dumps(st.session_state.history,ensure_ascii=False,indent=2),
                           file_name="helpdesk-conversation.json", mime="application/json", use_container_width=True)
    st.divider()
    with st.expander("Cấu hình model"):
        model = st.text_input("Model Ollama", value=settings.ollama_model, help="Dùng tên model được cung cấp bởi Ollama.")
        st.caption("Thay đổi model áp dụng cho câu hỏi tiếp theo.")
    st.caption("Không nhập mật khẩu hay khóa API. Nội dung gửi tới model đã cấu hình.")
    st.caption("Công cụ giáo dục, không dùng để chẩn đoán y khoa.")

with st.sidebar:
    section = st.radio("Chức năng", ["Hỏi đáp", "Feedback code", "Chấm code", "Flashcard"], key="section")
if section != "Hỏi đáp":
    from lab_ui import render_lab
    render_lab(section, model)
    st.stop()

st.markdown('<div class="topbar"><div><strong>AI Chat Assistant</strong><small>Mini Helpdesk dành cho sinh viên</small></div><span class="badge">Hỗ trợ học tập</span></div>', unsafe_allow_html=True)
if not st.session_state.history and "pending_question" not in st.session_state:
    st.markdown('<div class="welcome"><div class="symbol">AI</div><h1>Hôm nay bạn cần hỗ trợ gì?</h1><p>Giải thích kiến thức, tìm nguyên nhân lỗi code hoặc đọc kết quả mô hình. Mình sẽ cùng bạn xử lý từng bước.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">BẮT ĐẦU VỚI MỘT CÂU HỎI</div>', unsafe_allow_html=True)
    for column,(label,prompt) in zip(st.columns(3,gap="medium"),SUGGESTIONS):
        with column:
            with st.container(border=True):
                st.button(label, use_container_width=True, on_click=choose_question, args=(prompt,))
                st.caption(prompt)
    st.caption("Thông tin học vụ chính thức cần xác nhận với giảng viên hoặc phòng đào tạo.")



def render(reply):
    st.caption(f"{CATEGORIES[reply['category']]} · {STATUSES[reply['status']]}")
    if reply["source"] == "fallback":
        st.warning(reply["answer"])
    else:
        st.markdown(reply["answer"])
    if reply["steps"]:
        st.markdown("**Các bước tiếp theo**")
        st.markdown("\n".join(f"{index}. {step}" for index,step in enumerate(reply["steps"],1)))
    if reply["follow_up"]:
        st.info(reply["follow_up"], icon="💬")
    if reply["source"] == "fixed":
        st.caption("Câu trả lời cố định do ứng dụng cấu hình.")
    with st.expander("Xem dữ liệu JSON"):
        st.caption("Dữ liệu đã kiểm tra cấu trúc. Nội dung kiến thức vẫn cần đối chiếu khi sử dụng.")
        st.json(reply)

for item in st.session_state.history:
    with st.chat_message("user", avatar="👤"):
        st.markdown(item["question"])
    with st.chat_message("assistant", avatar="✨"):
        render(item["reply"])

question = st.chat_input("Nhập câu hỏi hoặc dán lỗi code của bạn…", max_chars=4000)
question = st.session_state.pop("pending_question", None) or question
if question:
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Đang đọc câu hỏi và chuẩn bị hướng dẫn…"):
            reply=service().ask(question, model, st.session_state.history).model_dump()
        render(reply)
    st.session_state.history.append({"question":question,"reply":reply})
    st.session_state.history=st.session_state.history[-20:]
