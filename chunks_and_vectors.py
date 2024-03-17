import os
from pinecone import Pinecone
from parse import parse_pdf
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


from document_list import upload_pdf_name
from langchain.embeddings import HuggingFaceEmbeddings

# Initialize device
device="cpu"

# Inititalize embedding_model
embedding_model="sentence-transformers/all-MiniLM-L6-v2" 
embedding = HuggingFaceEmbeddings(model_name=embedding_model, model_kwargs={'device':device})

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

cwd = os.getcwd()
pc = Pinecone(api_key="69895c60-6cf3-44e9-a23d-f5ac7d826e80")
index = pc.Index("fixit-abhinav")


# model_id = "sentence-transformers/all-MiniLM-L6-v2"
# hf_token = "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"

# api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
# headers = {"Authorization": f"Bearer {hf_token}"}

def recursive_character_text_splitter(text, max_length=2000, overlap=200):
    if len(text) <= max_length:
        return [text]
    else:
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        overlap_index = max(0, split_index - overlap)
        return [text[:split_index+1]] + recursive_character_text_splitter(text[overlap_index+1:].lstrip(), max_length, overlap)

async def text_to_vector(texts, file_name):
    chunks = recursive_character_text_splitter(texts, max_length=1000, overlap=100)
    print("length of chunks:",len(chunks))
    
    for i,chunk in enumerate(chunks):
        vector=embedding.embed_query(chunk)
        index.upsert(vectors=[(f"{file_name}_{i}", vector, {"filename": file_name, "content": chunk})])
        print("vectors upserted")
    upload_pdf_name(file_name)
    print("pdf name updated on supabase")



async def query_vectors(query_text, file_name):
    print("starting query")
    # Convert the query text to a vector
    query_vector = embedding.embed_query(query_text)
    print("query vectorized")
    print("file_name:",file_name)
    if file_name:
        metadata_filter = {"filename": {'$eq': f'{file_name}'}}
        response = index.query(vector=query_vector, top_k=6,include_metadata=True,filter=metadata_filter)
    else:
        response = index.query(vector=query_vector, top_k=6,include_metadata=True)
    # Return the query results
    chunks=[]
    for item in response["matches"]:
        chunk=item["metadata"]["content"]
        chunks.append(chunk)

    prompt = f'''Given a user query: {query_text}, provide a detailed and elaborate answer to it strictly based on the content of these chunks: {chunks}.
             If the question cannot be answered, simply state that it cannot be answered politely.For normal user interactions, introduce yourself as FIXIT AI with your capabilities only.
             Write strictly in Markdown format.End your response stating "Thank you for using FIXIT AI". Add anything else if you feel like goes accordingly'''


    # Use OpenAI's GPT-3 model to generate the response
    messages = [{'role': 'system',
                    'content': '''You are a document question answering chatbot named "FIXIT AI" designed to assist users with answering questions based on the chunks retrieved from their own documents. Please provide a detailed and elaborate answer to the user query based on the content of these chunks. 
                    If the question cannot be answered,or if the chunks do not contain the asnwer,  simply state that it cannot be answered politely.
                    .Asnwer in  Markdown format  strictly.Make sure you adress the query of the user. For normal user interactions such as HI /hello/ what's up , introduce yourself as I am FIXIT AI with your capabilities only'''},
                {'role': 'user', 'content': prompt.lower()}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        max_tokens=1000,
        top_p=0.7,
        seed=12345,
        # Set stream parameter to True
        )

    try:
        return response.choices[0].message.content, chunks
    except Exception as e:
        return None



# Loading and trying open source models
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
# model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")

# inputs = tokenizer.encode(prompt, return_tensors='pt')

# try:
#     # Generate the output
#     outputs = model.generate(inputs, max_length=1000, do_sample=True)
#     # Decode the output
#     answer = tokenizer.decode(outputs[0])
#     print("answer: ",answer)
# except Exception as e:
#     print(f"An error occurred: {e}")




    



