# RAG Dynamic Document Parsing and Chunking

## Project Overview

A Python-based document preprocessing project developed as part of a Generative AI assignment.

The project extracts and organizes content from multiple document formats using document-specific parsing and chunking strategies.

It prepares structured JSON chunks for future Retrieval-Augmented Generation (RAG) applications.

## Technologies Used

- Python
- PyMuPDF – PDF text extraction
- python-docx – Word document processing
- Pytesseract – OCR processing
- Pillow – Image handling
- JSON – Structured output
- Regular Expressions – Text processing
- VS Code – Development environment

## Key Features

- Extract text from PDF, DOCX, Markdown, and TXT files
- Perform section-aware text chunking
- Preserve Markdown code blocks
- Extract text from scanned invoices using OCR
- Group troubleshooting instructions and warnings
- Apply a configurable 100-word text chunking target
- Generate structured JSON output
- Flag selected chunks for manual review

## Document Processing Strategies

| Document Type | Processing Method |
|---|---|
| Employee Policy PDF | Section-based chunking |
| Product Documentation | Markdown-aware chunking |
| Scanned Invoice | OCR and field extraction |
| Troubleshooting Guide | Issue-based grouping |

## Project Structure

```text
rag_assignment/
├── input/
│   ├── employee_policy.pdf
│   ├── product_documentation.md
│   ├── scanned_invoice.png
│   └── troubleshooting_guide.txt
├── output/
│   └── chunks.json
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-dynamic-document-chunking.git
```

### 2. Navigate to the project

```bash
cd rag-dynamic-document-chunking
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment (Windows)

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Tesseract OCR

Install Tesseract OCR separately and update the executable path in `main.py` to match your local installation.

### 7. Run the application

```bash
python main.py
```

## Execution Results

The following results were obtained during testing:

```text
OK employee: 3 chunks
OK product: 3 chunks
OK invoice: 1 chunks
OK troubleshooting: 2 chunks

Saved 9 chunks to output/chunks.json
```

## JSON Output Format

Each output chunk includes:

- `chunk_id`
- `source`
- `document_type`
- `section`
- `text`
- `word_count`
- `needs_review`

Example:

```json
{
  "chunk_id": "employee_002",
  "source": "employee_policy.pdf",
  "document_type": "employee",
  "section": "Attendance Policy",
  "text": "Employees must record attendance each working day.",
  "word_count": 7,
  "needs_review": false
}
```

## Learning Outcomes

Through this project, I gained hands-on experience in:

- Python-based document parsing
- Document-specific chunking strategies
- OCR integration
- JSON data generation
- Text preprocessing for RAG pipelines
- Error handling and debugging
- Working with multiple file formats

## Limitations

This project focuses on document preprocessing rather than implementing a complete RAG chatbot.

It does not currently include embeddings, vector database integration, semantic retrieval, or LLM-generated responses.

Scanned invoice fields require manual verification.

## Future Enhancements

- Integrate sentence embeddings
- Add FAISS or ChromaDB vector storage
- Implement semantic document retrieval
- Integrate an LLM for question answering
- Develop a Streamlit user interface
- Improve OCR accuracy and document parsing

## Author

**Gowtham M**

Python | Generative AI | RAG | Backend Development

## Project Status

**Completed – Document Parsing and Chunking Assignment**