# Mini Lab buổi 13–15

Mở Mini Helpdesk, chọn chức năng ở sidebar. Model, API client và cấu hình key được giữ nguyên.

## Buổi 13: Feedback code

Nhập đề bài, code và giải thích nếu có. Kết quả: bug, gợi ý, câu hỏi kiểm tra và kết luận.
Prompt có ROLE, TASK, CONTEXT, CONSTRAINTS, FORMAT, ràng buộc không đưa full đáp án.
Code chỉ được đọc làm dữ liệu, không thực thi. Ràng buộc prompt không bảo đảm tuyệt đối
model sẽ không đưa lời giải; cần đọc kết quả thực tế trước khi nộp.

## Buổi 14: Chấm code

Rubric đã thống nhất: đúng chức năng 4, trường hợp biên 2, chất lượng code 2, giải thích 2.
Đầu ra có bốn điểm thành phần, bốn nhận xét, tổng điểm, gợi ý và kết luận.
Validation kiểm tra tổng điểm, giới hạn điểm và buộc điểm giải thích bằng 0 nếu không có giải thích.
Điểm là nhận xét tĩnh do AI đề xuất, chưa thay thế đánh giá của giảng viên.
Few-shot có ca đúng và ca sai. Prompt đầu, prompt sửa, input/output và nhận xét nằm trong `prompt_development.json`.

## Buổi 15: Flashcard

Nhập chủ đề, chọn easy/medium/hard. Tạo đúng 3 thẻ khác nhau, mỗi thẻ có question,
answer và difficulty. Mở từng thẻ để xem đáp án, tải JSON để nộp.
Schema Pydantic ở `app/services/lab_service.py`; năm ca sai nằm trong `tests/test_labs.py`:
JSON không parse được, thiếu answer, question sai kiểu, difficulty sai enum, chỉ có hai thẻ.
Ngoài ra còn kiểm tra tổng điểm, input rỗng, sửa JSON và lỗi API.

## Chạy lại kiểm tra

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Khi nộp, bổ sung tên hai thành viên, input đã dùng, JSON tải từ giao diện và kết luận ngắn.
Kết luận mẫu về cách kiểm tra: schema đúng chưa chứng minh nội dung đúng; đối chiếu bug,
điểm rubric và flashcard với kiến thức của môn học. Không ghi rằng đã chạy code sinh viên.

## Cập nhật từ bản cũ

Dừng Streamlit bằng Ctrl+C. Chép `app`, `tests`, `.streamlit` và tài liệu từ bản mới vào
thư mục cũ. Giữ nguyên `.env` và `.venv`. Không thêm thư viện mới trong lần cập nhật này.
Chạy lại `run_helpdesk.bat`. Không sửa phần gọi API buổi 12.
