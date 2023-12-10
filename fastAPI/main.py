from fastapi import FastAPI
import api_db_conn
from typing import Dict, Any
from pydantic import BaseModel
from api_db_conn import Company, Client, SolarBoards, CompanyRequest, CompanyDeleteRequest

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getall")
async def getall():
    return api_db_conn.select_all()

@app.get("/getclient/{id}")
async def getall(id: int):
    return api_db_conn.select_clients(id)


@app.get("/status")
async def status():
    if api_db_conn.testar_conexao():
        return {"status": "Conectado"}
    else:
        return {"status": "Não conectado"}
    
@app.post("/insert_company/")
async def insert_comp(company: CompanyRequest):
    return api_db_conn.insert_company(company) 

"""@app.post("/update_company/")
async def update_comp(company: CompanyRequest):
    return api_db_conn.update_company(company)

@app.post("/delete_company/")
async def delete_comp(company: CompanyDeleteRequest):
    return api_db_conn.delete_company(company)
    """