import os
import sqlite3


def conectar_banco():
    """Configura e cria automaticamente o arquivo de banco de dados SQLite."""
    try:
        # Cria um arquivo chamado 'banco_ads.db' na pasta do seu projeto
        conexao = sqlite3.connect("banco_ads.db")
        return conexao
    except Exception as e:
        print(f"\n[ERRO] Não foi possível conectar ao banco de dados: {e}")
        return None


def criar_tabela():
    """Cria a tabela de usuários caso ela não exista no banco."""
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        comando_sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        """
        cursor.execute(comando_sql)
        conexao.commit()
        cursor.close()
        conexao.close()


def cadastrar_usuario():
    """Cadastra um novo usuário com nome e e-mail."""
    print("\n--- CADASTRAR USUÁRIO ---")
    nome = input("Digite o nome: ").strip()
    email = input("Digite o e-mail: ").strip()

    if not nome or not email:
        print("[ERRO] Nome e e-mail não podem ficar em branco.")
        return

    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            comando_sql = "INSERT INTO usuarios (nome, email) VALUES (?, ?);"
            cursor.execute(comando_sql, (nome, email))
            conexao.commit()
            print(f"\n[SUCESSO] {nome} foi cadastrado com sucesso!")
        except sqlite3.integrityerror:
            print(f"\n[ERRO] Este e-mail '{email}' já está cadastrado!")
        except Exception as e:
            print(f"\n[ERRO] Falha ao cadastrar: {e}")
        finally:
            cursor.close()
            conexao.close()


def listar_usuarios():
    """Exibe todos os usuários cadastrados no sistema."""
    print("\n--- LISTA DE USUÁRIOS ---")
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios ORDER BY id;")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("Nenhum usuário cadastrado ainda.")
        else:
            for usuario in usuarios:
                print(
                    f"ID: {usuario[0]} | Nome: {usuario[1]} | E-mail: {usuario[2]}"
                )

        cursor.close()
        conexao.close()


def menu_interativo():
    """Menu principal para interação do usuário no terminal."""
    criar_tabela()  # Garante que a tabela e o arquivo sejam criados ao iniciar

    while True:
        print("\n===============================")
        print("    SISTEMA DE CADASTRO ADS    ")
        print("===============================")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("0. Sair do Programa")
        print("===============================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        else:
            print("\n[AVISO] Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_interativo()
