from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#PARA INICIAR: uvicorn main:app --reload

app = FastAPI()

#Diccionario de URLS
urls ={"wwww.google.com":"google",
        "www.amazon.com":"amazon",}

#Tipo de dato para almacenar URL en el diccionario
class url(BaseModel):
    url_id: str
    url_short: str



"""
Shortener de URLS
"""
#
@app.post("/")
async def root():
    return {"message":"Hito 1-2, API de shortener."}


#Función para insertar URL en el diccionario
@app.post("/register/{url_id}/{url_short}")
async def register_url(url_id, url_short):
    urls[url_id] = url_short
    make_sure = url_id
    for id, short in urls.items():
        if id == make_sure:
            return True #Si ha entrado la URL y el short dentro del diccionario, devuelve True
    return False #Si no ha entrado en el diccionario devuelve False
    
#Función para visualizar el diccionario
@app.get("/registered_URLS")
async def urls_registered():
    return urls
