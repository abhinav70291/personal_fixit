from supabase import create_client, Client


SUPABASE_URL="https://ojavvzgfskmghymsrgsd.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qYXZ2emdmc2ttZ2h5bXNyZ3NkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MDMwNjksImV4cCI6MjAyMjk3OTA2OX0.naAncNROfOwYTiCe-2gUE_K-Ps0XIrmY3uaE_-QSGZA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_pdf_name(document_name):
    try:
        response = supabase.table('fixit').upsert({"document_name": document_name}).execute()
    except:
        response = supabase.table('fixit').update({"document_name": document_name}).execute()
    return response

def document_list():
    response = supabase.table('fixit').select("*").execute()
    # Check if the response is successful and has data
    print("response:",response)
    try:
        document_names = [doc['document_name'] for doc in response.data]
        print("List of documents:", list(set(document_names)))
        return list(set(document_names))
    except Exception as e:
        # Handle errors or no data case
        print("Failed to fetch documents or no documents found.")
        return []