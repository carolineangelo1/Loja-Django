import pytest
from django.core.exceptions import ValidationError
from loja.models import ItemPedido, Pedido, Produto, EspecificacaoProduto, Usuario, Fornecedor

@pytest.fixture
def usuario():
    return Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )

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
def pedido(usuario):
    return Pedido.objects.create(
        usuario=usuario,
        data_pedido="2024-12-18",
        valor_total=100.0,
        status="Pendente",
        endereco_entrega="Rua Teste, 123"
    )

@pytest.fixture
def especificacao_produto(produto):
    return EspecificacaoProduto.objects.create(
        produto=produto,
        tamanho="M",
        cor="Azul"
    )

@pytest.mark.django_db
def test_item_pedido_creation(pedido, produto, especificacao_produto):
    item_pedido = ItemPedido.objects.create(
        pedido=pedido,
        produto=produto,
        especificacao=especificacao_produto,
        quantidade=2,
        preco_unitario=10.0
    )

    item_pedido.full_clean()
    item_pedido.save()

    item_pedido_from_db = ItemPedido.objects.get(id=item_pedido.id)

    assert item_pedido.pedido == item_pedido_from_db.pedido
    assert item_pedido.produto == item_pedido_from_db.produto
    assert item_pedido.especificacao == item_pedido_from_db.especificacao
    assert item_pedido.quantidade == item_pedido_from_db.quantidade
    assert item_pedido.preco_unitario == item_pedido_from_db.preco_unitario

@pytest.mark.django_db
def test_item_pedido_update(pedido, produto, especificacao_produto):
    item_pedido = ItemPedido.objects.create(
        pedido=pedido,
        produto=produto,
        especificacao=especificacao_produto,
        quantidade=2,
        preco_unitario=10.0
    )

    item_pedido.quantidade = 3
    item_pedido.save()

    updated_item_pedido = ItemPedido.objects.get(id=item_pedido.id)

    assert updated_item_pedido.quantidade == 3

@pytest.mark.django_db
def test_item_pedido_deletion(pedido, produto, especificacao_produto):
    item_pedido = ItemPedido.objects.create(
        pedido=pedido,
        produto=produto,
        especificacao=especificacao_produto,
        quantidade=2,
        preco_unitario=10.0
    )

    item_pedido_id = item_pedido.id
    item_pedido.delete()
    with pytest.raises(ItemPedido.DoesNotExist):
        ItemPedido.objects.get(id=item_pedido_id)

@pytest.mark.django_db
def test_item_pedido_quantidade_negativa(pedido, produto, especificacao_produto):
    with pytest.raises(ValidationError):
        item_pedido = ItemPedido(
            pedido=pedido,
            produto=produto,
            especificacao=especificacao_produto,
            quantidade=-1,
            preco_unitario=10.0
        )
        item_pedido.full_clean()

@pytest.mark.django_db
def test_item_pedido_preco_unitario_negativo(pedido, produto, especificacao_produto):
    with pytest.raises(ValidationError):
        item_pedido = ItemPedido(
            pedido=pedido,
            produto=produto,
            especificacao=especificacao_produto,
            quantidade=2,
            preco_unitario=-10.0
        )
        item_pedido.full_clean()

@pytest.mark.django_db
def test_item_pedido_pedido_nulo(produto, especificacao_produto):
    with pytest.raises(ValidationError):
        item_pedido = ItemPedido(
            pedido=None,
            produto=produto,
            especificacao=especificacao_produto,
            quantidade=2,
            preco_unitario=10.0
        )
        item_pedido.full_clean()

@pytest.mark.django_db
def test_item_pedido_produto_nulo(pedido, especificacao_produto):
    with pytest.raises(ValidationError):
        item_pedido = ItemPedido(
            pedido=pedido,
            produto=None,
            especificacao=especificacao_produto,
            quantidade=2,
            preco_unitario=10.0
        )
        item_pedido.full_clean()

@pytest.mark.django_db
def test_item_pedido_especificacao_nula(pedido, produto):
    item_pedido = ItemPedido.objects.create(
        pedido=pedido,
        produto=produto,
        especificacao=None,
        quantidade=2,
        preco_unitario=10.0
    )

    item_pedido.full_clean()
    item_pedido.save()

    item_pedido_from_db = ItemPedido.objects.get(id=item_pedido.id)

    assert item_pedido.especificacao == item_pedido_from_db.especificacao
