import django
import pytest
from django.core.exceptions import ValidationError
from loja.models import Pedido, Usuario

@pytest.fixture
def usuario():
    return Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )

@pytest.mark.django_db
def test_pedido_creation(usuario):
    pedido = Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )

    pedido.full_clean()
    pedido.save()

    pedido_from_db = Pedido.objects.get(id=pedido.id)

    assert pedido.usuario == pedido_from_db.usuario
    assert pedido.data_pedido == pedido_from_db.data_pedido
    assert pedido.valor_total == pedido_from_db.valor_total
    assert pedido.status == pedido_from_db.status
    assert pedido.endereco_entrega == pedido_from_db.endereco_entrega

@pytest.mark.django_db
def test_pedido_update(usuario):
    pedido = Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )

    pedido.status = "Concluído"
    pedido.save()

    updated_pedido = Pedido.objects.get(id=pedido.id)

    assert updated_pedido.status == "Concluído"

@pytest.mark.django_db
def test_pedido_deletion(usuario):
    pedido = Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )

    pedido_id = pedido.id
    pedido.delete()
    with pytest.raises(Pedido.DoesNotExist):
        Pedido.objects.get(id=pedido_id)

@pytest.mark.django_db
def test_pedido_valor_total_negativo(usuario):
    with pytest.raises(ValidationError):
        pedido = Pedido(
            usuario=usuario,
            data_pedido="2024-12-18",
            valor_total=-100.0,
            status="Pendente",
            endereco_entrega="Rua Teste, 123"
        )
        pedido.full_clean()

@pytest.mark.django_db
def test_pedido_endereco_entrega_vazio(usuario):
    with pytest.raises(ValidationError):
        pedido = Pedido(
            usuario=usuario,
            data_pedido="2024-12-18",
            valor_total=100.0,
            status="Pendente",
            endereco_entrega=""
        )
        pedido.full_clean()

@pytest.mark.django_db
def test_pedido_usuario_nulo():
    with pytest.raises(ValidationError):
        pedido = Pedido(
            usuario=None,
            data_pedido="2024-12-18",
            valor_total=100.0,
            status="Pendente",
            endereco_entrega="Rua Teste, 123"
        )
        pedido.full_clean()

@pytest.mark.django_db
def test_pedido_data_pedido_vazia(usuario):
    with pytest.raises(ValidationError):
        pedido = Pedido(
            usuario=usuario,
            data_pedido="",
            valor_total=100.0,
            status="Pendente",
            endereco_entrega="Rua Teste, 123"
        )
        pedido.full_clean()

@pytest.mark.django_db
def test_pedido_status_vazio(usuario):
    with pytest.raises(ValidationError):
        pedido = Pedido(
            usuario=usuario,
            data_pedido="2024-12-18",
            valor_total=100.0,
            status="",
            endereco_entrega="Rua Teste, 123"
        )
        pedido.full_clean()

@pytest.mark.django_db
def test_pedido_usuario_cascade(usuario):
    pedido = Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )
    with pytest.raises(django.db.models.deletion.ProtectedError):
        usuario.delete()



