from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

#PARA INICIAR: uvicorn main:app --reload

#Diccionario de usuarios
fake_users_db  = {
    "Lelouch":{
        "username":"Lelouch",
        "fullname":"99th Emperor of the Britanian Empire Lelouch",
        "email":"emperor.britania@britnian.geass",
        "hashed_password":"fakehashedgeass",
        "disbled": "true",
    },
    "Palpatine":{
        "username":"TheEmperor66",
        "fullname":"The Senate Sheev Palpatine",
        "email":"supreme_Chancellor@XOXOrepublic.darth",
        "hashed_password":"fakehashedgosith",
        "disabled": "true",    
        },
}

#Diccionario de URLS
urls ={"wwww.google.com":"google",
        "www.amazon.com":"amazon",}

app = FastAPI()

"""
Verificacion de usuarios
"""

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


#Tipo de dato para almacenar URL en el diccionario
class url(BaseModel):
    url_id: str
    url_short: str


"""
Shortener de URLS
"""
#Función en la que metes el value y diccionario y te devuelve el Key que lo contiene
def conversor_short(dictio , short):
    for i in dictio:
        if dictio[i] == short:
            return i


#Pagina Inicial
@app.post("/")
async def root():
    return {"message":"Hito 1-2, API de shortener."}


#Función para insertar URL en el diccionario
@app.post("/register/{url_id}/{url_short}")
async def register_url(url_id, url_short, token: str = Depends(get_current_active_user)):
    urls[url_id] = url_short
    make_sure = url_id
    for id, short in urls.items():
        if id == make_sure:
            return True #Si ha entrado la URL y el short dentro del diccionario, devuelve True
    return False #Si no ha entrado en el diccionario devuelve False
    
#Función para visualizar el diccionario
@app.get("/registered_URLS/")
async def urls_registered(token: str = Depends(get_current_active_user)):
    return urls

@app.get("/redirect/{short}")
async def redirect(short):
    if short in urls.values():
        return RedirectResponse(conversor_short(urls,short))
    else:
        return RedirectResponse("https://amazon.com")
