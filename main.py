from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

usuarios_db ={
        "nombre": "hatsune",
        "contraseña": "miku"
}


#INICIALIZAR: uvicorn main:app --reload

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Estructura que utilizaremos para guardar los usurarios con permisos de utilización
class User(BaseModel):
    usuario: str
    contraseña: str

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(User):
    hashed_password: str


def get_user(db, usuario: str):
    if usuario in db:
        user_dict = db[usuario]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(usuarios_db, token)
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = usuarios_db.get(form_data.nombre)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecto")
    user = UserInDB(**user_dict)
    hashed_password = usuarios_db.get(form_data.contraseña)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecto")

    return {"access_token": user.username, "token_type": "bearer"}





#Estructura que utilizaremos para guardar los datos que recojamos

class Url(BaseModel):
    url_id: str
    url_normal: str

#El diccionario donde guardaremos los datos que recojamos

urls = {}

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
 
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
async def enseñar_lista():
    return print(urls)

