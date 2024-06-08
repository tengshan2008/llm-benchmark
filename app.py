import streamlit as st
import json

# 假设的数据库连接和表创建代码
# conn = sqlite3.connect('answers.db')
# c = conn.cursor()
# ... 创建表的代码 ...

# 加载 JSON 数据
def load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 初始化 session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# 显示问题和评分控件
def show_question_and_ratings(data, index):
    flash = st.button("刷新")
    if index < len(data):
        question = data[index]
        st.write(f"问题：{question['question']}")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            score1 = st.number_input("答案1评分", min_value=0, max_value=5, key=f"score1_{index}")
            st.write(f"答案1: {question['answer1']}")
        with col2:
            score2 = st.number_input("答案2评分", min_value=0, max_value=5, key=f"score2_{index}")
            st.write(f"答案2: {question['answer2']}")
        with col3:
            score3 = st.number_input("答案3评分", min_value=0, max_value=5, key=f"score3_{index}")
            st.write(f"答案3: {question['answer3']}")

        return question, score1, score2, score3
    else:
        st.write("没有更多问题了。")
        return None

# 提交按钮和数据库存储逻辑
def submit_and_move_to_next(data, index):
    question_data = show_question_and_ratings(data, index)
    if question_data is not None:
        question, score1, score2, score3 = question_data
        # 存储到数据库的逻辑
        # c.execute('''
        #     INSERT INTO answers (question, answer1_score, answer2_score, answer3_score)
        #     VALUES (?, ?, ?, ?)
        # ''', (question['question'], score1, score2, score3))
        # conn.commit()
        print(f"问题: {question['question']}, 答案1评分: {score1}, 答案2评分: {score2}, 答案3评分: {score3}")
        # 更新当前问题索引
        st.session_state.current_index += 1

# 主函数
def main():
    st.title('问题评分应用')
    
    # 加载 JSON 数据
    data = load_json_data('questions.json')
    
    # 提交按钮
    submit_button_clicked = st.button('提交并获取新问题')

    if submit_button_clicked:
        submit_and_move_to_next(data, st.session_state.current_index)

    # 显示当前问题和答案
    show_question_and_ratings(data, st.session_state.current_index)

if __name__ == '__main__':
    main()