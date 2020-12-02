from fastapi import FastAPI
from pydantic import BaseModel

#INICIALIZAR: uvicorn main:app --reload

app = FastAPI()

#La estructura que utilizaremos para guardar los datos que recojamos

class Url(BaseModel):
    url_id: str
    url_normal: str

#El diccionario donde guardaremos los datos que recojamos

urls = {}
 
#La pagina principal, solo te dice el Hito en el que estamos y su titulo

@app.get("/")
async def root():
    return {"message": "Página principal. HITO 1: URLs-Shortener."}

#El metodo con el que añadimos datos a nuestro diccnionario, de momento es mejor usar /docs para añadir"

@app.post("/postear/{url_id1}/{url_normal1}")
async def postear(url_id1, url_normal1):
    urls[url_id1] = url_normal1
    return urls

#El metodo para poder enseñar todos los datos dentro del diccionario

@app.get("/enseñar")
async def enseñar():
    return print(urls)