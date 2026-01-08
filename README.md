# agenticenterpriseassistant`


# 🧠 Agentic Enterprise Assistant (PoA)

## Overview

This repository presents a **Proof of Architecture (PoA)** for an **Agentic Enterprise Assistant** built using a **Retrieval-Augmented Generation (RAG)** approach.
The system enables employees to query large, unstructured enterprise documents using natural language and receive **accurate, page-traceable, and context-grounded responses**.

The PoA emphasizes **offline execution**, **hallucination prevention**, and **enterprise-safe design**, without integrating with live production systems.

---

## 🎯 Problem Statement

Enterprises manage large volumes of unstructured internal data such as policies, reports, and technical documentation.
Traditional keyword search lacks semantic understanding, while standalone LLMs cannot reliably ground responses in organization-specific knowledge.

This project demonstrates how an **agentic, retrieval-first architecture** can safely and effectively support enterprise knowledge access and decision support.

---

## 🏗️ High-Level Architecture

### Ingestion Pipeline

```
PDF
 → Layout Parsing (Unstructured)
 → Modality Routing (Text / Table / Image)
 → Image Captioning (BLIP)
 → Selective OCR (Tesseract)
 → Table Normalization
 → Structure-Aware Chunking
 → Embeddings (BGE)
 → FAISS Vector Index
```

### Query Pipeline

```
User Query
 → Query Embedding
 → FAISS Similarity Search
 → Retrieved Chunks (with page numbers)
 → LLM (Ollama + Mistral-7B)
 → Grounded Answer / Structured Output
```

---

## 🧱 Technical Architecture

* **LLM**: Ollama (Mistral-7B)

  * Enables fully local, offline, and privacy-preserving answer generation

* **Embedding Model**: BGE (`bge-small-en`)

  * Provides instruction-tuned embeddings for accurate semantic retrieval

* **Vector Database**: FAISS

  * Supports fast cosine-similarity search in a lightweight local setup

* **PDF Parsing & Layout Extraction**: Unstructured

  * Extracts text, tables, and images while preserving page-level metadata

* **Image Understanding**: BLIP (`Salesforce/blip-image-captioning-base`)

  * Generates semantic captions to classify charts, text-heavy, or decorative images

* **Image OCR (Selective)**: Tesseract OCR

  * Applied only to non-decorative images for extracting text and numbers

* **Table Processing**: Unstructured + custom normalization

  * Preserves raw tables and produces retrieval-friendly text representations

* **Chunking Strategy**: Structure-aware, title-based chunking

  * Maintains document hierarchy and semantic coherence

* **Architecture Pattern**: Retrieval-Augmented Generation (RAG)

  * Separates retrieval from generation to ensure grounded responses

* **Design Constraint**: Query-time LLM invocation only

  * Prevents hallucination and ensures page-traceable answers

---

## 📂 Project Structure

```
AGENTICENTERPRISEASSISTANT/
│
├── data/
│   ├── input/                # Source PDFs
│   ├── phase1_parsed/        # Raw parsed layout elements
│   ├── phase2_routed/        # Routed text / image / table elements
│   ├── phase3_images/        # Image captions (BLIP + OCR)
│   ├── phase4_tables/        # Normalized table representations
│   ├── phase5_chunks/        # Final structured chunks
│   └── embeddings/           # FAISS index and metadata
│
├── src/
│   ├── phase1_parse.py       # PDF parsing (Unstructured)
│   ├── phase2_route.py       # Modality routing
│   ├── phase3_images.py      # Image captioning + selective OCR
│   ├── phase4_tables.py      # Table normalization
│   ├── phase5_chunk.py       # Structure-aware chunking
│   ├── phase6_embed_faiss.py # Embeddings + FAISS indexing
│   └── phase7_query.py       # Retrieval and query interface
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔍 Phase-wise Description

### Phase 1 – PDF Parsing

* Layout-aware parsing into Title, Text, Table, and Image elements
* Page numbers and coordinates preserved
* No LLM usage (deterministic ingestion)

### Phase 2 – Routing

* Rule-based separation of elements by modality
* Ensures clean downstream processing

### Phase 3 – Image Processing

* BLIP used for semantic captioning
* Images classified as decorative or informative
* OCR applied only when necessary

### Phase 4 – Table Processing

* Raw tables preserved for numerical accuracy
* Normalized textual form created for retrieval

### Phase 5 – Chunking

* Title-based, structure-aware chunk formation
* Multimodal content merged into unified chunks
* Page references stored per chunk

### Phase 6 – Embedding & Indexing

* Chunks embedded using BGE
* Indexed locally using FAISS (cosine similarity)

### Phase 7 – Retrieval & Querying

* Semantic retrieval without LLM (validation mode)
* LLM invoked only at query time for answer generation

---

## 🔐 Key Design Principles

* No LLM usage during ingestion
* One unified embedding space for all modalities
* Deterministic preprocessing for enterprise safety
* Fully offline and auditable pipeline
* Page-level traceability for all responses

---

## 🧪 Current Capabilities (PoA Scope)

* Multimodal document ingestion (text, tables, images)
* Accurate semantic retrieval
* Page-referenced responses
* Local, offline execution
* Agent-ready architecture for future extensions

---

## 🚀 Future Work

* Tool / function calling for enterprise actions
* Conversational memory for follow-up queries
* Advanced chart understanding
* Role-based access control

---

## 🏁 Conclusion

This PoA demonstrates a **robust, enterprise-grade foundation** for building safe and explainable agentic AI systems.
By combining deterministic ingestion, semantic retrieval, and controlled generation, the system avoids common LLM pitfalls while remaining practical and extensible.