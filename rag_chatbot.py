import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-flash-lite-latest"

# ---- STEP A: Load and chunk the document ----
def load_and_chunk(filepath):
    """Reads a text file and splits it into chunks by blank lines."""
    with open(filepath, "r") as f:
        content = f.read()
    # Split on double newlines — each Q&A pair becomes one chunk
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks

chunks = load_and_chunk("company_faq.txt")
print(f"Loaded {len(chunks)} chunks from the document.\n")

# ---- STEP B: Set up the vector database and store embeddings ----
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_docs")

# Generate an embedding for each chunk and store it
for i, chunk in enumerate(chunks):
    embedding_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )
    embedding_vector = embedding_response.embeddings[0].values

    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[embedding_vector],
        documents=[chunk]
    )

print("Document indexed and ready for questions.\n")

# ---- STEP C: Given a question, retrieve the most relevant chunks ----
def retrieve_relevant_chunks(question, n_results=2):
    question_embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    ).embeddings[0].values

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    return results["documents"][0]

# ---- STEP D: Answer using retrieved context ----
def answer_question(question):
    relevant_chunks = retrieve_relevant_chunks(question)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""Answer the customer's question using ONLY the information below.
If the answer isn't in the information provided, say you don't have that information.

Company information:
{context}

Customer question: {question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

# ---- Chat loop ----
print("Ask a question about the company. Type 'quit' to stop.\n")
while True:
    user_question = input("You: ")
    if user_question.lower() == "quit":
        break

    answer = answer_question(user_question)
    print("AI:", answer, "\n")
