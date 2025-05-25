import os

def criar_estrutura_arquivos(base_path="."):
    """
    Cria uma estrutura de diretórios e arquivos vazios na pasta especificada.

    Args:
        base_path (str): O caminho base onde a estrutura será criada.
                         Padrão é ".", que significa o diretório atual.
    """

    # Lista de diretórios a serem criados
    # Inclui diretórios que podem ficar vazios ou são pais de outros
    diretorios = [
        "css",
        "js",
        "assets", # ou "images" - escolhemos "assets" por ser mais genérico
        "assets/images",
        "assets/icons",
        "doc"
    ]

    # Lista de arquivos vazios a serem criados (com seus caminhos relativos)
    arquivos = [
        "index.html",
        "committees.html",
        "speakers.html",
        "programme.html",
        "registration.html",
        "abstract-submission.html",
        "venue-travel.html",  # Escolha entre venue-travel.html ou reach-us.html
        "accommodation.html",
        "explore-joao-pessoa.html", # Escolha entre explore-joao-pessoa.html ou nearby-attractions.html
        "cultural-program.html",
        "contact.html",

        "css/style.css",
        # "css/bootstrap.min.css", # Opcional, não criar por padrão

        "js/script.js",
        # "js/bootstrap.bundle.min.js", # Opcional, não criar por padrão

        "assets/images/banner-bricsagac2025-jp.jpg",
        "assets/images/logo-brics-agac-2025.png",
        "assets/images/logo-ufpb.png",
        "assets/images/logo-sbf.png",
        "assets/images/logo-sponsor1.png",
        "assets/images/speaker-photo-example.png", # Placeholder para o padrão speaker-photo-[lastname].png
        "assets/images/avatar-committee-member.png",
        "assets/images/map-venue-jp.png",
        "assets/images/jp-tambau.jpg",
        "assets/images/jp-farol.jpg",
        "assets/images/jp-seixas.jpg",
        "assets/images/placeholder_image_01.jpg", # Para "... (outras imagens placeholder)"
        "assets/images/placeholder_image_02.jpg", # Para "... (outras imagens placeholder)"
        # Nenhum arquivo SVG específico em assets/icons/ por padrão

        "doc/BRICS-AGAC2025-Programme-v1.pdf",
        "doc/BRICS-AGAC2025-Abstracts-v1.pdf",
        "doc/abstract_template.docx"
    ]

    print(f"Criando estrutura de arquivos em: {os.path.abspath(base_path)}\n")

    # Criar diretórios
    for diretorio in diretorios:
        path_completo = os.path.join(base_path, diretorio)
        try:
            os.makedirs(path_completo, exist_ok=True)
            print(f"Diretório criado/existente: {path_completo}")
        except OSError as e:
            print(f"Erro ao criar diretório {path_completo}: {e}")
            return # Interrompe se não conseguir criar um diretório essencial

    # Criar arquivos vazios
    for arquivo in arquivos:
        path_completo = os.path.join(base_path, arquivo)
        # Garante que o diretório pai do arquivo exista
        # (redundante se todos os pais estiverem em 'diretorios', mas seguro)
        dir_pai = os.path.dirname(path_completo)
        if dir_pai: # Se não for um arquivo na raiz do base_path
            try:
                os.makedirs(dir_pai, exist_ok=True)
            except OSError as e:
                print(f"Erro ao criar diretório pai {dir_pai} para {path_completo}: {e}")
                continue # Pula este arquivo se não conseguir criar o diretório pai

        try:
            # Abre o arquivo em modo de escrita ('w'). Se não existir, cria. Se existir, sobrescreve (vazio).
            with open(path_completo, 'w') as f:
                pass  # Cria um arquivo vazio
            print(f"Arquivo criado: {path_completo}")
        except IOError as e:
            print(f"Erro ao criar arquivo {path_completo}: {e}")

    print("\nEstrutura de arquivos criada com sucesso!")

if __name__ == "__main__":
    # O script irá criar a estrutura na pasta onde ele mesmo está localizado.
    # Se você quiser especificar uma subpasta, mude o argumento de criar_estrutura_arquivos.
    # Por exemplo: criar_estrutura_arquivos("meu_projeto_web")
    criar_estrutura_arquivos()