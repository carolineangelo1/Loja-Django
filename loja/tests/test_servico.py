import django
import pytest
from django.core.exceptions import ValidationError
from loja.models import ServicoFretagem, Pedido, Usuario

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
def test_servico_fretagem_creation(pedido):
    servico_fretagem = ServicoFretagem.objects.create(
        nome_transportadora="Transportadora Teste",
        preco_fretagem=50.0,
        tipo_servico="Expresso",
        pedido=pedido,
        prazo_entrega=5
    )

    servico_fretagem.full_clean()
    servico_fretagem.save()

    servico_fretagem_from_db = ServicoFretagem.objects.get(id=servico_fretagem.id)

    assert servico_fretagem.nome_transportadora == servico_fretagem_from_db.nome_transportadora
    assert servico_fretagem.preco_fretagem == servico_fretagem_from_db.preco_fretagem
    assert servico_fretagem.tipo_servico == servico_fretagem_from_db.tipo_servico
    assert servico_fretagem.pedido == servico_fretagem_from_db.pedido
    assert servico_fretagem.prazo_entrega == servico_fretagem_from_db.prazo_entrega

@pytest.mark.django_db
def test_servico_fretagem_update(pedido):
    servico_fretagem = ServicoFretagem.objects.create(
        nome_transportadora="Transportadora Teste",
        preco_fretagem=50.0,
        tipo_servico="Expresso",
        pedido=pedido,
        prazo_entrega=5
    )

    servico_fretagem.tipo_servico = "Normal"
    servico_fretagem.save()

    updated_servico_fretagem = ServicoFretagem.objects.get(id=servico_fretagem.id)

    assert updated_servico_fretagem.tipo_servico == "Normal"

@pytest.mark.django_db
def test_servico_fretagem_deletion(pedido):
    servico_fretagem = ServicoFretagem.objects.create(
        nome_transportadora="Transportadora Teste",
        preco_fretagem=50.0,
        tipo_servico="Expresso",
        pedido=pedido,
        prazo_entrega=5
    )

    servico_fretagem_id = servico_fretagem.id
    servico_fretagem.delete()
    with pytest.raises(ServicoFretagem.DoesNotExist):
        ServicoFretagem.objects.get(id=servico_fretagem_id)

@pytest.mark.django_db
def test_servico_fretagem_preco_negativo(pedido):
    with pytest.raises(ValidationError):
        servico_fretagem = ServicoFretagem(
            nome_transportadora="Transportadora Teste",
            preco_fretagem=-50.0,
            tipo_servico="Expresso",
            pedido=pedido,
            prazo_entrega=5
        )
        servico_fretagem.full_clean()

@pytest.mark.django_db
def test_servico_fretagem_prazo_entrega_negativo(pedido):
    with pytest.raises(ValidationError):
        servico_fretagem = ServicoFretagem(
            nome_transportadora="Transportadora Teste",
            preco_fretagem=50.0,
            tipo_servico="Expresso",
            pedido=pedido,
            prazo_entrega=-5
        )
        servico_fretagem.full_clean()

@pytest.mark.django_db
def test_servico_fretagem_nome_transportadora_vazio(pedido):
    with pytest.raises(ValidationError):
        servico_fretagem = ServicoFretagem(
            nome_transportadora="",
            preco_fretagem=50.0,
            tipo_servico="Expresso",
            pedido=pedido,
            prazo_entrega=5
        )
        servico_fretagem.full_clean()

@pytest.mark.django_db
def test_servico_fretagem_tipo_servico_vazio(pedido):
    with pytest.raises(ValidationError):
        servico_fretagem = ServicoFretagem(
            nome_transportadora="Transportadora Teste",
            preco_fretagem=50.0,
            tipo_servico="",
            pedido=pedido,
            prazo_entrega=5
        )
        servico_fretagem.full_clean()

@pytest.mark.django_db
def test_servico_fretagem_pedido_nulo():
    with pytest.raises(ValidationError):
        servico_fretagem = ServicoFretagem(
            nome_transportadora="Transportadora Teste",
            preco_fretagem=50.0,
            tipo_servico="Expresso",
            pedido=None,
            prazo_entrega=5
        )
        servico_fretagem.full_clean()

@pytest.mark.django_db
def test_servico_fretagem_pedido_cascade(pedido):
    servico_fretagem = ServicoFretagem.objects.create(
        nome_transportadora="Transportadora Teste",
        preco_fretagem=50.0,
        tipo_servico="Expresso",
        pedido=pedido,
        prazo_entrega=5
    )
    with pytest.raises(django.db.models.deletion.ProtectedError):
      pedido.delete()
