import os

# Conteúdo padrão para alguns arquivos especiais
CONTEUDO_GITIGNORE = """# Python
__pycache__/
*.py[cod]
*.pyd
*.pyo
*.pyc

# Virtual environment
.venv/
venv/
"""

CONTEUDO_README = """

Este projeto utiliza Python e segue uma estrutura de pastas modular.
"""

CONTEUDO_MAIN = """def main():
    print("Iniciando o sistema...")

if __name__ == "__main__":
    main()
"""

CONTEUDO_REQUIREMENTS = """pymongo
requests
cryptography
"""

def criar_arquivo(caminho_arquivo):
    """
    Cria um arquivo com conteúdo padrão para alguns nomes específicos
    ou vazio, caso contrário.
    """
    nome = os.path.basename(caminho_arquivo).lower()

    # Define conteúdo com base no nome do arquivo
    if nome == ".gitignore":
        conteudo = CONTEUDO_GITIGNORE
    elif nome == "readme.md":
        conteudo = CONTEUDO_README
    elif nome == "main.py":
        conteudo = CONTEUDO_MAIN
    elif nome == "requirements.txt":
        conteudo = CONTEUDO_REQUIREMENTS
    else:
        conteudo = ""  # Vazio para qualquer outro arquivo

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def main():
    # Diretório base onde ficam todos os projetos
    diretorio_base = r"C:\vscode"

    # Nome do sistema (pasta do sistema)
    nome_sistema = "name"

    # Caminho raiz do projeto: ex. C:\vscode\
    raiz_projeto = os.path.join(diretorio_base, nome_sistema)

    # Estrutura de pastas e arquivos (dicionário):
    #  - chave = pasta
    #  - valor = lista de arquivos
    estrutura = {
        # Raiz do projeto
        raiz_projeto: [
            ".gitignore",
            "README.md",
            "main.py",
            "requirements.txt",
        ],
        # Pasta src/
        os.path.join(raiz_projeto, "src"): [
            "__init__.py",
        ],
        # Pasta src/db/
        os.path.join(raiz_projeto, "src", "db"): [
            "__init__.py",
            "conexao.py",
        ],
        # Pasta src/cadastro/
        os.path.join(raiz_projeto, "src", "cadastro"): [
            "__init__.py",
            "cadastro_usuario.py",
        ],
        # Pasta src/captura/
        os.path.join(raiz_projeto, "src", "captura"): [
            "__init__.py",
            "captura_api.py",
            "processador_eventos.py",
        ],
        # Subpasta src/captura/tipos_eventos/
        os.path.join(raiz_projeto, "src", "captura", "tipos_eventos"): [
            "__init__.py",
            "evento_a.py",
            "evento_b.py",
            "evento_c.py",
            "evento_default.py",
        ],
        # Pasta src/utils/
        os.path.join(raiz_projeto, "src", "utils"): [
            "__init__.py",
            "funcoes_auxiliares.py",
        ],
        # Pasta src/services/
        os.path.join(raiz_projeto, "src", "services"): [
            "__init__.py",
            "exemplo_service.py",
        ],
        # Pasta tests/
        os.path.join(raiz_projeto, "tests"): [
            "__init__.py",
            "test_conexao.py",
            "test_cadastro_usuario.py",
            "test_captura_api.py",
        ],
    }

    # Cria as pastas e arquivos
    for pasta, arquivos in estrutura.items():
        os.makedirs(pasta, exist_ok=True)  # Cria a pasta se não existir
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, arquivo)
            criar_arquivo(caminho_arquivo)

    print(f"Estrutura de diretórios e arquivos criada em '{raiz_projeto}' com sucesso.")

if __name__ == "__main__":
    main()
