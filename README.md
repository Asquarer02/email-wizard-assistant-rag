# AI/ML Coding Challenge: Email Wizard's Assistant

This project implements an Email Wizard Assistant using a Retrieval-Augmented Generation (RAG) model to answer queries based on a provided email dataset.

## Task Overview (Covered in this Phase)

1.  **GitHub Repository Setup:** This repository.
2.  **RAG Model Integration:**
    *   Embedding: OpenAI `text-embedding-3-small`
    *   Generation: OpenAI `gpt-4o-mini`
    *   Orchestration: LangChain
3.  **Dataset Preparation:** Uses `proc_email.csv` (first 60 emails).
4.  **Embedding:** Emails are embedded and stored in a FAISS vector store.
5.  **Similarity Search:** FAISS is used for retrieving relevant emails.

## Project Structure
```
email-wizard-assistant-rag/
├── .git/                 
├── .gitignore            
├── api/                  # For Flask/FastAPI application (to be developed)
│   └── (empty for now)
├── data/                 # Contains the dataset
│   └── proc_email.csv    
├── notebooks/            # Jupyter notebooks for development and experimentation
│   └── email_assistant_rag.ipynb           
├── .env          
└── README.md             
```