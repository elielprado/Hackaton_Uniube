from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, relationship
import pymssql
from typing import Optional
from pydantic import BaseModel

Base = declarative_base()

driver = 'mssql+pyodbc'
server = 'localhost'
database = 'SunMonitor'
username = 'apidb'
password = 'apidb'
port = '1433'
conn = f'{driver}://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server'

engine = create_engine(conn, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Company(Base):
    __tablename__ = 'Company'
    Company_ID =  Column(Integer, primary_key=True, index=True, autoincrement=True)
    Company_Name = Column(String(100), nullable=False)
    Capacity = Column(Integer, nullable=False)

    clients = relationship("Client", back_populates="company")
    solar_boards = relationship("SolarBoards", back_populates="company")

class CompanyRequest(BaseModel):
   # Company_ID: Optional[int] = None
    Company_Name: str
    Capacity: int

class CompanyDeleteRequest(BaseModel):
    Company_ID: int

class Client(Base):
    __tablename__ = 'Client'

    Client_ID = Column(Integer, primary_key=True, index=True)
    Company = Column(Integer, ForeignKey('Company.Company_ID'), nullable=False)
    Name = Column(String(100), nullable=False)
    Address = Column(String(150), nullable=False)
    Email = Column(String(100), nullable=False)
    Login_User = Column(String(50), nullable=False)
    Login_Password = Column(String(50), nullable=False)

    company = relationship("Company", back_populates="clients")
    solar_boards = relationship("SolarBoards", back_populates="client")

class SolarBoards(Base):
    __tablename__ = 'SolarBoards'

    SolarBoards_ID = Column(Integer, primary_key=True, index=True)
    Status = Column(String(50), nullable=False)
    Alarms = Column(Boolean, nullable=False)
    Company = Column(Integer, ForeignKey('Company.Company_ID'), nullable=False)
    Client = Column(Integer, ForeignKey('Client.Client_ID'), nullable=False)

    company = relationship("Company", back_populates="solar_boards")
    client = relationship("Client", back_populates="solar_boards")

def testar_conexao():
    try:
        engine.raw_connection()
        engine.dispose()
        return True
    except:
        return False
    


def select_all():
    try:
        connect_db()
        
        # Selecionar informações dos clientes e companhias
        clients = session.query(Client).all()
        companies = session.query(Company).all()
        
        # Montar a estrutura de dados conforme o formato desejado
        data = []
        for company in companies:
            for client in clients:
                if client.Company == company.Company_ID:
                    entry = {
                        "company_name": company.Company_Name,
                        "cliente": {
                            "nome": client.Name,
                            "endereco": client.Address,
                            "email": client.Email
                        },
                        "capacidade": company.Capacity,
                        "alarms": {
                            "off": True if client.solar_boards else False  # Verifica se há painéis solares associados ao cliente
                        }
                    }
                    data.append(entry)
        
        return {
            "status": "success",
            "message": "Requisição realizada com sucesso!",
            "data": data,
            "statusCode": 200
        }
    
    except(Exception, pymssql.Error) as error:
        return {
            "status": "error",
            "message": "Erro ao processar a requisição",
            "data": [],
            "statusCode": 500
        }
                
    finally:
        disconnect_db()

    
def connect_db():
    try:
        engine.connect()
        return True
    except:
        return False
    
def disconnect_db():
    try:
        engine.dispose()
        return True
    except:
        return False
    

def select_company():
    try:
        connect_db()
        return session.query(Company).all()
    except(Exception, pymssql.Error) as error:
        print("Error while connecting to MSSQL", error)
        return False
    
def select_solarboards():
    try:
        connect_db()
        return session.query(SolarBoards).all()
    except(Exception, pymssql.Error) as error:
        print("Error while connecting to MSSQL", error)
        return False
    
def select_clients(id):
    try:
        connect_db()
        client = session.query(Client).filter(Client.Client_ID == id).first()
           
        
        # Montar a estrutura de dados do cliente
        client_data = {
            "Client_ID": client.Client_ID,
            "Name": client.Name,
            "Company": client.company.Company_Name,
            "Address": client.Address,
            "Email": client.Email,
            "Login_User": client.Login_User,
        }
        
        return {
            "status": "success",
            "message": "Requisição realizada com sucesso!",
            "data": client_data,
            "statusCode": 200
        }
    
    except(Exception, pymssql.Error) as error:
        return {
            "status": "error",
            "message": "Erro ao processar a requisição",
            "data": [],
            "statusCode": 500
        }
    #raise HTTPException(status_code=500, detail="Erro ao processar a requisição")
    finally:
        disconnect_db()

def insert_company(company_data: Company):
    try:
        connect_db()
        new_company = Company(
            Company_Name = company_data.Company_Name,
            Capacity = company_data.Capacity
        )
        session.add(new_company)
        session.commit()

        return {
                "status": "success",
                "message": "Empresa criada com sucesso!",
                "data": {
                "Company_ID": new_company.Company_ID,
                "Company_Name": new_company.Company_Name,
                "Capacity": new_company.Capacity
            },
            "statusCode": 201  # Código 201 indica criação bem-sucedida  }  
        }
    
        
    except(Exception, pymssql.Error) as error:
        return {
            "status": "error",
            "message": "Erro ao processar a requisição",
            "data": [],
            "statusCode": 500
        }
    
def update_company(company):
    pass

def delete_company(company_id: int):
    pass
    """
        try:
        connect_db()
        
        # Buscar a empresa pelo ID
        company = session.query(Company).filter(CompanyDeleteRequest.Company_ID == company_id)
        print("Imprimindo: ", company)
        return company
        if not company:
            return{
                "status": "error",
                "message": "Empresa não encontrada!",
                "data": [],
                "statusCode": 404
            }
        
        # Deletar a empresa
        session.delete(company.Company_ID)
        session.commit()
        
        return {"status": "success", "message": "Empresa deletada com sucesso!"}
    
    except(Exception, pymssql.Error) as error:
        return{
            "status": "error",
            "message": "Erro ao processar a requisição",
            "data": [],
            "statusCode": 500
        }
    finally:
        disconnect_db()
"""