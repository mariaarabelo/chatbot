# 🍽 Portuguese Recipe Chatbot

## 🚀 Features
- Fast semantic search with FAISS Index.
- Uses LangChain for handling chats.
- User-friendly Gradio web interface.

## 🛠 Set Up

### *Create a Virtual Environment*
```
python -m venv venv
```

### *Activate the Virtual Environment*
- *Windows:*  
  ```
  .\venv\Scripts\activate
  ```
- *Mac/Linux:*  
  ```
  source venv/bin/activate
  ```

### *Install Dependencies*
```
pip install -r requirements.txt
```


## 🔧 Usage

### *Running the Application*
```
python src/app.py
```

## *📖 Text Extraction & FAISS Indexing*
  - Different loaders for different types of documents.
  - Large text is splitted into smaller chunks.
  - FAISS indexes these chunks for fast similarity search.

Happy cooking! 🍽

$env:KMP_DUPLICATE_LIB_OK="TRUE"