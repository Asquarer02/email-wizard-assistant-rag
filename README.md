# Email Wizard's Assistant

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


## Evaluation

This section details the initial performance metrics for the Email Wizard's Assistant, based on a dataset of 60 emails and a suite of 6 diverse test queries.

### 1. Search Speed (Inference Time)

*   **Individual RAG Inference Times:**
    *   Query 1 ("Daren Farmer contact?"): `2.2525` seconds
    *   Query 2 ("i2 Technologies/Tax?"): `3.7890` seconds
    *   Query 3 ("MDEA Agreement scheduling?"): `2.0473` seconds
    *   Query 4 ("Vitro/Termination agreement?"): `3.2780` seconds
    *   Query 5 ("Status of my project?"): `3.2771` seconds
    *   Query 6 ("Hi, how are you?"): `2.4133` seconds
*   **Average Full RAG Inference Time:** The system processed these 6 test queries with an average end-to-end inference time of approximately **`2.8429` seconds** (calculated from the individual times above). This includes document retrieval and response generation by the `gpt-4o-mini` model.
*   **Retrieval Times (FAISS `similarity_search_with_score` for Top-3):**
    *   Query 1: `0.9723` sec
    *   Query 2: `0.9195` sec
    *   Query 3: `1.3319` sec
    *   Query 4: `0.8194` sec
    *   Query 5: `0.6122` sec
    *   Query 6: `0.5108` sec
*   **System:** (e.g., Tested on [Your System Specs: CPU, RAM, OpenAI Model Used])

### 2. Accuracy of Similarity (Retrieval Quality)

Retrieval quality was assessed using FAISS L2 distance scores (where **lower scores indicate higher similarity/relevance**) for the Top-1 retrieved document for each test query.

*   **Top-1 Document L2 Distance Scores (per query):**
    *   Query 1 ("What is the phone number for Daren Farmer at ENA?"): **`0.6766`**
        *   *Qualitative Note:* The retrieved document was highly relevant, containing the exact phone number.
    *   Query 2 ("What is the discussion about i2 Technologies and Tax?"): **`0.9416`**
        *   *Qualitative Note:* The retrieved document was highly relevant, detailing the discussion regarding Erica's advice on EnronCredit.com contracts.
    *   Query 3 ("Who should be contacted about the MDEA Agreement scheduling?"): **`0.8944`**
        *   *Qualitative Note:* The retrieved document was relevant, identifying Bob Priest in relation to the MDEA agreement.
    *   Query 4 ("Tell me about the Vitro/Termination agreement."): **`0.8657`**
        *   *Qualitative Note:* The retrieved document mentioned the termination agreement and related personnel, providing useful context even if not the full agreement text.
    *   Query 5 ("What's the status of my project?"): **`1.4451`**
        *   *Qualitative Note:* The higher L2 score reflects the generic nature of the query. The retrieved documents were the closest syntactic matches but did not contain specific project status information (as expected from this dataset).
    *   Query 6 ("Hi, how are you?"): **`1.3443`**
        *   *Qualitative Note:* Similar to the above, the L2 score is higher as there are no direct "how are you" emails. The retrieved documents were the closest available but not semantically relevant to the greeting.

*   **Interpretation of L2 Scores:**
    *   L2 distance scores range from 0 (identical embedding) upwards. Scores below ~1.0 for specific, answerable queries (like Q1-Q4) indicate good retrieval from this small dataset. Higher scores for generic or unanswerable queries (Q5, Q6) are expected and demonstrate the system's attempt to find the nearest semantic match, even if not topically relevant.
    *   The quality of retrieval is further confirmed by the LLM's ability to utilize these top documents effectively (see Coherence section).

### 3. Coherence of Responses (LLM Generation Quality)

This was assessed qualitatively by reviewing the LLM-generated answers for the 6 test queries, considering their faithfulness to the retrieved context, relevance to the query, clarity, and fluency.

*   **Overall Assessment:** Responses were generally coherent and directly addressed the queries when relevant information was present in the retrieved documents. The system appropriately indicated when information was not available for generic or unanswerable queries.
*   **Examples of Coherent Responses:**
    *   **Query 1:** "What is the phone number for Daren Farmer at ENA?"
        *   LLM Answer: "The phone number for Daren Farmer at ENA is 713-853-6905."
        *   *Note:* This answer is directly supported by the top retrieved document (L2 Score: `0.6766`).
    *   **Query 2:** "What is the discussion about i2 Technologies and Tax?"
        *   LLM Answer: "The discussion about i2 Technologies and Tax revolves around the approval of contracts related to Enron Credit.com that are being signed in the US. Tana Jones emphasizes that Erica's advice should apply not only to the specific Non-Disclosure Agreement (NDA) but also to all NDAs and the overall business originating from the Houston-based EnronCredit.com team..."
        *   *Note:* This detailed answer accurately reflects the content of the top retrieved document (L2 Score: `0.9416`).
    *   **Query 5:** "What's the status of my project?"
        *   LLM Answer: "I don't know."
        *   *Note:* This is an appropriate and honest response, given the lack of specific project status emails in the dataset and the higher L2 score (`1.4451`) of the top retrieved document for this generic query.
*   **General Observation:** The LLM effectively utilized the context from the Top-1 (and likely Top-3) retrieved documents to formulate its answers or to determine when an answer could not be found.

---
