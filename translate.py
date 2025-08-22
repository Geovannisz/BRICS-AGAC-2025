import os
from bs4 import BeautifulSoup, NavigableString

def get_html_files(root_dir):
    html_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def add_lang_switcher(soup):
    navbar = soup.find('ul', class_='navbar-nav')
    if navbar and not soup.find('a', id='lang-switcher-en'):
        lang_switcher_html = """
        <li class="nav-item d-flex align-items-center">
            <a class="nav-link lang-switcher" href="#" id="lang-switcher-en" style="font-weight: bold;">EN</a>
            <span class="nav-link disabled" style="padding: 0 0.25rem;">/</span>
            <a class="nav-link lang-switcher" href="#" id="lang-switcher-pt">PT</a>
        </li>
        """
        navbar.append(BeautifulSoup(lang_switcher_html, 'html.parser'))

def translate_element(tag, translations):
    if not tag.has_attr('data-lang-en'):
        # Handle tags with only string content
        if tag.string and tag.string.strip():
            original_text = tag.string.strip()
            if original_text in translations:
                portuguese_text = translations[original_text]
                tag['data-lang-en'] = original_text
                tag['data-lang-pt'] = portuguese_text
        else: # Handle tags with mixed content (like the footer)
            # This is a bit more complex, we'll get the full inner HTML
            children = list(tag.children)
            if any(isinstance(c, NavigableString) and c.strip() for c in children):
                original_html = ''.join(str(c) for c in tag.contents).strip()
                if original_html in translations:
                    portuguese_html = translations[original_html]
                    tag['data-lang-en'] = original_html
                    tag['data-lang-pt'] = portuguese_html


def process_html_file(filepath, translations):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    add_lang_switcher(soup)

    tags_to_translate = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'a', 'span', 'li', 'button', 'title']
    for tag in soup.find_all(tags_to_translate):
         translate_element(tag, translations)


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

if __name__ == "__main__":
    translations = {
        # General
        "Home": "Início",
        "Committees": "Comitês",
        "Speakers": "Palestrantes",
        "Programme": "Programação",
        "Shirts": "Camisetas",
        "Registration": "Inscrição",
        "Abstracts": "Resumos",
        "Local Info": "Informações Locais",
        "Venue & Travel": "Local e Viagem",
        "Accommodation": "Hospedagem",
        "Explore João Pessoa": "Explore João Pessoa",
        "BINGO Program": "Programa BINGO",
        "Contact": "Contato",
        "© 2024-2025 BRICS Association on Gravity, Astrophysics and Cosmology. All rights reserved.": "© 2024-2025 Associação BRICS de Gravitação, Astrofísica e Cosmologia. Todos os direitos reservados.",
        "5th BRICS-AGAC Symposium | João Pessoa, Paraíba, Brazil | December 2025": "5º Simpósio BRICS-AGAC | João Pessoa, Paraíba, Brasil | Dezembro 2025",

        # Index Page
        "5th BRICS-AGAC Symposium 2025": "5º Simpósio BRICS-AGAC 2025",
        "<i class=\"fas fa-map-marker-alt\"></i> João Pessoa, Paraíba, Brazil": "<i class=\"fas fa-map-marker-alt\"></i> João Pessoa, Paraíba, Brasil",
        "<i class=\"fas fa-calendar-alt\"></i> December 9-12, 2025": "<i class=\"fas fa-calendar-alt\"></i> 9 a 12 de dezembro de 2025",
        "Register Now": "Inscreva-se Agora",
        "View Programme": "Ver Programação",
        "Welcome to BRICS-AGAC 2025": "Bem-vindo ao BRICS-AGAC 2025",
        "Welcome to the 5th Symposium of the BRICS Association on Gravity, Astrophysics and Cosmology (BRICS-AGAC 2025), to be held in the vibrant city of João Pessoa, Brazil, in December 2025. This symposium continues the tradition of fostering collaboration and sharing cutting-edge research among scientists from BRICS nations and around the globe.": "Bem-vindo ao 5º Simpósio da Associação BRICS de Gravitação, Astrofísica e Cosmologia (BRICS-AGAC 2025), a ser realizado na vibrante cidade de João Pessoa, Brasil, em dezembro de 2025. Este simpósio continua a tradição de promover a colaboração e o compartilhamento de pesquisas de ponta entre cientistas das nações do BRICS e de todo o mundo.",
        "We invite you to explore the frontiers of cosmology, astrophysics, and gravitational physics in a stimulating and collaborative environment. Join us for insightful talks, engaging discussions, and networking opportunities with leading experts and young researchers in the field.": "Convidamos você a explorar as fronteiras da cosmologia, astrofísica e física gravitacional em um ambiente estimulante e colaborativo. Junte-se a nós para palestras perspicazes, discussões envolventes e oportunidades de networking com especialistas renomados e jovens pesquisadores da área.",
        "Important Dates": "Datas Importantes",
        "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Registration & Abstract Submission Opens:</strong> Now Open": "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Inscrições e Submissão de Resumos:</strong> Já abertas",
        "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Registration & Abstract Submission Deadline:</strong> November 14, 2025": "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Prazo para Inscrição e Submissão de Resumos:</strong> 14 de novembro de 2025",
        "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Symposium Dates:</strong> December 9-12, 2025": "<i class=\"fas fa-calendar-alt text-secondary me-2\"></i><strong>Datas do Simpósio:</strong> 9 a 12 de dezembro de 2025",
        "Organizers & Supporters": "Organizadores e Apoiadores",
        "Host Institution": "Instituição Anfitriã",
        "Federal University of Paraíba (UFPB)": "Universidade Federal da Paraíba (UFPB)",
        "(The exact auditorium will be announced soon)": "(O auditório exato será anunciado em breve)",
        "Organized by": "Organizado por",
        "BRICS Association on Gravity, Astrophysics and Cosmology": "Associação BRICS de Gravitação, Astrofísica e Cosmologia",
        "Supported by": "Apoiado por",
        "SECTIES (State Secretariat for Science, Technology, Innovation and Higher Education of Paraíba)": "SECTIES (Secretaria de Estado da Ciência, Tecnologia, Inovação e Ensino Superior da Paraíba)",

        # Committees Page
        "Organizing Committees": "Comitês Organizadores",
        "Meet the teams behind BRICS-AGAC 2025.": "Conheça as equipes por trás do BRICS-AGAC 2025.",
        "International Scientific Committee (ISC)": "Comitê Científico Internacional (ISC)",
        "Local Organizing Committee (LOC)": "Comitê Organizador Local (LOC)",
        "TS for the 'Esperança no Espaço' Project": "TS do Projeto 'Esperança no Espaço'",

        # Speakers Page
        "Invited Speakers": "Palestrantes Convidados",
        "Esteemed experts sharing their insights at BRICS-AGAC 2025.": "Renomados especialistas compartilhando seus conhecimentos no BRICS-AGAC 2025.",
        "Speakers will be announced soon.": "Os palestrantes serão anunciados em breve.",
    }


    html_files = get_html_files('.')
    # Exclude files that I have already manually edited or don't want to translate.
    files_to_exclude = ['/index.html', '/committees/index.html', 'thank-you.html']

    # Correctly filter files
    files_to_process = [
        f for f in html_files
        if not any(ex in f.replace('\\', '/') for ex in files_to_exclude)
    ]

    # Manually add back the files I want to process
    files_to_process.append('index.html')
    files_to_process.append('committees/index.html')
    files_to_process.append('speakers/index.html')

    # Remove duplicates
    files_to_process = list(set(files_to_process))


    for file in files_to_process:
        process_html_file(file, translations)

    print("Done.")
