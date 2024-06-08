import pandas as pd
from llm import LLmsService
from tqdm import tqdm


class BenchMark:

    def __init__(self, input_file, output_file) -> None:
        self.data = pd.read_excel(input_file)
        self.output_file = output_file


    def eval_all(self, input_file, output_file):
        df = pd.read_excel(input_file)
        query_list = []
        answer_list = []
        for index, row in df.iterrows():
            if index>5:
                break

            query = row[0].strip()
            if len(query)>0:
                answer = fun_call(query)
                query_list.append(query)
                answer_list.append(answer)
            else:
                query_list.append("空")
                answer_list.append("空")

        df_new = pd.DataFrame(
            {
                'query': query_list,
                'answer': answer_list,
            }
        )
        df_new.to_csv(output_file, index=False, sep=',')

   
    def eval_model(self, model):
        model_params={
            "top_p": 0.7,
            "temperature": 0.9,
            # 'max_tokens': 8000,
            'stream': False
        }
        llm = LLmsService(model, model_params)
        
        for idx, row in tqdm(self.data.iterrows(), total=self.data.shape[0], desc="Row Processing"):
            query = row[0].strip()
            if len(query) > 0:
                answer = llm([{"role": "user", "content": query}])
                self.data.at[idx, "answer"] = answer
            else:
                self.data.at[idx, "answer"] = "空"
        
        self.data.to_excel(output_file, sheet_name="glm-4", index=False)


if __name__ == '__main__':
    model = "qwen2"
    input_file = "F-Eval2.xlsx"
    output_file = f"Eval2_result_{model}.xlsx"

    benchmark = BenchMark(input_file, output_file)
    benchmark.eval_model(model)

