from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

class Transacao(ABC):
    """Interface para qualquer transação (Depósito / Saque)."""

    def __init__(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        self.valor = float(valor)
        self.carimbada_em = datetime.now()

    @property
    @abstractmethod
    def tipo(self) -> str:
        ...

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        """
        Aplica o efeito na conta (sacar/depositar) e retorna True se deu certo.
        O histórico é atualizado fora, por quem chamou.
        """
        ...

class Deposito(Transacao):
    @property
    def tipo(self) -> str:
        return "DEPÓSITO"

    def registrar(self, conta: "Conta") -> bool:
        return conta.depositar(self.valor)


class Saque(Transacao):
    @property
    def tipo(self) -> str:
        return "SAQUE"

    def registrar(self, conta: "Conta") -> bool:
        return conta.sacar(self.valor)

@dataclass
class RegistroTransacao:
    tipo: str
    valor: float
    data_hora: datetime
    saldo_resultante: float

    def __str__(self) -> str:
        ts = self.data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return f"[{ts}] {self.tipo}: R$ {self.valor:.2f} | saldo: R$ {self.saldo_resultante:.2f}"


class Historico:
    """Composição: 1 Histórico por Conta; guarda N registros."""

    def __init__(self) -> None:
        self.transacoes: List[RegistroTransacao] = []

    def adicionar_transacao(self, transacao: Transacao, saldo_resultante: float) -> None:
        self.transacoes.append(
            RegistroTransacao(
                tipo=transacao.tipo,
                valor=transacao.valor,
                data_hora=transacao.carimbada_em,
                saldo_resultante=saldo_resultante,
            )
        )

    def __iter__(self):
        return iter(self.transacoes)

    def total_saques(self) -> int:
        return sum(1 for t in self.transacoes if t.tipo == "SAQUE")

class Cliente:
    """Cliente genérico. Possui 0..N contas e pode realizar transações."""

    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas: List["Conta"] = []

    def adicionar_conta(self, conta: "Conta") -> None:
        # evita duplicidade por número+agência
        if any(c.numero == conta.numero and c.agencia == conta.agencia for c in self.contas):
            raise ValueError("Este cliente já possui uma conta com o mesmo número e agência.")
        self.contas.append(conta)

    def realizar_transacao(self, conta: "Conta", transacao: Transacao) -> bool:
        if conta not in self.contas:
            raise ValueError("A conta informada não pertence a este cliente.")
        sucesso = transacao.registrar(conta)
        if sucesso:
            conta.historico.adicionar_transacao(transacao, saldo_resultante=conta._saldo)
        return sucesso


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str) -> None:
        super().__init__(endereco=endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __repr__(self) -> str:
        return f"PessoaFisica(nome={self.nome!r}, cpf={self.cpf!r})"

class Conta:
    """Conta genérica."""

    def __init__(self, cliente: Cliente, numero: int, agencia: str = "0001") -> None:
        self._saldo: float = 0.0
        self.numero = int(numero)
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self._saldo += valor
        return True

    def sacar(self, valor: float) -> bool:
        """Regra padrão: não permite saldo negativo."""
        if valor <= 0:
            return False
        if valor > self._saldo:
            return False
        self._saldo -= valor
        return True

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int, **kwargs) -> "Conta":
        """
        Cria uma nova conta. Se chamado a partir de uma subclasse, retorna a subclasse.
        Ex.: ContaCorrente.nova_conta(cliente, 1, limite=500, limite_saques=3)
        """
        conta = cls(cliente=cliente, numero=numero, **kwargs)
        cliente.adicionar_conta(conta)
        return conta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ag={self.agencia}, num={self.numero}, saldo={self._saldo:.2f})"


class ContaCorrente(Conta):
    """Especialização de Conta, com limite e limite de saques."""

    def __init__(self, cliente: Cliente, numero: int, agencia: str = "0001",
                 limite: float = 0.0, limite_saques: int = 3) -> None:
        super().__init__(cliente=cliente, numero=numero, agencia=agencia)
        self.limite = float(limite)
        self.limite_saques = int(limite_saques)

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            return False

        saques_efetuados = self.historico.total_saques()
        if saques_efetuados >= self.limite_saques:
            return False

        disponivel = self._saldo + self.limite
        if valor > disponivel:
            return False

        self._saldo -= valor
        return True