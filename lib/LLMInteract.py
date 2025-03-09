import requests
import json
from pdf2text import pdf2text

class LLMInteract:
    def __init__(self, filepath):
        self.filepath = filepath
        self.prompt = None
        self.text = None

    def text_get(self):
        pdf_text = pdf2text(self.filepath)
        self.text = pdf_text.clean()
        print('文本提取成功')
        
    def prompt_struct(self):
        self.prompt = f"""
        
            你是一个学术助手，请从以下文献中提取研究目标与方法论部分，注意，
            方法论部分需要重点展开，需要包含论文的研究思路，使用的模型原理等，同时，需要总结研究的不足之处
            并以清晰、结构化的方式总结：
            
            {self.text[:10000]}  # 避免超长输入，截取前10000字符

            请以 Markdown 格式返回，比如：
            
            ## 研究目标
            - **研究目标**: xxx

            ## 方法论
            - **研究方法**: xxx
            - **实验设置**: xxx
            - **数据来源**: xxx
            - **关键参数**: xxx
            
            ## 研究不足
            """

        print('Prompt构造成功')
    def query_ollama(self):
        url = 'http://localhost:11434/api/generate'
        payload = {
            "model": 'deepseek-r1:8b',
            "prompt": self.prompt
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print('提交给本地模型，开始分析')
        # 按行解析 JSON
        responses = []
        for line in response.text.strip().split("\n"):  # 逐行解析
            try:
                data = json.loads(line)  # 解析 JSON
                if "response" in data:
                    responses.append(data["response"])
            except json.JSONDecodeError:
                print(f"解析失败的行: {line}")  # 方便调试
                continue
        return "".join(responses)  # 拼接所有返回的内容

if __name__ == "__main__":
    file_path = r"C:\Users\Kangxin\Zotero\storage\ZQZEW8NY\Qin 等 - 2021 - Optimizing matching time intervals for ride-hailin.pdf"
    llm = LLMInteract(file_path)
    llm.text_get()
    llm.prompt_struct()
    response = llm.query_ollama()
    print(response)

    
