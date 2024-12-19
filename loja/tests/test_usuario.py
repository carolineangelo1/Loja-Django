import pytest
from django.core.exceptions import ValidationError
from loja.models import Usuario

# Teste para criação de um usuário
@pytest.mark.django_db
def test_usuario_creation():
    usuario = Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )

    usuario.full_clean()
    usuario.save()

    usuario_from_db = Usuario.objects.get(id=usuario.id)

    assert usuario.nome == usuario_from_db.nome
    assert usuario.email == usuario_from_db.email
    assert usuario.senha == usuario_from_db.senha

# Teste para atualização de um usuário
@pytest.mark.django_db
def test_usuario_update():
    usuario = Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )
    usuario.nome = "Updated User"

    usuario.save()

    updated_usuario = Usuario.objects.get(id=usuario.id)

    assert updated_usuario.nome == "Updated User"

# Teste para exclusão de um usuário
@pytest.mark.django_db
def test_usuario_deletion():
    usuario = Usuario.objects.create(
        nome="Test User",
        email="testuser@example.com",
        senha="password123"
    )
    usuario_id = usuario.id
    usuario.delete()
    with pytest.raises(Usuario.DoesNotExist):
        Usuario.objects.get(id=usuario_id)

# Teste para validar nome vazio
@pytest.mark.django_db
def test_usuario_nome_vazio():
    with pytest.raises(ValidationError):
        usuario = Usuario(nome="", email="testuser@example.com", senha="password123")
        usuario.full_clean()

# Teste para validar email inválido
@pytest.mark.django_db
def test_usuario_email_invalido():
    with pytest.raises(ValidationError):
        usuario = Usuario(nome="Test User", email="invalid-email", senha="password123")
        usuario.full_clean()

# Teste para validar senha curta
@pytest.mark.django_db
def test_usuario_senha_curta():
    with pytest.raises(ValidationError):
        usuario = Usuario(nome="Test User", email="testuser@example.com", senha="short")
        usuario.full_clean()

# Teste para validar email único
@pytest.mark.django_db
def test_usuario_email_unico():
    Usuario.objects.create(nome="Test User", email="testuser@example.com", senha="password123")
    with pytest.raises(ValidationError):
        usuario = Usuario(nome="Another User", email="testuser@example.com", senha="password123")
        usuario.full_clean()
