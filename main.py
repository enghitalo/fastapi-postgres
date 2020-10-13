from typing import List
from variables import YOUR_DATABASE_URL
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional




# from typing import List
# import databases
# import sqlalchemy
# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import os
# import urllib

# #DATABASE_URL = "sqlite:///./test.db"

# host_server = os.environ.get('host_server', 'localhost')
# db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '45641')))
# database_name = os.environ.get('database_name', 'postgres')
# db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
# db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'admin')))
# ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
DATABASE_URL = YOUR_DATABASE_URL
# DATABASE_URL = "postgresql://user:password@postgresserver/db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "teste",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.INT),
    # sqlalchemy.Column("Tumbnail", sqlalchemy.CHAR),
    sqlalchemy.Column("nome", sqlalchemy.CHAR),
    # sqlalchemy.Column("Departamento", sqlalchemy.CHAR),
    sqlalchemy.Column("home_page_categories", sqlalchemy.CHAR),
    sqlalchemy.Column("tipo", sqlalchemy.CHAR),
    # sqlalchemy.Column("gender", sqlalchemy.CHAR),
    # sqlalchemy.Column("Garantia", sqlalchemy.INTEGER),
    # sqlalchemy.Column("Realease", sqlalchemy.DATETIME),
    # sqlalchemy.Column("NPS", sqlalchemy.REAL),
    # sqlalchemy.Column("Vida Útil", sqlalchemy.INTEGER),
    sqlalchemy.Column("marca", sqlalchemy.CHAR),
    # sqlalchemy.Column("Descrição", sqlalchemy.TEXT),
    # sqlalchemy.Column("Peso", sqlalchemy.INTEGER),
    # sqlalchemy.Column("Volume", sqlalchemy.REAL),
    sqlalchemy.Column("categoria", sqlalchemy.CHAR),
    sqlalchemy.Column("subcategoria", sqlalchemy.CHAR),
    # sqlalchemy.Column("Modelo", sqlalchemy.CHAR),
    # sqlalchemy.Column("Detalhes", sqlalchemy.CHAR),

)

engine = sqlalchemy.create_engine(
    #DATABASE_URL, connect_args={"check_same_thread": False}
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    # tumbnail: str = None
    nome: str = None
    # departamento: str = None
    home_page_categories: str = None
    tipo: str = None
    # gender: str
    # garantia: str = None
    # realease: str = None
    # nps: str = None
    # lifespan: int =None
    marca: str = None
    # description: str = None
    # peso: str = None
    # volume: str = None
    categoria: str = None
    subcategoria: str = None
    modelo: str = None
    # detalhes: str = None


app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# @app.post("/hhhh/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await database.execute(query)
#     return {**note.dict(), "id": last_record_id}

# @app.put("/hhhh/{note_id}/", response_model=Note)
# async def update_note(note_id: int, payload: NoteIn):
#     query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
#     await database.execute(query)
#     return {**payload.dict(), "id": note_id}


@app.get("/products_store/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.get("/products_store/{note_id}/", response_model=Note)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.get("/teste/", response_model=List[Note])
async def read_notes(genders: str = None, marcas: str = None, home_page_categoriess:str=None):
    query = notes.select()
    if home_page_categoriess!=None:
        query = query.where(notes.c.home_page_categories == home_page_categoriess)
    if genders != None:
        query = query.where(notes.c.gender == genders)
    if marcas != None:
        query = query.where(notes.c.marca == marcas)

    # print("testinhi  ${\query  }")
    print(query.where(notes.c.home_page_categories == home_page_categoriess))

    # print("testinhi  ${\query }")

    return await database.fetch_all(query)

# @app.delete("/notes/{note_id}/")
# async def update_note(note_id: int):
#     query = notes.delete().where(notes.c.id == note_id)
#     await database.execute(query)
#     return {"message": "Note with id: {} deleted successfully!".format(note_id)}

