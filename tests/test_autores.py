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


def test_listar_autores_options_deve_retornar_template_options_autores(
    client, session
):
    response = client.get('/autores/options/')

    assert response.template.name == 'options.html.jinja'
