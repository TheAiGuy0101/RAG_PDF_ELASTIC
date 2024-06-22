from transformers import AutoTokenizer, AutoModel

def test_imports():
    try:
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        print("Import and model loading successful!")
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_imports()
