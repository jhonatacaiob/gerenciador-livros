from random import randint

from src.gerenciador_livros.models import Autor

from .factories import AutorFactory


def test_listar_autor_options_deve_retornar_uma_lista_de_autores(
    client, session
):
    session.bulk_save_objects(AutorFactory.create_batch(5))
    session.commit()

    response = client.get('/autores/options/')

    for autor in response.context['autores']:
        assert isinstance(autor, Autor)


def test_listar_autores_options_deve_retornar_lista_vazia_quando_nao_ha_autor(
    client, session
):
    response = client.get('/autores/options/')

    assert len(response.context['autores']) == 0


def test_listar_autores_options_deve_retornar_todos_os_autores_criados(
    client, session
):
    len_autores = 10
    session.bulk_save_objects(AutorFactory.create_batch(len_autores))
    session.commit()

    response = client.get('/autores/options/')

    assert len(response.context['autores']) == len_autores


def test_listar_autores_options_deve_uma_opcao_vazia(client, session):
    session.bulk_save_objects(AutorFactory.create_batch(2))
    session.commit()

    response = client.get('/autores/options/')

    esperado = '<option value="" selected disabled hidden>Choose here</option>'

    assert esperado in response.content.decode()


def test_listar_autores_options_nao_deve_retornar_opcao_vazia_quando_parametro_passado(  # noqa
    client, session
):
    session.bulk_save_objects(AutorFactory.create_batch(2))
    session.commit()

    response = client.get('/autores/options/', params={'autor_selecionado': 1})

    nao_esperado = (
        '<option value="" selected disabled hidden>Choose here</option>'
    )

    assert nao_esperado not in response.content.decode()


def test_listar_autores_options_deve_retornar_com_uma_opcao_selecionada(
    client, session
):
    len_autores = 2
    session.bulk_save_objects(AutorFactory.create_batch(len_autores))
    session.commit()

    response = client.get('/autores/options/', params={'autor_selecionado': 1})

    assert '<option value="1" selected>' in response.content.decode()


def test_listar_autores_options_deve_retornar_com_uma_opcao_aleatoria_selecionada(  # noqa
    client, session
):
    len_autores = 10
    autor_selecionado = randint(1, len_autores)

    session.bulk_save_objects(AutorFactory.create_batch(len_autores))
    session.commit()

    response = client.get(
        '/autores/options/', params={'autor_selecionado': autor_selecionado}
    )

    esperado = f'<option value="{autor_selecionado}" selected>'

    assert esperado in response.content.decode()
