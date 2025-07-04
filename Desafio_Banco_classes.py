from abc import ABC, abstractclassmethod, abstractproperty



class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if valor > saldo:
            print("Você não tem saldo suficiente!❌")


        elif valor > 0:
            self._saldo -= valor
            print("Saque Realizado com Sucesso ✅")
            return True

        else:
            print("O valor informado é inválido ❌")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print()
            print("Deposito Realizado com Sucesso ✅")
        else:
            print("Valor inválido ❌")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self._limite:
             print(" O valor do saque excede o limite ❌")

        elif numero_saques >= self._limite_saques:
            print(" Número máximo de saques excedido ❌")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Titular:\t{self.cliente.nome}
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
           
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():


    menu = """
    ********** Menu **********
    [1]-----------Novo usuário
    [2]-------------Nova conta
    [3]------------- Depositar
    [4]----------------- Sacar
    [5]--------------- Extrato
    [6]----------Listar contas
    [7]------Cartão de Credito
    [0]------------------ Sair

    **************************
    Escolha: """
    return input((menu))

def consultar_usuario(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n O Cliente não possui conta ❌")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = consultar_usuario(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado❌")
        return

    valor = float(input("Informe o valor do depósito R$: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = consultar_usuario(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado ❌")
        return

    valor = float(input("Informe o valor do saque R$: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = consultar_usuario(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado ❌")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def novo_usuario(clientes):
    cpf = input("Informe o CPF, Ex:12345678900:\n")
    cliente = consultar_usuario(cpf, clientes)

    if cliente:
        print("Usuário já Cadastrado!")
        return

    nome = input("Informe o nome completo:\n")
    data_nascimento = input("Informe a data de nascimento Ex: dd-mm-aaaa:\n")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado):\n")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    
    print("----Dados Cadastrados---------")
    print(f"Nome:{nome} \n Data de Nascimento:{data_nascimento} \n Endereço:{endereco}")
    print()
    print("Usuário criado com sucesso!✅")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = consultar_usuario(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado❌")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso ✅")

def cartao_credito():
 cartao_credito = 2000
 print("---Cartão de credito-----")
 print()
 print(f"Valor disponivel para compras no Credito R$: {cartao_credito:.2f}")
 compra = float(input("Informe o valor da Compra R$: "))
 cartao_credito -= compra
 
 if compra > cartao_credito:
      print("Saldo Insuficiente❌")
 else:
       print("Compra Realizada Com sucesso✅")
       print()
       print(f"Valor disponivel para compras no Credito: {cartao_credito:.2f}")
 
def listar_contas(contas):
    print("------Lista de Contas")
    for conta in contas:
        print("-----------------------")
        print(conta)

clientes = []
contas = []
numero_conta = 0

while True:

    opcao = menu()
    
    if opcao == "1":
           novo_usuario(clientes)
    
    elif opcao == "2":
        numero_conta += 1 
        criar_conta(numero_conta, clientes, contas) 

    elif opcao == "3":
        depositar(clientes)

    elif opcao == "4":
       sacar(clientes)
        
    elif opcao == "5":
       exibir_extrato(clientes)
    
    elif opcao == "6":
       listar_contas(contas)
    
    elif opcao == "7":
        cartao_credito()
       
    elif opcao == "0":

       break
    
    else:
        print("Por favor selecione novamente a operação desejada.")
