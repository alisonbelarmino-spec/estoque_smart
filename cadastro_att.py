# Instalar antes, no terminal: pip install bcrypt validate-docbr
import re
import bcrypt
from validate_docbr import CPF, CNPJ

clientes = [{"nome": "Maria", "email": "maria@gmail.com", "doc": "12345678909"}]
usuarios = {"admin": {"senha": bcrypt.hashpw(b"1234", bcrypt.gensalt()), "ativo": True}}


def validar_cliente(nome, email, doc):
    erros = []
    if not nome.strip():
        erros.append("Nome vazio.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        erros.append("E-mail inválido.")
    if not (CPF().validate(doc) or CNPJ().validate(doc)):
        erros.append("CPF/CNPJ inválido.")
    elif any(c["doc"] == doc for c in clientes):
        erros.append("CPF/CNPJ já cadastrado.")
    return erros


def login(usuario, senha):
    u = usuarios.get(usuario)
    if not u:
        return "Usuário não encontrado."
    if not u["ativo"]:
        return "Usuário inativo."
    if not bcrypt.checkpw(senha.encode(), u["senha"]):
        return "Senha incorreta."
    return "Login feito com sucesso!"


def main():
    nome = input("Nome: ")
    email = input("E-mail: ")
    doc = re.sub(r"\D", "", input("CPF ou CNPJ: "))

    erros = validar_cliente(nome, email, doc)
    if erros:
        print("Falha no cadastro:", *erros, sep="\n- ")
    else:
        clientes.append({"nome": nome, "email": email, "doc": doc})
        print("Cadastro realizado!")

    print(login(input("Usuário: "), input("Senha: ")))


if __name__ == "__main__":
    main()