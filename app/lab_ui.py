import json
import streamlit as st
from services.lab_service import LabService

@st.cache_resource
def lab_service():
    return LabService()

def render_lab(section, model):
    kinds = {'Feedback code': 'feedback', 'Chấm code': 'grade', 'Flashcard': 'flashcards'}
    kind = kinds[section]
    st.header(section)
    st.caption('Code được đọc để nhận xét, không được thực thi. Điểm do AI đề xuất, cần người học đối chiếu.')
    if kind == 'grade':
        st.table({'Tiêu chí': ['Đúng chức năng', 'Trường hợp biên', 'Chất lượng code', 'Giải thích'], 'Điểm tối đa': [4, 2, 2, 2]})
    with st.form('lab_' + kind):
        if kind == 'flashcards':
            topic = st.text_input('Chủ đề *', placeholder='Ví dụ: Train / Validation / Test')
            difficulty = st.selectbox('Độ khó', ['easy', 'medium', 'hard'])
            payload = {'topic': topic, 'difficulty': difficulty}
        else:
            assignment = st.text_area('Đề bài *', placeholder='Mô tả input, output và yêu cầu của bài tập.')
            code = st.text_area('Code Python *', height=200)
            explanation = st.text_area('Giải thích của sinh viên', help='Chấm code: không có giải thích thì tiêu chí này nhận 0 điểm.')
            payload = {'assignment': assignment, 'code': code, 'explanation': explanation}
        submitted = st.form_submit_button('Tạo 3 flashcard' if kind == 'flashcards' else section, type='primary')
    key = 'result_' + kind
    if submitted:
        with st.spinner('Đang chuẩn bị kết quả…'):
            st.session_state[key] = lab_service().run(kind, payload, model)
    result = st.session_state.get(key)
    if not result:
        return
    if not result['ok']:
        st.warning(result['message'])
        return
    data = result['data']
    if kind == 'flashcards':
        for index, card in enumerate(data['flashcards'], 1):
            with st.expander(f"Thẻ {index}: {card['question']}"):
                st.write(card['answer'])
                st.caption('Độ khó: ' + card['difficulty'])
    else:
        if kind == 'grade':
            st.metric('Tổng điểm đề xuất', f"{data['total']}/10")
            st.table({'Tiêu chí': ['Đúng chức năng', 'Trường hợp biên', 'Chất lượng code', 'Giải thích'],
                      'Điểm': [data[k] for k in ['functionality', 'edge_cases', 'code_quality', 'explanation']], 'Nhận xét': data['reasons']})
        else:
            st.markdown('**Bug / vấn đề phát hiện**')
            for bug in data['bugs']:
                st.write('• ' + bug)
            if not data['bugs']:
                st.info('Chưa phát hiện bug qua nhận xét tĩnh; chưa chứng minh code đúng mọi input.')
            st.info(data['check_question'])
        st.markdown('**Gợi ý tự sửa**')
        for hint in data['hints']:
            st.write('• ' + hint)
        st.write('Kết luận: ' + data['conclusion'])
    with st.expander('Xem JSON đã validate'):
        st.json(data)
    st.download_button('Tải kết quả JSON', json.dumps(data, ensure_ascii=False, indent=2),
                       file_name=kind + '.json', mime='application/json')
