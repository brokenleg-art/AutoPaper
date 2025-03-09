import sqlite3
from pdfminer.high_level import extract_text
from LLMInteract import LLMInteract

class FileDB:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn = None
        self.cursor = None

    def paperdb_construct(self):
        self.conn = sqlite3.connect("papers.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                file_path TEXT UNIQUE,  -- 确保同一篇文献不被重复存储
                extracted_text TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        self.conn.close()
    
    def add_paper(self, title, file_path, extract_text, summary):
        self.conn = sqlite3.connect("papers.db")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("INSERT OR IGNORE INTO papers (title, file_path, extracted_text, summary) VALUES (?,?,?,?)",
                             (title, file_path, extract_text, summary))
        self.conn.commit()
        self.conn.close()

    def delete_paper(self, file_path):
        self.conn = sqlite3.connect("papers.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM papers WHERE file_path = ?", (file_path,))
        self.conn.commit()
        self.conn.close()
    
    
if __name__ == "__main__":
    # 此处替换为你自己的文献存放的路径
    file_db = FileDB()