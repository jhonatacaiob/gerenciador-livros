from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .routers import autores, livros

app = FastAPI()

diretorio_app = Path('.') / 'src' / 'gerenciador_livros'

app.mount(
    '/static', StaticFiles(directory=(diretorio_app / 'static')), name='static'
)
app.include_router(livros.router)
app.include_router(autores.router)


@app.get('/', response_class=HTMLResponse)
def get_index():
    return RedirectResponse(url='/livros', status_code=301)
