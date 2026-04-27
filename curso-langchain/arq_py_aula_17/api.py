from fastapi import FastAPI
from langserve import add_routes

from main_api_assinc import runnable_with_history

app = FastAPI(title="Atendimento Saúde",
              description="Chatbot responsável por informar, orientar e registrar casos de dengue!")

add_routes(app, runnable_with_history, path="/chat")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)