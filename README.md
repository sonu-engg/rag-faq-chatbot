# RAG FAQ Chatbot (Work in Progress)

A chatbot that answers questions using only the information in a provided
document — built using Retrieval-Augmented Generation (RAG), so answers
are grounded in real data instead of the model's general knowledge.

## How it works

1. A text document is split into chunks
2. Each chunk is converted into an embedding (a numerical representation of its meaning)
3. Embeddings are stored in a local vector database (ChromaDB)
4. When a question is asked, the most relevant chunks are retrieved
5. The AI answers using only those retrieved chunks as context

## Example

**Document contains:** company FAQ (business hours, refund policy, shipping, etc.)

**Question:** "Can I get my money back if I don't like the product?"
**Answer:** Retrieves the refund policy chunk and answers correctly — even
though the question doesn't use the word "refund."

**Question:** "What's your favorite color?"
**Answer:** Correctly states it doesn't have that information, instead of
making something up.

## Requirements

- Python 3.9 or higher
- A free Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

## Setup

1. Clone this repository:git clone https://github.com/sonu-engg/rag-faq-chatbot.git
cd rag-faq-chatbot




2. Create and activate a virtual environment:python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt



4. Create a `.env` file in the project root and add your API key:

GEMINI_API_KEY=your_key_here



5. Run it:

python rag_chatbot.py



## Status

This is a learning/experimental version using a small sample FAQ file.
Planned improvements: support for PDF/website input, a real client-facing
document, and integration into a broader automation workflow (e.g. n8n).


