#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
import os
import subprocess
import sys

# ===========================================
# Utilitários de config.ini
# ===========================================
def carregar_config(caminho_config="config.ini"):
    """Lê as configurações do arquivo .ini (caso exista)."""
    config = configparser.ConfigParser()
    if os.path.exists(caminho_config):
        config.read(caminho_config, encoding="utf-8")
    return config

def salvar_config(config, caminho_config="config.ini"):
    """Salva (sobrescreve) o arquivo de configuração config.ini."""
    with open(caminho_config, 'w', encoding='utf-8') as f:
        config.write(f)

    # Adicionar 'config.ini' ao .gitignore, se ainda não existir
    gitignore_path = os.path.join(os.path.dirname(caminho_config), '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r+', encoding='utf-8') as f:
            linhas = f.read().splitlines()
            if 'config.ini' not in linhas:
                f.write('\nconfig.ini\n.gitignore\n')
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write('config.ini\n.gitignore\n')

# ===========================================
# Funções Git
# ===========================================
def git_init(caminho_projeto):
    """Inicializa repositório Git no caminho especificado (git init)."""
    subprocess.run(["git", "init"], cwd=caminho_projeto, check=True)
    print(f"[OK] Repositório Git inicializado em {caminho_projeto}")

def git_connect(caminho_projeto, url_remota, branch="main"):
    if not os.path.isdir(os.path.join(caminho_projeto, ".git")):
        git_init(caminho_projeto)

    subprocess.run(["git", "branch", "-M", branch], cwd=caminho_projeto, check=True)

    # Tenta adicionar origin
    result = subprocess.run(["git", "remote", "add", "origin", url_remota],
                            cwd=caminho_projeto,
                            text=True,
                            capture_output=True)

    if result.returncode != 0:
        # Verifica se o erro foi "remote origin already exists"
        if "remote origin already exists" in result.stderr.lower():
            print("[AVISO] O remoto 'origin' já existe. Nada a fazer.")
        else:
            # Se for outro erro, lança exceção
            result.check_returncode()
    else:
        print(f"[OK] Remote origin adicionado: {url_remota} (branch: {branch})")

def git_add(caminho_projeto):
    """Adiciona todos os arquivos ao stage (equivalente a 'git add .')."""
    subprocess.run(["git", "add", "."], cwd=caminho_projeto, check=True)
    print("[OK] Arquivos adicionados ao stage.")

def git_commit(caminho_projeto, mensagem="Update"):
    # Verifica se há algo para commitar
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=caminho_projeto, capture_output=True, text=True
    )
    if not status_result.stdout.strip():
        print("[OK] Nada para commitar.")
        return

    subprocess.run(["git", "commit", "-m", mensagem], cwd=caminho_projeto, check=True)
    print(f"[OK] Commit realizado: {mensagem}")

def git_push(caminho_projeto, branch="master"):
    """Faz push (git push -u origin <branch>)."""
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=caminho_projeto, check=True)
    print(f"[OK] Push realizado para a branch '{branch}'")

def git_status(caminho_projeto):
    """Exibe status do repositório (equivalente a 'git status')."""
    subprocess.run(["git", "status"], cwd=caminho_projeto, check=True)

def git_checkout(caminho_projeto, branch):
    """
    Faz checkout em uma determinada branch (git checkout <branch>).
    Se a branch não existir, cria com 'git checkout -b <branch>'.
    """
    resultado = subprocess.run(["git", "checkout", branch], cwd=caminho_projeto)
    if resultado.returncode != 0:
        subprocess.run(["git", "checkout", "-b", branch], cwd=caminho_projeto, check=True)
        print(f"[OK] Branch '{branch}' criada e selecionada.")

def git_pull(caminho_projeto, branch="master"):
    """Faz pull (git pull origin <branch>)."""
    try:
        subprocess.run(["git", "pull", "origin", branch, "--allow-unrelated-histories"], cwd=caminho_projeto, check=True)
        print(f"[OK] Pull realizado da branch '{branch}'")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao fazer pull: {e}")
        print("Por favor, resolva os conflitos de mesclagem manualmente e tente novamente.")
        exit(1)

def git_log(caminho_projeto, limit=10):
    """Mostra últimos commits (git log --oneline -n <limit>)."""
    subprocess.run(["git", "log", "--oneline", "-n", str(limit)], cwd=caminho_projeto, check=True)

def git_diff(caminho_projeto):
    """Mostra diferenças (git diff)."""
    subprocess.run(["git", "diff"], cwd=caminho_projeto, check=True)

def git_clone(url_remota, caminho_destino="."):
    """
    Clona um repositório (git clone <url> <destino>).
    Se 'destino' não for especificado, clona na pasta atual.
    """
    subprocess.run(["git", "clone", url_remota, caminho_destino], check=True)
    print(f"[OK] Repositório clonado de {url_remota} para {caminho_destino}")

# ===========================================
# Função pushfull (add + commit + push)
# ===========================================
def git_pushfull(caminho_projeto, mensagem, config):
    branch_config = config.get('git', 'branch', fallback='main')
    git_add(caminho_projeto)
    git_commit(caminho_projeto, mensagem)
    git_pull(caminho_projeto, branch=branch_config)
    git_push(caminho_projeto, branch=branch_config)

# ===========================================
# Subcomando config (interativo + conectar)
# ===========================================
def git_config_interativo(args, caminho_config="config.ini"):
    """
    Ajusta (cria/edita) o arquivo config.ini para armazenar as variáveis (url, branch, etc.).
    - Se não houver argumentos, pergunta interativamente.
    - Ao final, mostra resumo e pergunta se deseja salvar.
    - Se salvar, pergunta se deseja também conectar ao remoto (git remote add origin).
    """
    config = carregar_config(caminho_config)
    if "git" not in config:
        config["git"] = {}

    # Valores atuais no config.ini (caso existam)
    url_atual = config["git"].get("url", "")
    branch_atual = config["git"].get("branch", "")
    username_atual = config["git"].get("username", "")
    token_atual = config["git"].get("token", "")

    # 1. Capturar/parâmetros ou interativo
    if args.url:
        nova_url = args.url
    else:
        nova_url = input(f"URL do repositório [{url_atual}]: ").strip()
        if not nova_url:
            nova_url = url_atual

    if args.branch:
        nova_branch = args.branch
    else:
        nova_branch = input(f"Branch principal [{branch_atual}]: ").strip()
        if not nova_branch:
            nova_branch = branch_atual

    if args.username:
        novo_username = args.username
    else:
        novo_username = input(f"Username (Git/GitHub) [{username_atual}]: ").strip()
        if not novo_username:
            novo_username = username_atual

    if args.token:
        novo_token = args.token
    else:
        novo_token = input(f"Token ou senha [{token_atual}]: ").strip()
        if not novo_token:
            novo_token = token_atual

    # 2. Mostra resumo e pergunta se quer salvar
    print("\n*** Resumo das configurações ***")
    print(f"URL:       {nova_url}")
    print(f"Branch:    {nova_branch}")
    print(f"Username:  {novo_username}")
    print(f"Token:     {novo_token}")
    confirma = input("\nDeseja salvar essas configurações? [s/N] ").strip().lower()

    if confirma == "s":
        # Salva config.ini
        config["git"]["url"] = nova_url
        config["git"]["branch"] = nova_branch
        config["git"]["username"] = novo_username
        config["git"]["token"] = novo_token

        salvar_config(config, caminho_config)
        print(f"[OK] Configurações salvas em '{caminho_config}'\n")

        # Pergunta se quer conectar agora
        conectar_agora = input(f"Deseja conectar agora ao repositório remoto '{nova_url}'? [s/N] ").strip().lower()
        if conectar_agora == "s":
            caminho_repo = args.caminho  # path do repo local
            try:
                git_connect(caminho_repo, nova_url, nova_branch)
            except subprocess.CalledProcessError as e:
                print(f"[ERRO] Falha ao conectar: {e}")
        else:
            print("Ok, repositório não foi conectado agora.\n")
    else:
        print("Operação cancelada. Nada foi alterado.\n")

# ===========================================
# main() - argparse
# ===========================================
def main():
    parser = argparse.ArgumentParser(
        description="Gerenciador de comandos Git via Python, incluindo 'pushfull' e 'config' que conecta."
    )
    subparsers = parser.add_subparsers(dest="acao", help="Escolha qual subcomando executar.")

    # git init
    p_init = subparsers.add_parser("init", help="Inicializa repositório Git no diretório.")
    p_init.add_argument("--caminho", default=".", help="Caminho do repositório local (padrão: .)")

    # git conectar
    p_connect = subparsers.add_parser("conectar", help="Conecta repo local a um remoto (git remote add origin...).")
    p_connect.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_connect.add_argument("--url", help="URL remota do repositório (ex.: https://github.com/...).")
    p_connect.add_argument("--branch", default="master", help="Nome da branch principal (padrão: master).")

    # git adicionar
    p_add = subparsers.add_parser("adicionar", help="Adiciona arquivos ao stage (git add .).")
    p_add.add_argument("--caminho", default=".", help="Caminho do repositório local (padrão: .)")

    # git commit
    p_commit = subparsers.add_parser("commit", help="Faz commit (git commit -m ...).")
    p_commit.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_commit.add_argument("--mensagem", "-m", default="Update", help="Mensagem do commit (padrão: 'Update').")

    # git push
    p_push = subparsers.add_parser("push", help="Faz push para o remoto (git push -u origin <branch>).")
    p_push.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_push.add_argument("--branch", default="master", help="Branch a enviar (padrão: master).")

    # git status
    p_status = subparsers.add_parser("status", help="Exibe status do repositório (git status).")
    p_status.add_argument("--caminho", default=".", help="Caminho do repositório local.")

    # git checkout
    p_checkout = subparsers.add_parser("checkout", help="Faz checkout em uma branch (ou cria se não existir).")
    p_checkout.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_checkout.add_argument("branch", help="Nome da branch para checkout.")

    # git pull
    p_pull = subparsers.add_parser("pull", help="Faz pull da branch (git pull origin <branch>).")
    p_pull.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_pull.add_argument("--branch", default="master", help="Branch a receber (padrão: master).")

    # git log
    p_log = subparsers.add_parser("log", help="Mostra últimos commits (git log --oneline -n <limit>).")
    p_log.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_log.add_argument("--limit", default=10, type=int, help="Quantidade de commits a exibir (padrão: 10).")

    # git diff
    p_diff = subparsers.add_parser("diff", help="Mostra diferenças (git diff).")
    p_diff.add_argument("--caminho", default=".", help="Caminho do repositório local.")

    # git clone
    p_clone = subparsers.add_parser("clone", help="Clona um repositório remoto (git clone <url> <destino>).")
    p_clone.add_argument("url", help="URL do repositório remoto (HTTPS ou SSH).")
    p_clone.add_argument("--destino", default=".", help="Pasta de destino (padrão: atual).")

    # Subcomando config (interativo + conectar opcional)
    p_conf = subparsers.add_parser("config", help="Config interativo para definir config.ini e conectar.")
    p_conf.add_argument("--url", help="URL do repositório (ex.: https://github.com/usuario/projeto.git).")
    p_conf.add_argument("--branch", help="Branch principal (ex.: main, master, dev...).")
    p_conf.add_argument("--username", help="Nome de usuário do Git/GitHub.")
    p_conf.add_argument("--token", help="Token ou senha (cuidado!).")
    p_conf.add_argument("--caminho", default=".", help="Caminho do repositório local (padrão: .)")

    # Subcomando pushfull
    p_pushfull = subparsers.add_parser("pushfull", help="Adiciona, comita e faz push de uma só vez.")
    p_pushfull.add_argument("--caminho", default=".", help="Caminho do repositório local.")
    p_pushfull.add_argument("--mensagem", "-m", default="Update", help="Mensagem do commit (padrão: 'Update').")

    # Processa argumentos
    args = parser.parse_args()

    # Carrega config.ini (usado no pushfull e no conectar se faltar --url)
    config = carregar_config()

    # Despacha subcomandos
    if args.acao == "init":
        git_init(args.caminho)

    elif args.acao == "conectar":
        url = args.url if args.url else config["git"].get("url", None) if "git" in config else None
        if not url:
            print("[ERRO] É necessário fornecer uma URL do repositório remoto (--url) ou config.ini.")
            sys.exit(1)
        git_connect(args.caminho, url, args.branch)

    elif args.acao == "adicionar":
        git_add(args.caminho)

    elif args.acao == "commit":
        git_commit(args.caminho, args.mensagem)

    elif args.acao == "push":
        git_push(args.caminho, args.branch)

    elif args.acao == "status":
        git_status(args.caminho)

    elif args.acao == "checkout":
        git_checkout(args.caminho, args.branch)

    elif args.acao == "pull":
        git_pull(args.caminho, args.branch)

    elif args.acao == "log":
        git_log(args.caminho, args.limit)

    elif args.acao == "diff":
        git_diff(args.caminho)

    elif args.acao == "clone":
        git_clone(args.url, args.destino)

    elif args.acao == "config":
        git_config_interativo(args)

    elif args.acao == "pushfull":
        git_pushfull(args.caminho, args.mensagem, config)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
