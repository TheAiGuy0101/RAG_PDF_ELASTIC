# PDF Processing Project

## Overview

The PDF Processing Project is a multi-agent platform built using CrewAI to process large PDF files, including those with text as images. The platform uses OCR capabilities to extract text from images and indexes the extracted text in Elasticsearch. Users can then query the indexed text and generate responses using OpenAI's API. The project also includes a Streamlit application for an interactive user interface.

## Features

- **Multi-Agent System**: Utilizes CrewAI to manage agents and tasks.
- **OCR Integration**: Uses Tesseract OCR to extract text from images.
- **Text Embeddings**: Converts text into vector embeddings using Transformer models.
- **Elasticsearch Indexing**: Stores and indexes extracted text for efficient querying.
- **Interactive UI**: Provides a Streamlit application for easy interaction with the platform.

### Installation

1. **Clone the repository**


[git clone https://github.com/yourusername/pdf_processing_project.git](https://github.com/TheAiGuy0101/RAG_PDF_ELASTIC.git)
cd RAG_PDF_ELASTIC

2. **Setup & Configuration**
    Create Python Environment
        python -m venv .venv
    Activate the python environment
        .venv\Scripts\activate.bat
    Install Elastic locally
        Download elastic[text](https://www.elastic.co/downloads/elasticsearch)
        Go in the config folder and disable security by changing following setting:
            xpack.security.enabled: false
            xpack.security.enrollment.enabled: false


3. **Running the Application**
    Run following command: streamlit run src/pdf_processing_project/main.py
    you can access the Streamlit application at http://localhost:8501.

4. **Usage**

    Uploading PDFs
        Open the Streamlit application in your browser.
        Use the file uploader to select one or more PDF files.
        Click the "Process PDFs" button to start the processing.
    Asking Questions
        Enter your question in the text input field under the "Ask Questions" section.
        Click the "Get Answer" button to retrieve the answer based on the indexed text.
    Getting Summaries
        Click the "Get Summary" button under the "Get Summary" section to generate a summary of the indexed text.

5. **Contributing**
    Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

6. **License**
    This project is licensed under the MIT License. See the LICENSE file for more details.
