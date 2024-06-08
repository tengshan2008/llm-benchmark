from typing import Any
import pandas as pd
import json


class Convert:
    NUM_SAMPLES = 100
    
    def __init__(self, input_file, sheet_name) -> None:
        self.data = pd.read_excel(input_file, sheet_name=sheet_name)
    
    def subjective(self) -> Any:
        subjective_df = self.data[self.data['题目类型'] == '主观题']

        result = pd.concat([
            subjective_df[subjective_df['一级能力'] == '中文通用基础能力\n(300道）'].sample(n=self.NUM_SAMPLES, random_state=1),
            subjective_df[subjective_df['一级能力'] == '金融能力\n(400道）'].sample(n=self.NUM_SAMPLES, random_state=2),
            subjective_df[subjective_df['一级能力'] == '业务专精能力\n(300道）'].sample(n=self.NUM_SAMPLES, random_state=3),
        ])

        result = result[["序号", "一级能力", "二级能力", "题目", "标准答案", "解释（可为空）"]]
        prompt = result[["题目"]]

        result.to_excel("samples.xlsx", sheet_name="样本", index=False)
        prompt.to_excel("prompt.xlsx", sheet_name="prompt", index=False)

    def objective(self) -> Any:
        objective_df = self.data[self.data['题目类型'] == '客观题']
        
        result = []
        for _, row in objective_df.iterrows():
            if pd.isna(row[0]):
                continue
            num_id = int(row[0])
            question = row[5]
            item_a = row[6]
            item_b = row[7]
            item_c = row[8]
            item_d = row[9]
            answer = row[10]
            result.append({
                'id': f"{num_id}",
                "question": f"{question}",
                "A": f"{item_a}",
                "B": f"{item_b}",
                "C": f"{item_c}",
                "D": f"{item_d}",
                "answer": f"{answer}"
            })
            
        with open("objective.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)


    def subjective_app(self, input_file) -> Any:
        subjective_df = pd.read_excel(input_file, sheet_name="Sheet1")
        
        result = []
        
        for _, row in subjective_df.iterrows():
            
            
            result.append({
                'question': row["题目"],
                'answer1': row["glm-4"],
                'answer2': row['qwen2'],
                'answer3': row['doubao']
            })

        with open("questions.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
        

if __name__ == '__main__':
    convert = Convert("F-Eval 2.0 评测集-0606版.xlsx", "F-Eval 2.0基准结构（测试集)")
    # convert.subjective()
    # convert.objective()
    
    convert.subjective_app("主观题.xlsx")
    
