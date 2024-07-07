from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
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

Session = Annotated[Session, Depends(get_session)]  # type: ignore


@dataclass
class BodyForm:
    titulo: Annotated[str, Form()]
    data_publicacao: Annotated[date, Form()]
    autor_id: Annotated[int, Form()]


@router.get('/', response_class=HTMLResponse)
def listar_livros(request: Request, session: Session):
    livros = session.scalars(select(Livro)).all()

    return templates.TemplateResponse(
        request=request, name='index.html.jinja', context={'livros': livros}
    )


@router.get('/criacao/', response_class=HTMLResponse)
def criar_livro_pagina(request: Request):
    return templates.TemplateResponse(
        name='criacao.html.jinja', request=request
    )


@router.post('/', response_class=HTMLResponse)
def criar_livro(
    request: Request,
    session: Session,
    form_data: BodyForm = Depends(),
):
    livro = Livro(
        titulo=form_data.titulo,
        data_publicacao=form_data.data_publicacao,
        autor_id=form_data.autor_id,
    )

    session.add(livro)
    session.commit()

    return RedirectResponse(
        url=router.url_path_for('listar_livros'),
        status_code=status.HTTP_302_FOUND,
    )


@router.get('/edicao/{livro_id}/', response_class=HTMLResponse)
def editar_livro_pagina(livro_id: int, request: Request, session: Session):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    return templates.TemplateResponse(
        name='edicao.html.jinja', request=request, context={'livro': livro}
    )


@router.put('/{livro_id}/', response_class=HTMLResponse)
def editar_livro(
    livro_id: int,
    request: Request,
    session: Session,
    form_data: BodyForm = Depends(),
):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if livro:
        livro.titulo = form_data.titulo
        livro.data_publicacao = form_data.data_publicacao
        livro.autor_id = form_data.autor_id

    session.add(livro)
    session.commit()

    return RedirectResponse(
        url=router.url_path_for('listar_livros'),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get('/{livro_id}/', response_class=HTMLResponse)
def ler_livro(livro_id: int, request: Request, session: Session):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    return templates.TemplateResponse(
        name='detalhes.html.jinja', request=request, context={'livro': livro}
    )


@router.delete(
    '/{livro_id}/',
    response_class=Response,
)
def excluir_livro(livro_id: int, request: Request, session: Session):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    session.delete(livro)
    session.commit()
