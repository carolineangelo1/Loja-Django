import pytest
from django.core.exceptions import ValidationError
from loja.models import EspecificacaoProduto, Produto, Fornecedor

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
def test_especificacao_produto_creation(especificacao_produto):
  especificacao_produto.full_clean()
  especificacao_produto.save()

  especificacao_produto_from_db = EspecificacaoProduto.objects.get(id=especificacao_produto.id)

  assert especificacao_produto.produto == especificacao_produto_from_db.produto
  assert especificacao_produto.tamanho == especificacao_produto_from_db.tamanho
  assert especificacao_produto.cor == especificacao_produto_from_db.cor
  assert especificacao_produto.personalizacao == especificacao_produto_from_db.personalizacao
  assert especificacao_produto.preco_adicional == especificacao_produto_from_db.preco_adicional

@pytest.mark.django_db
def test_especificacao_produto_update(especificacao_produto):
  especificacao_produto.tamanho = "G"
  especificacao_produto.save()

  updated_especificacao_produto = EspecificacaoProduto.objects.get(id=especificacao_produto.id)

  assert updated_especificacao_produto.tamanho == "G"

@pytest.mark.django_db
def test_especificacao_produto_deletion(especificacao_produto):
  especificacao_produto_id = especificacao_produto.id
  especificacao_produto.delete()

  with pytest.raises(EspecificacaoProduto.DoesNotExist):
    EspecificacaoProduto.objects.get(id=especificacao_produto_id)

@pytest.mark.django_db
def test_especificacao_produto_tamanho_vazio(produto):
  with pytest.raises(ValidationError):
    especificacao_produto = EspecificacaoProduto(produto=produto, tamanho="", cor="Azul")
    especificacao_produto.full_clean()

@pytest.mark.django_db
def test_especificacao_produto_tamanho_grande(produto):
  with pytest.raises(ValidationError):
    especificacao_produto = EspecificacaoProduto(produto=produto, tamanho="Tamanho muito grande", cor="Azul")
    especificacao_produto.full_clean()

@pytest.mark.django_db
def test_especificacao_produto_cor_vazia(produto):
  with pytest.raises(ValidationError):
    especificacao_produto = EspecificacaoProduto(produto=produto, tamanho="M", cor="")
    especificacao_produto.full_clean()

@pytest.mark.django_db
def test_especificacao_produto_cor_grande(produto):
  with pytest.raises(ValidationError):
    especificacao_produto = EspecificacaoProduto(produto=produto, tamanho="M", cor="Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande Cor muito grande")
    especificacao_produto.full_clean()
