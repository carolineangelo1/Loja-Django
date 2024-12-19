import pytest
from django.core.exceptions import ValidationError
from loja.models import HistoricoPedido, Pedido, Usuario

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
def test_historico_pedido_creation(pedido):
    historico_pedido = HistoricoPedido.objects.create(
        pedido=pedido,
        data_alteracao="2024-12-19",
        status_anterior="Pendente",
        status_atual="Concluído"
    )

    historico_pedido.full_clean()
    historico_pedido.save()

    historico_pedido_from_db = HistoricoPedido.objects.get(id=historico_pedido.id)

    assert historico_pedido.pedido == historico_pedido_from_db.pedido
    assert historico_pedido.data_alteracao == historico_pedido_from_db.data_alteracao
    assert historico_pedido.status_anterior == historico_pedido_from_db.status_anterior
    assert historico_pedido.status_atual == historico_pedido_from_db.status_atual

@pytest.mark.django_db
def test_historico_pedido_update(pedido):
    historico_pedido = HistoricoPedido.objects.create(
        pedido=pedido,
        data_alteracao="2024-12-19",
        status_anterior="Pendente",
        status_atual="Concluído"
    )

    historico_pedido.status_atual = "Cancelado"
    historico_pedido.save()

    updated_historico_pedido = HistoricoPedido.objects.get(id=historico_pedido.id)

    assert updated_historico_pedido.status_atual == "Cancelado"

@pytest.mark.django_db
def test_historico_pedido_deletion(pedido):
    historico_pedido = HistoricoPedido.objects.create(
        pedido=pedido,
        data_alteracao="2024-12-19",
        status_anterior="Pendente",
        status_atual="Concluído"
    )

    historico_pedido_id = historico_pedido.id
    historico_pedido.delete()
    with pytest.raises(HistoricoPedido.DoesNotExist):
        HistoricoPedido.objects.get(id=historico_pedido_id)

@pytest.mark.django_db
def test_historico_pedido_data_alteracao_vazia(pedido):
    with pytest.raises(ValidationError):
        historico_pedido = HistoricoPedido(
            pedido=pedido,
            data_alteracao="",
            status_anterior="Pendente",
            status_atual="Concluído"
        )
        historico_pedido.full_clean()

@pytest.mark.django_db
def test_historico_pedido_pedido_nulo():
    with pytest.raises(ValidationError):
        historico_pedido = HistoricoPedido(
            pedido=None,
            data_alteracao="2024-12-19",
            status_anterior="Pendente",
            status_atual="Concluído"
        )
        historico_pedido.full_clean()
