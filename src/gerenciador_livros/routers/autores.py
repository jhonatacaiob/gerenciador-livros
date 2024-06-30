from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from ..database import get_session
from ..models import Autor

templates_dir = Path('.') / 'src' / 'gerenciador_livros' / 'templates'

router = APIRouter(
    prefix='/autores',
    tags=['autores'],
)
templates = Jinja2Templates(
    directory=[(templates_dir), (templates_dir / 'autores')]
)

Session = Annotated[Session, Depends(get_session)]


@router.get('/options', response_class=HTMLResponse)
def listar_autor_options(request: Request, session: Session):
    autores = session.scalars(select(Autor)).all()
    return templates.TemplateResponse(
        request=request, name='options.html', context={'autores': autores}
    )
