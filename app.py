from datetime import date
from main import PessoaFisica, ContaCorrente, Deposito, Saque

clientes = []

def buscar_cliente_por_cpf(cpf: str):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def menu():
    while True:
        print("\n==== BANCO ====")
        print("1 - Criar cliente")
        print("2 - Criar conta")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Extrato")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            depositar()
        elif opcao == "4":
            sacar()
        elif opcao == "5":
            extrato()
        elif opcao == "0":
            print("Saindo... até logo!")
            break
        else:
            print("Opção inválida!")

def criar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento = input("Data de nascimento (YYYY-MM-DD): ")
    endereco = input("Endereço: ")

    data_nasc = date.fromisoformat(nascimento)
    cliente = PessoaFisica(nome, cpf, data_nasc, endereco)
    clientes.append(cliente)

    print(f"Cliente {nome} criado com sucesso!")

def criar_conta():
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    numero = len(cliente.contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero, agencia="0001", limite=500, limite_saques=3)

    print(f"Conta {conta.numero} criada para {cliente.nome}.")

def depositar():
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    if not cliente.contas:
        print("Este cliente não possui contas.")
        return

    conta = cliente.contas[0]
    valor = float(input("Valor do depósito: "))
    deposito = Deposito(valor)

    cliente.realizar_transacao(conta, deposito)
    print("Depósito realizado com sucesso!")

def sacar():
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    if not cliente.contas:
        print("Este cliente não possui contas.")
        return

    conta = cliente.contas[0]
    valor = float(input("Valor do saque: "))
    saque = Saque(valor)

    sucesso = cliente.realizar_transacao(conta, saque)
    if sucesso:
        print("Saque realizado com sucesso!")
    else:
        print("Saque não permitido (saldo insuficiente ou limite atingido).")

def extrato():
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    if not cliente.contas:
        print("Este cliente não possui contas.")
        return

    conta = cliente.contas[0]
    print(f"\n=== Extrato da conta {conta.numero} ===")
    for reg in conta.historico:
        print(" -", reg)
    print(f"Saldo atual: R$ {conta.saldo():.2f}")


if __name__ == "__main__":
    menu()
