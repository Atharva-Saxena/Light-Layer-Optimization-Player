## Notebook plan

### Cell 1: install deps
```python
!pip install -q scikit-learn faiss-cpu sentence-transformers
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
```

### Cell 2: small dataset
```python
data = [
    ("fix this python error", "coding"),
    ("debug this traceback", "coding"),
    ("write a function to sort a list", "coding"),
    ("explain transformer attention", "explain"),
    ("what is a vector database", "explain"),
    ("summarize this paragraph", "explain"),
    ("how do I install pandas", "coding"),
    ("why does my loop not stop", "coding"),
]
df = pd.DataFrame(data, columns=["text", "label"])
df.head()
```

### Cell 3: rule router
```python
def rule_router(text):
    t = text.lower().strip()
    if not t:
        return "clarify"

    if any(k in t for k in ["error", "bug", "traceback", "exception", "failing", "debug"]):
        return "coding"
    if any(k in t for k in ["write", "function", "script", "class", "code", "python", "java", "javascript"]):
        return "coding"
    if any(k in t for k in ["explain", "what is", "why", "how does"]):
        return "explain"

    return "general"
```

Test it:
```python
    print(rule_router("fix this python error"))
    print(rule_router("explain attention"))
```

### Cell 4: classifier
```python
# TODO: build a simple text classifier
# use TfidfVectorizer + LogisticRegression
# fit on df["text"] and df["label"]
```

Use this structure:
```python
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression(max_iter=1000)
)
model.fit(df["text"], df["label"])
```

Check it:
```python
print(model.predict(["fix this java error", "what is a neural network"]))
```

### Cell 5: tiny retrieval layer
```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

docs = [
    "Python debugging tips for syntax and runtime errors",
    "How attention works in transformers",
    "How to write a function in Python",
    "What is a vector database",
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
```

Search function:
```python
def retrieve(query, top_k=2):
    q = model.encode([query], convert_to_numpy=True)
    D, I = index.search(q, top_k)
    return [docs[i] for i in I[0]]
```

Test:
```python
print(retrieve("how to debug python"))
```

### Cell 6: combined router
```python
def route_query(text):
    rule = rule_router(text)
    if rule in ["coding", "explain"]:
        return {
            "rule": rule,
            "classifier": model.predict([text])[0],
            "retrieval": retrieve(text, top_k=2)
        }

    return {
        "rule": rule,
        "classifier": model.predict([text])[0],
        "retrieval": []
    }
```

```python
print(route_query("fix this python error"))
print(route_query("what is a vector database"))
```


