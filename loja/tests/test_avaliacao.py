import pytest
from django.core.exceptions import ValidationError
from loja.models import Avaliacao, Produto, Usuario, Fornecedor

@pytest.fixture
def usuario():
  return Usuario.objects.create(
    nome="Test User",
    email="testuser@example.com",
    senha="password123"
  )

@pytest.fixture
def produto():
  fornecedor = Fornecedor.objects.create(
      nome="Test Fornecedor",
      telefone="123456789",
      email="fornecedor@example.com",
      endereco="123 Test St",
      cnpj="12345678000100"
  )
  return Produto.objects.create(
      nome="Test Product",
      descricao="Test Description",
      preco=10.0,
      estoque=10,
      fornecedor=fornecedor
  )

@pytest.mark.django_db
def test_avaliacao_creation(usuario, produto):
  avaliacao = Avaliacao.objects.create(
    usuario=usuario,
    produto=produto,
    nota=5,
    comentario="Test Comment"
  )

  avaliacao.full_clean()
  avaliacao.save()

  avaliacao_from_db = Avaliacao.objects.get(id=avaliacao.id)

  assert avaliacao.usuario == avaliacao_from_db.usuario
  assert avaliacao.produto == avaliacao_from_db.produto
  assert avaliacao.nota == avaliacao_from_db.nota
  assert avaliacao.comentario == avaliacao_from_db.comentario

@pytest.mark.django_db
def test_avaliacao_update(usuario, produto):
  avaliacao = Avaliacao.objects.create(
    usuario=usuario,
    produto=produto,
    nota=5,
    comentario="Test Comment"
  )

  avaliacao.nota = 4
  avaliacao.save()

  updated_avaliacao = Avaliacao.objects.get(id=avaliacao.id)

  assert updated_avaliacao.nota == 4

@pytest.mark.django_db
def test_avaliacao_deletion(usuario, produto):
  avaliacao = Avaliacao.objects.create(
    usuario=usuario,
    produto=produto,
    nota=5,
    comentario="Test Comment"
  )
  avaliacao_id = avaliacao.id
  avaliacao.delete()
  with pytest.raises(Avaliacao.DoesNotExist):
    Avaliacao.objects.get(id=avaliacao_id)

@pytest.mark.django_db
def test_avaliacao_nota_invalida(usuario, produto):
  with pytest.raises(ValidationError):
    avaliacao = Avaliacao(usuario=usuario, produto=produto, nota="6", comentario="Test Comment")
    avaliacao.full_clean()


@pytest.mark.django_db
def test_avaliacao_usuario_nulo(produto):
  with pytest.raises(ValidationError):
    avaliacao = Avaliacao(usuario=None, produto=produto, nota=5, comentario="Test Comment")
    avaliacao.full_clean()

@pytest.mark.django_db
def test_avaliacao_produto_nulo(usuario):
  with pytest.raises(ValidationError):
    avaliacao = Avaliacao(usuario=usuario, produto=None, nota=5, comentario="Test Comment")
    avaliacao.full_clean()
