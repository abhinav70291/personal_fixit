# Fixit AI - Personal Document Query Chatbot

## Overview
Fixit AI is a chatbot designed to facilitate document queries within personal documents. It leverages a FastAPI backend with two main endpoints, integrating with Pinecone for vector search and Supabase for metadata storage.

## Components
### Backend
- **FastAPI**: Provides robust, efficient APIs for handling document processing and querying.
- **Pinecone**: Used for storing and retrieving document vectors for efficient similarity search.
- **Supabase**: Acts as a metadata store for document filenames.

### Endpoints
1. **Document Chunking and Storage**:
   - **POST** `/chunk-and-store`
   - Takes in documents and prepares chunks using a recursive text character splitter (1000 characters, 200 overlap).
   - Stores chunks in Pinecone and adds the filename to Supabase.

2. **Query and Retrieve**:
   - **GET** `/query`
   - Accepts a query and an optional filename filter (selectable from the frontend).
   - Embeds the query, filters by filename, and retrieves the top 6 chunks from Pinecone.
   - Passes the chunks to OpenAI's GPT-3.5 Turbo API for completion.

## Installation
1. Clone the repository:
   ```bash
   git clone [your-repository-url]

## Usage
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload

## Usage
3. Start the Streamlit server:
   ```bash
   streamlit run streamlit_app.py


   
