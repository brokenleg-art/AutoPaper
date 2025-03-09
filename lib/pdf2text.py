from pdfminer.high_level import extract_text
import re

class pdf2text:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = None
    def clean(self):
        # 文本清理，截取有效的论文部分
        self.text = extract_text(self.pdf_path)
        self.text = re.sub(r'\s+', ' ', self.text)  # 移除多余空格
        self.text = re.sub(r'-\n', '', self.text)  # 处理换行符导致的单词拆分
        self.text = re.sub(r'\n+', '\n', self.text)  # 移除多余换行
        self.text.strip()

        match = re.search(r'Introduction', self.text, re.IGNORECASE)
        if match:
            self.text = self.text[match.start():]  # 截取从 "Introduction" 开始的部分
        return self.text

if __name__ == '__main__':
    file_path = r"C:\Users\Kangxin\Zotero\storage\ZQZEW8NY\Qin 等 - 2021 - Optimizing matching time intervals for ride-hailin.pdf"
    pdf_text = pdf2text(file_path)
    pdf_text.clean()  # 文本清理
    print(pdf_text.text[:1000])  # 预览前1000个字符
