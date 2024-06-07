from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select

from .models import Autor, Livro
from .database import get_session, engine

def lifespan(app):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)
diretorio_app = Path('.') / 'src' / 'gerenciador_livros'

app.mount('/static', StaticFiles(directory=(diretorio_app / 'static')), name='static')
templates = Jinja2Templates(directory=(diretorio_app / 'templates'))


Session = Annotated[Session, Depends(get_session)]

@app.get('/', response_class=HTMLResponse)
def get_index(request: Request, session: Session):

    autor1 = Autor(nome='Machado de assis')
    autor2 = Autor(nome='Guimarães rosa')
    session.add(autor1)
    session.add(autor2)
    session.commit()

    return templates.TemplateResponse(
        request=request, name='index.html', context={'autores': [autor1, autor2]}
    )
