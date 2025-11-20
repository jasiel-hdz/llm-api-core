import uvicorn
from fastapi import FastAPI
from database import Base, engine
from core.llm.routes import llm_router



app = FastAPI()

api = '/api/v1'

app.include_router(llm_router, prefix=f'{api}/llm', tags=['llm']) 

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)