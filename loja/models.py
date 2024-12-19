from django.db import models
from django.core.exceptions import ValidationError

class Usuario(models.Model):
  nome = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  senha = models.CharField(max_length=255)

  def clean(self):
    if len(self.senha) < 8:
      raise ValidationError("Senha deve ter pelo menos 8 caracteres.")

  def __str__(self):
    return self.nome


class Fornecedor(models.Model):
  nome = models.CharField(max_length=100)
  telefone = models.CharField(max_length=15)
  email = models.EmailField()
  endereco = models.CharField(max_length=255)
  cnpj = models.CharField(max_length=14)

  def clean(self):
    if len(self.cnpj) != 14:
      raise ValidationError("CNPJ deve ter exatamente 14 dígitos.")

  def __str__(self):
    return self.nome


class Produto(models.Model):
  nome = models.CharField(max_length=100)
  descricao = models.TextField()
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  estoque = models.IntegerField()
  fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

  def clean(self):
    if self.preco < 0:
      raise ValidationError("Preço não pode ser negativo.")
    if self.estoque < 0:
      raise ValidationError("Estoque não pode ser negativo.")

  def __str__(self):
    return self.nome


class EspecificacaoProduto(models.Model):
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
  tamanho = models.CharField(max_length=10)
  cor = models.CharField(max_length=50)
  personalizacao = models.CharField(max_length=255, blank=True, null=True)
  preco_adicional = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

  def __str__(self):
    return f"{self.produto.nome} - {self.tamanho}/{self.cor}"


class Pedido(models.Model):
  usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
  data_pedido = models.DateField()
  valor_total = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.CharField(max_length=50)
  endereco_entrega = models.CharField(max_length=255)

  def clean(self):
    if self.valor_total < 0:
      raise ValidationError("Valor total não pode ser negativo.")

  def __str__(self):
    return f"Pedido {self.id} - {self.status}"


class ItemPedido(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
  produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
  especificacao = models.ForeignKey(EspecificacaoProduto, on_delete=models.PROTECT, blank=True, null=True)
  quantidade = models.IntegerField()
  preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

  def clean(self):
    if self.quantidade < 0:
      raise ValidationError("Quantidade não pode ser negativa.")
    if self.preco_unitario < 0:
      raise ValidationError("Preço unitário não pode ser negativo.")

  def __str__(self):
    return f"Item {self.id} - Pedido {self.pedido.id}"


class Pagamento(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
  forma_pagamento = models.CharField(max_length=50)
  data_pagamento = models.DateField()
  valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2)

  def clean(self):
    if self.valor_pagamento < 0:
      raise ValidationError("Valor do pagamento não pode ser negativo.")

  def __str__(self):
    return f"Pagamento {self.id} - Pedido {self.pedido.id}"


class Avaliacao(models.Model):
  produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  nota = models.IntegerField(null=False)
  comentario = models.TextField(blank=True, null=True)

  def clean(self):
    if not (0 <= self.nota <= 5):
      raise ValidationError("A nota deve estar entre 0 e 5.")

  def __str__(self):
    return f"Avaliação {self.id} - {self.produto.nome}"


class HistoricoPedido(models.Model):
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
  data_alteracao = models.DateField(null=False, blank=False)
  status_anterior = models.CharField(max_length=50)
  status_atual = models.CharField(max_length=50)

  def __str__(self):
    return f"Histórico {self.id} - Pedido {self.pedido.id}"


class ServicoFretagem(models.Model):
  nome_transportadora = models.CharField(max_length=100)
  preco_fretagem = models.DecimalField(max_digits=10, decimal_places=2)
  tipo_servico = models.CharField(max_length=50)
  pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
  prazo_entrega = models.IntegerField()

  def clean(self):
    if self.preco_fretagem < 0:
      raise ValidationError("Preço da fretagem não pode ser negativo.")
    if self.prazo_entrega < 0:
      raise ValidationError("Prazo de entrega não pode ser negativo.")

  def __str__(self):
    return self.nome_transportadora
