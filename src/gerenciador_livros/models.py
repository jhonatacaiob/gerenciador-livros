from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Base(SQLModel):
    ...


class Autor(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    livros: list['Livro'] = Relationship(back_populates='autor')


class Livro(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    data_publicacao: date = Field()
    autor_id: int = Field(default=None, foreign_key='autor.id')
    autor: Autor = Relationship(back_populates='livros')
