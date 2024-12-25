import os
import shutil

def replicar_estrutura(origem, destino):
    """
    Lê a estrutura de 'origem' e recria a mesma hierarquia em 'destino'.
    - Todos os arquivos serão criados vazios, EXCETO o 'requirements.txt',
      cujo conteúdo será copiado integralmente.
    """
    for raiz, diretorios, arquivos in os.walk(origem):
        # Caminho relativo da pasta atual em relação à origem
        caminho_relativo = os.path.relpath(raiz, origem)
        
        # Caminho correspondente no destino
        destino_atual = os.path.join(destino, caminho_relativo)
        
        # Cria a pasta se ainda não existir
        os.makedirs(destino_atual, exist_ok=True)
        
        for nome_arquivo in arquivos:
            caminho_origem_arquivo = os.path.join(raiz, nome_arquivo)
            caminho_destino_arquivo = os.path.join(destino_atual, nome_arquivo)
            
            if nome_arquivo.lower() == "requirements.txt":
                # Copiar o conteúdo do requirements.txt
                shutil.copy2(caminho_origem_arquivo, caminho_destino_arquivo)
            else:
                # Criar arquivo vazio (sem conteúdo)
                with open(caminho_destino_arquivo, 'w', encoding='utf-8'):
                    pass

def main():
    # Exemplos de caminhos de origem e destino (ajuste conforme necessário)
    diretorio_origem = r"C:\vscode\exemplo_origem"
    diretorio_destino = r"C:\vscode\exemplo_destino"

    replicar_estrutura(diretorio_origem, diretorio_destino)
    print(f"Estrutura replicada de '{diretorio_origem}' para '{diretorio_destino}' com sucesso.")
    print("Arquivos criados vazios, exceto 'requirements.txt', que foi copiado com conteúdo.")

if __name__ == "__main__":
    main()
