from fastapi import FastAPI
from pydantic import BaseModel

from Atax.backend.router.ai_router import PromptRouter

app = FastAPI(title="Atax AI Router")
router = PromptRouter()


class QueryRequest(BaseModel):
    prompt: str


class QueryResponse(BaseModel):
    route: str
    rule: str
    classifier: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/query", response_model=QueryResponse)
def handle_query(request: QueryRequest) -> QueryResponse:
    result = router.route_query(request.prompt)
    return QueryResponse(**result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Atax.backend.api.main:app", host="127.0.0.1", port=8000, reload=True)
