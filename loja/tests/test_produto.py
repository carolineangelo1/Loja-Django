import pytest
from django.core.exceptions import ValidationError
from loja.models import Produto, Fornecedor, EspecificacaoProduto, Avaliacao

@pytest.fixture
def fornecedor():
  return Fornecedor.objects.create(
    nome="Test Supplier",
    telefone="123456789",
    email="testuser@example.com",
    endereco="Rua Teste, 123",
    cnpj="12345678901234"
  )

@pytest.fixture
def produto(fornecedor):
  return Produto.objects.create(
    nome="Test Product",
    descricao="Test Description",
    preco=10.0,
    estoque=10,
    fornecedor=fornecedor
  )

@pytest.fixture
def especificacao_produto(produto):
  return EspecificacaoProduto.objects.create(
    produto=produto,
    tamanho="M",
    cor="Azul"
  )

@pytest.mark.django_db
def test_produto_creation(fornecedor):
  produto = Produto.objects.create(
    nome="Test Product",
    descricao="Test Description",
    preco=10.0,
    estoque=10,
    fornecedor=fornecedor
  )

  produto.full_clean()
  produto.save()

  produto_from_db = Produto.objects.get(id=produto.id)

  assert produto.nome == produto_from_db.nome
  assert produto.descricao == produto_from_db.descricao
  assert produto.preco == produto_from_db.preco
  assert produto.estoque == produto_from_db.estoque
  assert produto.fornecedor == produto_from_db.fornecedor

@pytest.mark.django_db
def test_produto_update(fornecedor):
  produto = Produto.objects.create(
    nome="Test Product",
    descricao="Test Description",
    preco=10.0,
    estoque=10,
    fornecedor=fornecedor
  )

  produto.nome = "Updated Product"
  produto.save()

  updated_produto = Produto.objects.get(id=produto.id)

  assert updated_produto.nome == "Updated Product"

@pytest.mark.django_db
def test_produto_deletion(fornecedor):
  produto = Produto.objects.create(
    nome="Test Product",
    descricao="Test Description",
    preco=10.0,
    estoque=10,
    fornecedor=fornecedor
  )

  produto_id = produto.id
  produto.delete()
  with pytest.raises(Produto.DoesNotExist):
    Produto.objects.get(id=produto_id)

@pytest.mark.django_db
def test_produto_nome_vazio(fornecedor):
  with pytest.raises(ValidationError):
    produto = Produto(nome="", descricao="Test Description", preco=10.0, estoque=10, fornecedor=fornecedor)
    produto.full_clean()

@pytest.mark.django_db
def test_produto_descricao_vazia(fornecedor):
  with pytest.raises(ValidationError):
    produto = Produto(nome="Test Product", descricao="", preco=10.0, estoque=10, fornecedor=fornecedor)
    produto.full_clean()

@pytest.mark.django_db
def test_produto_preco_negativo(fornecedor):
  with pytest.raises(ValidationError):
    produto = Produto(nome="Test Product", descricao="Test Description", preco=-10.0, estoque=10, fornecedor=fornecedor)
    produto.full_clean()

@pytest.mark.django_db
def test_produto_estoque_negativo(fornecedor):
  with pytest.raises(ValidationError):
    produto = Produto(nome="Test Product", descricao="Test Description", preco=10.0, estoque=-10, fornecedor=fornecedor)
    produto.full_clean()

@pytest.mark.django_db
def test_produto_fornecedor_nulo():
  with pytest.raises(ValidationError):
    produto = Produto(nome="Test Product", descricao="Test Description", preco=10.0, estoque=10, fornecedor=None)
    produto.full_clean()

@pytest.mark.django_db
def test_produto_especificacao_cascata(produto, especificacao_produto):
  produto_id = produto.id
  especificacao_id = especificacao_produto.id

  produto.delete()

  with pytest.raises(EspecificacaoProduto.DoesNotExist):
    EspecificacaoProduto.objects.get(id=especificacao_id)

@pytest.mark.django_db
def test_produto_avaliacao_cascata(produto):
  produto_id = produto.id

  produto.delete()

  with pytest.raises(Avaliacao.DoesNotExist):
    Avaliacao.objects.get(produto_id=produto_id)
