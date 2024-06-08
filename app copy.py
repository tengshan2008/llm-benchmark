import streamlit as st
import json
import sqlite3

# 连接到 SQLite 数据库
# 如果文件不存在，会自动在当前目录创建一个数据库文件
conn = sqlite3.connect('answers.db')
c = conn.cursor()

# 创建一个表来存储数据
c.execute('''
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY,
    question TEXT,
    answer1 TEXT,
    answer2 TEXT,
    answer3 TEXT,
    score1 INTEGER,
    score2 INTEGER,
    score3 INTEGER
)
''')

# 加载 JSON 数据
def load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 显示问题和答案，允许用户打分
def show_question_and_score(data):
    for idx, item in enumerate(data):
        col1, col2, col3 = st.columns(3)
        st.write(f"问题：{item['question']}")
        
        with col1:
            st.write(f"答案1：{item['answer1']}")
            st.number_input(f'分数_{idx}_1', key=f"score_{idx}_1", min_value=0, max_value=5, value=0)
        with col2:
            st.write(f"答案2：{item['answer2']}")
            st.number_input(f'分数_{idx}_2', key=f"score_{idx}_2", min_value=0, max_value=5, value=0)
        with col3:
            st.write(f"答案3：{item['answer3']}")
            st.number_input(f'分数_{idx}_3', key=f"score_{idx}_3", min_value=0, max_value=5, value=0)
        if st.button('提交', key=f"button_{idx}"):
            score1 = st.session_state.get(f"score_1", 0)
            score2 = st.session_state.get(f"score_2", 0)
            score3 = st.session_state.get(f"score_3", 0)
            # 将数据保存到数据库
            c.execute('''
                INSERT INTO answers (question, answer1, answer2, answer3, score1, score2, score3)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item['question'], item['answer1'], item['answer2'], item['answer3'], score1, score2, score3))
            conn.commit()
            # 重置 session state
            st.session_state[f"score_1"] = 0
            st.session_state[f"score_2"] = 0
            st.session_state[f"score_3"] = 0

# 运行 Streamlit 应用
def main():
    st.title('问题评分应用')
    
    # 加载 JSON 数据
    data = load_json_data('questions.json')
    
    # # 显示问题和答案，允许用户打分
    # show_question_and_score(data)

    # 提交所有数据到数据库
    if st.button('提交并获取新问题'):
        submit_and_move_to_next(data, st.session_state.current_index)
        conn.commit()

if __name__ == '__main__':
    main()