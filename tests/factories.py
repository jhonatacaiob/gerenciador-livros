import factory

from src.gerenciador_livros.models import Autor, Livro


class AutorFactory(factory.Factory):
    class Meta:
        model = Autor

    nome = factory.Faker('name', locale='pt_BR')


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Faker('sentence', locale='pt_BR')
    data_publicacao = factory.Faker('date_object', locale='pt_BR')
    autor_id = factory.SelfAttribute('autor.id')
    autor = factory.SubFactory(AutorFactory)
