# Sistema-de-banco-3.0
Sistema de banco otimizado utilizando o paradigma da Orientação a Objetos.

Base que o programa deve seguir:

| Classe / Interface               | Atributos                                                                                 | Métodos                                                                      | Observações                                    |
| -------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------- |
| **Transacao (interface)**        | -                                                                                         | `registrar(conta: Conta)`                                                    | Interface que Saque e Depósito vão implementar |
| **Deposito**                     | `valor: float`                                                                            | `registrar(conta: Conta)`                                                    | Implementa Transacao                           |
| **Saque**                        | `valor: float`                                                                            | `registrar(conta: Conta)`                                                    | Implementa Transacao                           |
| **Historico**                    | `transacoes: list`                                                                        | `adicionar_transacao(transacao: Transacao)`                                  | Guarda todas as transações de uma conta        |
| **Conta**                        | `saldo: float`, `numero: int`, `agencia: str`, `cliente: Cliente`, `historico: Historico` | `saldo()`, `nova_conta(cliente, numero)`, `sacar(valor)`, `depositar(valor)` | Classe genérica de conta                       |
| **ContaCorrente (herda Conta)**  | `limite: float`, `limite_saques: int`                                                     | Usa os mesmos da Conta                                                       | Conta especializada                            |
| **Cliente**                      | `endereco: str`, `contas: list`                                                           | `realizar_transacao(conta, transacao)`, `adicionar_conta(conta)`             | Classe genérica de cliente                     |
| **PessoaFisica (herda Cliente)** | `cpf: str`, `nome: str`, `data_nascimento: date`                                          | -                                                                            | Cliente pessoa física                          |

*OBS: desenvolvido utilizando a linguagem Python (versão 3.13.2) e na IDE VSCODE;
