import uvicorn
from fastapi import FastAPI
from database import Base, engine
from core.llm.routes import llm_router


app = FastAPI(
    title="LLM API Core",
    description="A FastAPI-based REST API service for interacting with Large Language Models (LLMs) using OpenAI",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI - Interactive API documentation
    redoc_url="/redoc",  # ReDoc - Alternative API documentation
    openapi_url="/openapi.json",  # OpenAPI schema JSON
)

api = '/api/v1'

app.include_router(llm_router, prefix=f'{api}/llm', tags=['llm']) 

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)