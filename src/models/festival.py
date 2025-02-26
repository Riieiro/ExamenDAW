from sqlmodel import Field, SQLModel

class Festival(SQLModel, table=True):
    nombre: str | None = Field(default=None, primary_key=True)
    artista: str = Field(index=True, max_length=50)
    horas: int = Field(gt=0)

