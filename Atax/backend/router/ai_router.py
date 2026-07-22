import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


def rule_router(text: str) -> str:
    t = (text or "").strip().lower()
    if not t:
        return "clarify"

    if any(k in t for k in ["error", "bug", "traceback", "exception", "failing", "debug", "fix"]):
        return "coding"
    if any(k in t for k in ["write", "function", "script", "class", "code", "python", "java", "javascript", "api", "sql", "node", "react"]):
        return "coding"
    if any(k in t for k in ["explain", "what is", "why", "how does", "how do", "summarize", "what does"]):
        return "explain"
    return "general"


class PromptRouter:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.label_encoder = LabelEncoder()
        self._train()

    def _train(self):
        data = [
            ("fix this python error", "coding"),
            ("debug this traceback", "coding"),
            ("write a function to sort a list", "coding"),
            ("how do I install pandas", "coding"),
            ("why does my loop not stop", "coding"),
            ("build a react app", "coding"),
            ("write a REST API in Flask", "coding"),
            ("explain transformer attention", "explain"),
            ("what is a vector database", "explain"),
            ("summarize this paragraph", "explain"),
            ("how does backpropagation work", "explain"),
            ("why does attention work", "explain"),
            ("what is a neural network", "explain"),
            ("explain embeddings in NLP", "explain"),
            ("what is supervised learning", "explain"),
        ]
        df = pd.DataFrame(data, columns=["text", "label"])
        X = self.vectorizer.fit_transform(df["text"])
        y = self.label_encoder.fit_transform(df["label"])
        self.model.fit(X, y)

    def predict_label(self, text: str) -> str:
        x = self.vectorizer.transform([text])
        pred_idx = int(self.model.predict(x)[0])
        return str(self.label_encoder.inverse_transform([pred_idx])[0])

    def route_query(self, text: str) -> dict:
        t = (text or "").strip().lower()
        if not t:
            return {"route": "clarify", "rule": "clarify", "classifier": "clarify"}

        rule = rule_router(t)
        classifier = self.predict_label(t)

        explain_markers = ["what is", "explain", "how does", "how do", "why", "what does", "summarize"]
        if any(k in t for k in explain_markers):
            route = "explain"
        elif rule == "coding" or classifier == "coding":
            route = "coding"
        else:
            route = "general"

        return {
            "route": route,
            "rule": rule,
            "classifier": classifier,
        }


router = PromptRouter()


def route_query(text: str) -> dict:
    return router.route_query(text)
