from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from Conexion.conexionOracle import insertar_datos
from datetime import datetime

templateJinja = Jinja2Templates(directory="Frontend")
alertaCandidato = False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root(resquest: Request): 
    return templateJinja.TemplateResponse("index.html", {"request":resquest})

@app.post("/candidatos", response_class=HTMLResponse)
def create_candidato(resquest: Request,
                     usuario: Annotated[str, Form()], 
                     nombre:Annotated[str, Form(),], 
                     apellido:Annotated[str, Form(),], 
                     fecha_nacimiento:Annotated[str, Form(),], 
                     tipo_documento:Annotated[str, Form(),], 
                     numero_documento:Annotated[str, Form(),]):
    #Convertir la fecha de nacimiento para poderla ingresar bien a la BD
    print(fecha_nacimiento)
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").strftime("%d/%m/%Y")
    print(fecha_nacimiento,' ',nombre,' ', apellido, ' ',usuario, ' ',tipo_documento, ' ',numero_documento)

    alertaCandidato = insertar_datos(usuario, tipo_documento, nombre, apellido, fecha_nacimiento, numero_documento)
    
    print('aler', alertaCandidato)

    if alertaCandidato==True:
         return templateJinja.TemplateResponse("index.html", {"request":resquest, "alertaCandidato":alertaCandidato})
    else:
        return RedirectResponse("/", status_code=303)