```plaintext
# Git Automate

Este projeto fornece uma interface de linha de comando para gerenciar repositórios Git utilizando Python. Ele inclui funcionalidades para inicializar repositórios, conectar a repositórios remotos, adicionar arquivos, fazer commits, push, pull, e muito mais.

A ideia é facilitar dentro do VScode com um "git.py pushfull"
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
- Adicionar, comitar e fazer push de uma só vez (`git pushfull`)

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
python git.py pushfull --caminho /caminho/do/projeto --mensagem "Mensagem do commit"
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
Copyright (c) [2024] [Franklin Ferreira]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```