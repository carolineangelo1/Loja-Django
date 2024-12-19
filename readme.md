# Loja Django

Este é um projeto Django para uma loja online. O projeto inclui modelos para usuários, fornecedores, produtos, pedidos, itens de pedido, pagamentos, avaliações, histórico de pedidos e serviços de fretagem.

## Requisitos

- Python 3.8+
- Django 5.1.4
- pytest
- pytest-django
- MySQL (ou outro banco de dados configurado)

## Instalação

1. Clone o repositório:

```sh
git clone https://github.com/mestresol/loja-django.git
cd loja-django
```

2. Crie e ative um ambiente virtual:

```sh
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

4. Configure o banco de dados no arquivo settings.py:

```json
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'root',
        'PASSWORD': 'Root',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_nome_do_banco',
            'MIRROR': 'default',
        },
    }
}
```

5. Execute as migrações do banco de dados:

```sh
python manage.py migrate
```
## Executando os Testes

1. Instale as dependências de teste:

```sh
pip install pytest pytest-django
```

2. Execute os testes:
```sh
pytest
```
