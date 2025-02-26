from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func

from src.models.festival import Festival
from src.data.db import init_db, get_session


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

@app.get("/festival",response_model=list[Festival])
def lista_festival(session: SessionDep):
    fest=session.exec(select(Festival)).all()
    return fest

@app.post("/festival",response_model=Festival)
def subir_festival(festival:Festival,session: SessionDep):
    session.add(festival)
    session.commit()
    return festival

@app.delete("/festival",response_model=Festival)
def borrar_festival(festival:Festival, session: SessionDep):
    session.delete(festival)
    session.commit()
    return festival

@app.put("/festival",response_model=Festival)
def modificar_festival(festival:Festival,session:SessionDep):
    fest=session.exec(select(Festival).where(Festival.nombre==festival.nombre))
    if not fest:
        raise HTTPException(404,"Error al encontrar el festival")
    festival.artista=fest.artista
    festival.horas=fest.horas
    session.commit()
    return fest