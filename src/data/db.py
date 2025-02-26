import os
from sqlmodel import create_engine, SQLModel, Session
from src.models.festival import Festival

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "fastapi-db" 
db_port: int = 3306  
db_name: str = "cochesdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("db_url",DATABASE_URL), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Festival(nombre="RBF", artista="Quevedo", horas=2))
        session.add(Festival(nombre="Puro Latino", artista="Anuel AA", horas=1))
        session.add(Festival(nombre="Coca Cola Music", artista="Noriel", horas=3))
        session.commit()
        #session.refresh_all()