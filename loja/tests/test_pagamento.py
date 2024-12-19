import django
import pytest
from django.core.exceptions import ValidationError
from loja.models import Pagamento, Pedido, Usuario

@pytest.fixture
def usuario():
    return Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )

@pytest.fixture
def pedido(usuario):
    return Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )

@pytest.mark.django_db
def test_pagamento_creation(pedido):
    pagamento = Pagamento.objects.create(
        pedido=pedido,
        forma_pagamento="Cartão de Crédito",
        data_pagamento="2024-12-19",
        valor_pagamento=100.0
    )

    pagamento.full_clean()
    pagamento.save()

    pagamento_from_db = Pagamento.objects.get(id=pagamento.id)

    assert pagamento.pedido == pagamento_from_db.pedido
    assert pagamento.forma_pagamento == pagamento_from_db.forma_pagamento
    assert pagamento.data_pagamento == pagamento_from_db.data_pagamento
    assert pagamento.valor_pagamento == pagamento_from_db.valor_pagamento

@pytest.mark.django_db
def test_pagamento_update(pedido):
    pagamento = Pagamento.objects.create(
        pedido=pedido,
        forma_pagamento="Cartão de Crédito",
        data_pagamento="2024-12-19",
        valor_pagamento=100.0
    )

    pagamento.forma_pagamento = "Boleto"
    pagamento.save()

    updated_pagamento = Pagamento.objects.get(id=pagamento.id)

    assert updated_pagamento.forma_pagamento == "Boleto"

@pytest.mark.django_db
def test_pagamento_deletion(pedido):
    pagamento = Pagamento.objects.create(
        pedido=pedido,
        forma_pagamento="Cartão de Crédito",
        data_pagamento="2024-12-19",
        valor_pagamento=100.0
    )

    pagamento_id = pagamento.id
    pagamento.delete()
    with pytest.raises(Pagamento.DoesNotExist):
        Pagamento.objects.get(id=pagamento_id)

@pytest.mark.django_db
def test_pagamento_valor_negativo(pedido):
    with pytest.raises(ValidationError):
        pagamento = Pagamento(
            pedido=pedido,
            forma_pagamento="Cartão de Crédito",
            data_pagamento="2024-12-19",
            valor_pagamento=-100.0
        )
        pagamento.full_clean()

@pytest.mark.django_db
def test_pagamento_data_vazia(pedido):
    with pytest.raises(ValidationError):
        pagamento = Pagamento(
            pedido=pedido,
            forma_pagamento="Cartão de Crédito",
            data_pagamento="",
            valor_pagamento=100.0
        )
        pagamento.full_clean()

@pytest.mark.django_db
def test_pagamento_forma_pagamento_vazia(pedido):
    with pytest.raises(ValidationError):
        pagamento = Pagamento(
            pedido=pedido,
            forma_pagamento="",
            data_pagamento="2024-12-19",
            valor_pagamento=100.0
        )
        pagamento.full_clean()

@pytest.mark.django_db
def test_pagamento_pedido_nulo():
    with pytest.raises(ValidationError):
        pagamento = Pagamento(
            pedido=None,
            forma_pagamento="Cartão de Crédito",
            data_pagamento="2024-12-19",
            valor_pagamento=100.0
        )
        pagamento.full_clean()

@pytest.mark.django_db
def test_pagamento_pedido_cascade(pedido):
  pagamento = Pagamento.objects.create(
    pedido=pedido,
    forma_pagamento="Cartão de Crédito",
    data_pagamento="2024-12-19",
    valor_pagamento=100.0
  )

  with pytest.raises(django.db.models.deletion.ProtectedError):
    pedido.delete()
