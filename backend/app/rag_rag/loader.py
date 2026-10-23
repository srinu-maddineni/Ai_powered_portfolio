from pathlib import Path


def load_portfolio():
    file_path = Path(r"C:\Users\srinu\OneDrive\Desktop\rag\backend\data\srinu_data.txt")

    return file_path.read_text(encoding="utf-8")