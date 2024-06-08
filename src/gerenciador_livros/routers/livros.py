from pathlib import Path
from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from ..database import get_session
from ..models import Livro

templates_dir = Path('.') / 'src' / 'gerenciador_livros' / 'templates'

router = APIRouter(
    prefix='/livros',
    tags=['livros', 'livro'],
)
templates = Jinja2Templates(
    directory=[(templates_dir), (templates_dir / 'livros')]
)

Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_class=HTMLResponse)
def listar_livros(request: Request, session: Session):
    livros = session.execute(select(Livro)).scalars()

    return templates.TemplateResponse(
        request=request, name='index.html', context={'livros': livros}
    )


@router.get('/criacao/', response_class=HTMLResponse)
def criar_livro_pagina(request: Request):
    return templates.TemplateResponse(name='criacao.html', request=request)


@router.post('/', response_class=HTMLResponse)
def criar_livro(
    request: Request,
    titulo: Annotated[str, Form()],
    data_publicacao: Annotated[str, Form()],
    autor_id: Annotated[str | None, Form()],
    session: Session,
):
    ano, mes, dia = data_publicacao.split('-')

    livro = Livro(
        titulo=titulo,
        data_publicacao=date(int(ano), int(mes), int(dia)),
        autor_id=autor_id,
    )

    session.add(livro)
    session.commit()

    return RedirectResponse(
        url=router.url_path_for('listar_livros'), status_code=302
    )


@router.get('/{livro_id}', response_class=HTMLResponse)
def ler_livro(livro_id: int, request: Request, session: Session):
    livro = session.execute(
        select(Livro).where(Livro.id == livro_id)
    ).scalar_one_or_none()
    
    return templates.TemplateResponse(
        name='detalhes.html', request=request,
        context={'livro': livro}    
    )