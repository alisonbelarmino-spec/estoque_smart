from datetime import datetime

ESTOQUE_BAIXO = 5

produtos = {
    "P001": {"nome": "Hambúrguer artesanal", "preco": 25.0, "estoque": 20},
    "P002": {"nome": "Refrigerante", "preco": 6.0, "estoque": 15},
    "P003": {"nome": "Batata frita", "preco": 12.0, "estoque": 10},
}
historico = []


def cadastrar_produto(codigo, nome, preco, estoque):
    if codigo in produtos:
        raise ValueError("Código já cadastrado.")
    if not nome.strip():
        raise ValueError("Nome vazio.")
    if preco < 0 or estoque < 0:
        raise ValueError("Preço e quantidade não podem ser negativos.")
    produtos[codigo] = {"nome": nome, "preco": preco, "estoque": estoque}


def listar_produtos():
    for codigo, p in produtos.items():
        aviso = "  <- ESTOQUE BAIXO" if p["estoque"] <= ESTOQUE_BAIXO else ""
        print(f"{codigo} | {p['nome']} | R$ {p['preco']:.2f} | {p['estoque']} un.{aviso}")


def registrar_venda(itens):
    """itens: dicionário {codigo: quantidade}"""
    if not itens:
        raise ValueError("A venda precisa ter pelo menos um item.")

    # 1) valida tudo antes de mexer no estoque
    for codigo, qtd in itens.items():
        if codigo not in produtos:
            raise ValueError(f"Produto {codigo} não existe.")
        if qtd <= 0:
            raise ValueError(f"Quantidade inválida para {codigo}.")
        if qtd > produtos[codigo]["estoque"]:
            disp = produtos[codigo]["estoque"]
            raise ValueError(f"Estoque insuficiente para {codigo} (disponível: {disp}).")

    # 2) tudo certo: dá baixa e calcula o total
    total = 0
    lista = []
    for codigo, qtd in itens.items():
        p = produtos[codigo]
        p["estoque"] -= qtd
        subtotal = p["preco"] * qtd
        total += subtotal
        lista.append({"codigo": codigo, "nome": p["nome"], "qtd": qtd, "subtotal": subtotal})

    venda = {
        "id": len(historico) + 1,
        "itens": lista,
        "total": total,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    historico.append(venda)
    return venda


def mostrar_venda(venda):
    print(f"\nVenda #{venda['id']} - {venda['data']}")
    for i in venda["itens"]:
        print(f"  {i['qtd']} x {i['nome']}: R$ {i['subtotal']:.2f}")
    print(f"  Total: R$ {venda['total']:.2f}")


def listar_historico():
    if not historico:
        print("Nenhuma venda registrada.")
    for venda in historico:
        mostrar_venda(venda)


def menu_cadastro():
    codigo = input("Código: ").strip().upper()
    nome = input("Nome: ")
    preco = float(input("Preço: ").replace(",", "."))
    estoque = int(input("Quantidade em estoque: "))
    cadastrar_produto(codigo, nome, preco, estoque)
    print("Produto cadastrado!")


def menu_venda():
    itens = {}
    while True:
        codigo = input("Código do produto (Enter para finalizar): ").strip().upper()
        if codigo == "":
            break
        qtd = int(input("Quantidade: "))
        itens[codigo] = itens.get(codigo, 0) + qtd
    venda = registrar_venda(itens)
    print("Venda realizada!")
    mostrar_venda(venda)


while True:
    print("\n1-Cadastrar  2-Estoque  3-Vender  4-Histórico  0-Sair")
    opcao = input("Opção: ")
    if opcao == "0":
        break
    try:
        if opcao == "1":
            menu_cadastro()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            menu_venda()
        elif opcao == "4":
            listar_historico()
        else:
            print("Opção inválida.")
    except ValueError as erro:
        print("Erro:", erro)