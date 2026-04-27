# documentação: https://python.langchain.com/docs/langserve/
# tutorial: https://www.youtube.com/watch?v=7L0MnVu1KEo&t=130s
from fastapi import FastAPI
from langserve import add_routes

from main_api_assinc import runnable_with_history

app = FastAPI(title="Atendimento Online Smartfit",
              description="Eu sou a Bell, assistente virtual da Smart Fit. Aqui você pode encontrar respostas para suas principais dúvidas. ")

add_routes(app, runnable_with_history, path="/chat")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)