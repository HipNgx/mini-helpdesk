# Kết quả kiểm tra ngày 04/10/2026

- 9 unit test pass; bao gồm 5 dạng JSON sai và kiểm tra quy tắc nghiệp vụ.
- Gọi Ollama Cloud thực tế với `gemma4:31b`, dùng key đọc từ `.env` dự án cũ trong tiến trình kiểm tra. Không sao chép key vào deliverable.
- 8 input mới đều có source `llm`, JSON đã validate. Kết quả nằm trong `evaluation_results.json`.
- Một ca accuracy/recall ban đầu kết luận quá chắc. Đã bổ sung constraint và chạy lại ca đó. `prompt_iteration.json` lưu trước/sau; không khẳng định schema đảm bảo kiến thức đúng.
- Kiểm tra Streamlit bằng AppTest: tải giao diện, gửi câu hỏi với service giả, hiển thị JSON, xóa hội thoại đều pass. Chưa kiểm tra trực quan bằng trình duyệt.
- AppTest có cảnh báo dọn thư mục tạm của môi trường sau khi các assertion đã pass. Tiến trình trả exit code 0.
- Chạy bằng Python/dependencies trong `.venv` dự án cũ, chưa cài mới môi trường từ requirements.
- Chưa kiểm tra Ollama local, toàn bộ chức năng Tutor/Quiz cũ hoặc chất lượng trên một bộ dữ liệu lớn.

Kiểm tra 8 input thực hiện với prompt phiên bản đầu. Sau chỉnh prompt, chỉ chạy lại ca accuracy/recall. Các kết quả còn lại được giữ làm bằng chứng lần chạy trước.

UI bản mới: phong cách trắng/xanh cobalt, câu hỏi gợi ý, nhãn trạng thái tiếng Việt, tải hội thoại và cấu hình model thu gọn. AppTest pass cho trang chào, bấm gợi ý, chat, fallback, JSON và xóa hội thoại. Chưa xác minh hình thức bằng trình duyệt.

Giao diện AI Chat Assistant: nền #F0F2FD, sidebar trắng, điểm nhấn #2735FE, trang chào tập trung chat, gợi ý dạng thẻ và cấu hình thu gọn. Smoke test UI pass sau cập nhật; chưa kiểm tra trực quan bằng trình duyệt.

Bổ sung buổi 13–15: 16 unit test pass, ba form lab và luồng chat cũ pass qua AppTest. Gọi gemma4:31b thực tế: feedback, chấm code trước/sau chỉnh prompt và flashcards đều validate thành công. Một ca bài average đã được đọc để đối chiếu bug, gợi ý và tổng điểm. Không thực thi code sinh viên, không thay model hoặc API client. Chưa đánh giá tính ổn định trên nhiều bài hoặc kiểm tra trực quan trình duyệt.
