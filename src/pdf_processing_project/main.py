
import os
import yaml
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader
from elasticsearch import Elasticsearch, ConnectionError
import streamlit as st
from llm_factory import LLMFactory
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from transformers import AutoTokenizer, AutoModel
import torch
import time

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Set environment variables
os.environ["ELASTICSEARCH_URL"] = config["elasticsearch_url"]
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your Tesseract installation

# Initialize Elasticsearch with retry logic and no authentication
def init_elasticsearch(es_url, retries=5, delay=5):
    es = Elasticsearch(es_url)
    for _ in range(retries):
        try:
            if es.ping():
                print("Connected to Elasticsearch!")
                return es
            else:
                print("Failed to connect to Elasticsearch, retrying...")
                time.sleep(delay)
        except ConnectionError as e:
            print(f"Connection error: {e}, retrying...")
            time.sleep(delay)
    raise ConnectionError("Could not connect to Elasticsearch after several retries.")

es = init_elasticsearch(os.environ["ELASTICSEARCH_URL"])

# Initialize LLM
llm_model = LLMFactory.get_llm(config["llm_model"], config[f"{config['llm_model']}_api_key"])

# Initialize Transformer Model for Embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.detach().numpy()

def process_pdf(file_path):
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)

    def extract_page_text(page_num):
        page = reader.pages[page_num]
        try:
            text = page.extract_text()
            if not text:
                raise ValueError("No text found")
        except:
            # If text extraction fails, perform OCR
            images = convert_from_path(file_path, first_page=page_num + 1, last_page=page_num + 1)
            text = " ".join(extract_text_from_image(image) for image in images)

        embeddings = get_embeddings(text)
        es.index(index="pdf_text", body={"page": page_num, "text": text, "embeddings": embeddings.tolist()})

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(extract_page_text, range(num_pages))

def query_elasticsearch(query):
    query_embeddings = get_embeddings(query)
    response = es.search(
        index="pdf_text",
        body={
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                        "params": {
                            "query_vector": query_embeddings.tolist()[0]
                        }
                    }
                }
            }
        }
    )
    return response['hits']['hits']

def generate_answer(context, question):
    prompt = f"Based on the following context, answer the question: {context}\n\nQuestion: {question}"
    response = llm_model.query(prompt)
    return response

if __name__ == "__main__":
    st.title("PDF Processing with CrewAI")

    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.write(f"File {uploaded_file.name} uploaded successfully!")

        if st.button("Process PDFs"):
            for uploaded_file in uploaded_files:
                process_pdf(f"temp_{uploaded_file.name}")
            st.write("PDF processing started.")

    st.header("Ask Questions")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        results = query_elasticsearch(question)
        context = " ".join([res['_source']['text'] for res in results])
        answer = generate_answer(context, question)
        st.write(answer)

    st.header("Get Summary")
    if st.button("Get Summary"):
        results = query_elasticsearch("summary")
        context = " ".join([res['_source']['text'] for res in results])
        summary = generate_answer(context, "Provide a summary of the above content.")
        st.write(summary)
