import django
import pytest
from django.core.exceptions import ValidationError
from loja.models import Fornecedor, Produto, Avaliacao

# Teste para criação de um fornecedor
@pytest.mark.django_db
def test_fornecedor_creation():
    fornecedor = Fornecedor.objects.create(
        nome="Test Supplier",
        telefone="123456789",
        email="testuser@example.com",
        endereco="Rua Teste, 123",
        cnpj="12345678901234"
    )

    fornecedor.full_clean()
    fornecedor.save()

    fornecedor_from_db = Fornecedor.objects.get(id=fornecedor.id)

    assert fornecedor.nome == fornecedor_from_db.nome
    assert fornecedor.telefone == fornecedor_from_db.telefone
    assert fornecedor.email == fornecedor_from_db.email
    assert fornecedor.endereco == fornecedor_from_db.endereco
    assert fornecedor.cnpj == fornecedor_from_db.cnpj

# Teste para atualização de um fornecedor
@pytest.mark.django_db
def test_fornecedor_update():
    fornecedor = Fornecedor.objects.create(
        nome="Test Supplier",
        telefone="123456789",
        email="testuser@example.com",
        endereco="Rua Teste, 123",
        cnpj="12345678901234"
    )
    fornecedor.nome = "Updated Supplier"
    fornecedor.save()
    updated_fornecedor = Fornecedor.objects.get(id=fornecedor.id)
    assert updated_fornecedor.nome == "Updated Supplier"

# Teste para exclusão de um fornecedor
@pytest.mark.django_db
def test_fornecedor_deletion():
    fornecedor = Fornecedor.objects.create(
        nome="Test Supplier",
        telefone="123456789",
        email="testuser@example.com",
        endereco="Rua Teste, 123",
        cnpj="12345678901234"
    )

    fornecedor_id = fornecedor.id
    fornecedor.delete()
    with pytest.raises(Fornecedor.DoesNotExist):
        Fornecedor.objects.get(id=fornecedor_id)


# Teste para validar nome vazio
@pytest.mark.django_db
def test_fornecedor_nome_vazio():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor.objects.create(
            nome="",
            telefone="123456789",
            email="testuser@example.com",
            endereco="Rua Teste, 123",
            cnpj="12345678901234"
        )
        fornecedor.full_clean()

# Teste para telefone vazio
@pytest.mark.django_db
def test_fornecedor_telefone_vazio():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="", email="testuser@example.com", endereco="Rua Teste, 123", cnpj="12345678901234")
        fornecedor.full_clean()

# Teste para email vazio
@pytest.mark.django_db
def test_fornecedor_email_vazio():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="123456789", email="", endereco="Rua Teste, 123", cnpj="12345678901234")
        fornecedor.full_clean()

# Teste para email inválido
@pytest.mark.django_db
def test_fornecedor_email_invalido():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="123456789", email="invalid-email", endereco="Rua Teste, 123", cnpj="12345678901234")
        fornecedor.full_clean()

# Teste para endereço vazio
@pytest.mark.django_db
def test_fornecedor_endereco_vazio():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="123456789", email="testuser@example.com", endereco="", cnpj="12345678901234")
        fornecedor.full_clean()

# Teste para CNPJ vazio
@pytest.mark.django_db
def test_fornecedor_cnpj_vazio():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="123456789", email="testuser@example.com", endereco="Rua Teste, 123", cnpj="")
        fornecedor.full_clean()

# Teste para CNPJ inválido
@pytest.mark.django_db
def test_fornecedor_cnpj_invalido():
    with pytest.raises(ValidationError):
        fornecedor = Fornecedor(nome="Test Supplier", telefone="123456789", email="testuser@example.com", endereco="Rua Teste, 123", cnpj="123")
        fornecedor.full_clean()


@pytest.mark.django_db
def test_fornecedor_produto_cascade():
    fornecedor = Fornecedor.objects.create(
        nome="Test Supplier",
        telefone="123456789",
        email="testuser@example.com",
        endereco = "Rua Teste, 123",
        cnpj="12345678901234"
    )

    produto = Produto.objects.create(
        nome="Test Product",
        descricao="Test Description",
        preco=10.0,
        estoque=10,
        fornecedor=fornecedor
    )

    fornecedor.delete()
    with pytest.raises(Produto.DoesNotExist):
        Produto.objects.get(id=produto.id)
