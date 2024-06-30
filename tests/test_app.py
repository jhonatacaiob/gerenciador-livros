def test_index(client):
    response = client.get('/')

    assert response.status_code == 200


def test_index_redireciona_para_pagina_livros(client):
    response = client.get('/')

    assert response.template.name == 'index.html'
    assert len(response.history) > 0
