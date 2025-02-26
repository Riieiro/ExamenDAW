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
    return "Se ha añadido el festival"

@app.delete("/festival")
def borrar_festival(festival:Festival, session: SessionDep):
    fest=session.exec(select(Festival).where(Festival.nombre==festival.nombre)).first()
    if fest:
        session.delete(fest)
        session.commit()
    else:
        raise HTTPException(404,"Error al encontrar el festival")
    return "Se ha borrado el festival"


@app.put("/festival")
def modificar_festival(festival:Festival,session:SessionDep):
    fest=session.exec(select(Festival).where(Festival.nombre==festival.nombre)).first()
    if fest:
        fest.nombre=festival.nombre
        fest.artista=festival.artista
        fest.horas=festival.horas
        session.commit()
    else:
        raise HTTPException(404,"Error al encontrar el festival")
    return "Se ha modificado el festival"


@app.patch("/festival")
def modificar_festival(festival:Festival,session:SessionDep):
    fest=session.exec(select(Festival).where(Festival.nombre==festival.nombre)).first()
    if fest:
        fest.nombre=festival.nombre
        fest.artista=festival.artista
        fest.horas=festival.horas
        session.commit()
    else:
        raise HTTPException(404,"Error al encontrar el festival")
    return "Se ha modificado el festival"