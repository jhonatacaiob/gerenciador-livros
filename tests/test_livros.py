from fastapi import status
from sqlmodel import select

from src.gerenciador_livros.models import Livro

from .factories import LivroFactory


def test_listar_livros_deve_retornar_200(client):
    response = client.get('/livros/')

    assert response.status_code == 200


def test_listar_livros_deve_uma_lista_de_livros(client, session, autor):
    len_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(len_livros, autor_id=autor.id)
    )
    session.commit()

    response = client.get('/livros/')

    for livro in response.context['livros']:
        assert isinstance(livro, Livro)


def test_listar_livros_deve_retornar_todos_os_livros_criados(
    client, session, autor
):
    len_livros = 10
    session.bulk_save_objects(
        LivroFactory.create_batch(len_livros, autor_id=autor.id)
    )
    session.commit()

    response = client.get('/livros/')

    assert len(response.context['livros']) == len_livros


def test_listar_livros_deve_retornar_lista_vazia_quando_nao_ha_livros(
    client, session, autor
):
    response = client.get('/livros/')

    assert len(response.context['livros']) == 0


def test_criar_livro_pagina_deve_retornar_template_criacao_livros(
    client, session
):
    response = client.get('/livros/criacao/')

    assert response.template.name == 'criacao.html.jinja'
    assert len(response.history) == 0


def test_criar_livro_deve_criar_um_registro_no_banco(client, session, autor):
    livro = LivroFactory(id=1, autor_id=autor.id)
    _ = client.post(
        '/livros/',
        data={
            'titulo': livro.titulo,
            'data_publicacao': livro.data_publicacao.strftime('%Y-%m-%d'),
            'autor_id': autor.id,
        },
    )

    stmt = select(Livro).where(Livro.id == 1)
    livro_banco = session.scalar(stmt)

    assert livro_banco == livro


def test_criar_livro_deve_redirecionar_para_index(client, session, autor):
    livro = LivroFactory(id=1, autor_id=autor.id)
    response = client.post(
        '/livros/',
        data={
            'titulo': livro.titulo,
            'data_publicacao': livro.data_publicacao.strftime('%Y-%m-%d'),
            'autor_id': autor.id,
        },
    )

    assert response.template.name == 'index.html.jinja'
    assert len(response.history) > 0


def test_ler_livro_deve_retornar_o_livro_com_o_mesmo_id(
    client, session, livro
):
    response = client.get(f'/livros/{livro.id}/')

    assert response.context['livro'] == livro


def test_ler_livro_deve_retornar_o_template_detalhes_livros(
    client, session, livro
):
    response = client.get(f'/livros/{livro.id}/')

    assert response.template.name == 'detalhes.html.jinja'
    assert len(response.history) == 0


def test_excluir_livro_deve_remover_um_registro_no_banco(
    client, session, livro
):
    _ = client.delete(f'/livros/{livro.id}/')

    stmt = select(Livro).where(Livro.id == livro.id)
    livro_banco = session.scalar(stmt)

    assert livro_banco is None

