```plaintext
# Git Automate

Este projeto fornece uma interface de linha de comando para gerenciar repositórios Git utilizando Python. Ele inclui funcionalidades para inicializar repositórios, conectar a repositórios remotos, adicionar arquivos, fazer commits, push, pull, e muito mais.

## Funcionalidades

- Inicializar repositório Git (`git init`)
- Conectar a repositório remoto (`git conectar`)
- Adicionar arquivos ao stage (`git adicionar`)
- Fazer commit (`git commit`)
- Fazer push (`git push`)
- Exibir status do repositório (`git status`)
- Fazer checkout em uma branch (`git checkout`)
- Fazer pull (`git pull`)
- Mostrar últimos commits (`git log`)
- Mostrar diferenças (`git diff`)
- Clonar repositório (`git clone`)
- Configuração interativa (`git config`)
- Adicionar, comitar e fazer push de uma só vez (`git pushall`)

## Como Usar

### Inicializar Repositório

```sh
python git.py init --caminho /caminho/do/projeto
```

### Conectar a Repositório Remoto

```sh
python git.py conectar --caminho /caminho/do/projeto --url https://github.com/usuario/repo.git --branch main
```

### Adicionar Arquivos ao Stage

```sh
python git.py adicionar --caminho /caminho/do/projeto
```

### Fazer Commit

```sh
python git.py commit --caminho /caminho/do/projeto --mensagem "Mensagem do commit"
```

### Fazer Push

```sh
python git.py push --caminho /caminho/do/projeto --branch main
```

### Exibir Status do Repositório

```sh
python git.py status --caminho /caminho/do/projeto
```

### Fazer Checkout em uma Branch

```sh
python git.py checkout --caminho /caminho/do/projeto --branch nova-branch
```

### Fazer Pull

```sh
python git.py pull --caminho /caminho/do/projeto --branch main
```

### Mostrar Últimos Commits

```sh
python git.py log --caminho /caminho/do/projeto --limit 10
```

### Mostrar Diferenças

```sh
python git.py diff --caminho /caminho/do/projeto
```

### Clonar Repositório

```sh
python git.py clone https://github.com/usuario/repo.git --destino /caminho/do/destino
```

### Configuração Interativa

```sh
python git.py config --caminho /caminho/do/projeto
```

### Adicionar, Comitar e Fazer Push de uma Só Vez

```sh
python git.py pushall --caminho /caminho/do/projeto --mensagem "Mensagem do commit"
```

## Requisitos

- Python 3.x
- Git instalado e configurado no sistema

## Instalação

Clone o repositório e navegue até o diretório do projeto:

```sh
git clone https://github.com/usuario/git_automate.git
cd git_automate
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
```