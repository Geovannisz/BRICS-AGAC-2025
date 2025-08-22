import os
from bs4 import BeautifulSoup, NavigableString

def add_lang_switcher(soup):
    navbar = soup.find('ul', class_='navbar-nav')
    if navbar and not soup.find('a', id='lang-switcher-en'):
        lang_switcher_html = """
        <li class="nav-item d-flex align-items-center lang-switcher-container">
            <a class="nav-link lang-switcher" href="#" id="lang-switcher-en" style="font-weight: bold;">EN</a>
            <span class="nav-link disabled" style="padding: 0 0.25rem;">/</span>
            <a class="nav-link lang-switcher" href="#" id="lang-switcher-pt">PT</a>
        </li>
        """
        navbar.append(BeautifulSoup(lang_switcher_html, 'html.parser'))

def translate_element(tag, translations):
    if not tag.has_attr('data-lang-en'):
        if tag.string and tag.string.strip():
            original_text = tag.string.strip()
            if original_text in translations:
                portuguese_text = translations[original_text]
                tag['data-lang-en'] = original_text
                tag['data-lang-pt'] = portuguese_text
        else:
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

    tags_to_translate = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'a', 'span', 'li', 'button', 'title', 'label']
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

        # Programme Page
        "Symposium Programme": "Programação do Simpósio",
        "A detailed schedule of talks, sessions, and events for BRICS-AGAC 2025.": "Um cronograma detalhado de palestras, sessões e eventos para o BRICS-AGAC 2025.",
        "The full programme will be available soon.": "A programação completa estará disponível em breve.",
        "Download Preliminary Programme (PDF)": "Baixar Programação Preliminar (PDF)",

        # Registration Page
        "Registration Information": "Informações de Inscrição",
        "Join us for the 5th BRICS-AGAC Symposium. Register below.": "Junte-se a nós no 5º Simpósio BRICS-AGAC. Inscreva-se abaixo.",
        "Registration Fees": "Taxas de Inscrição",
        "Early Bird (Until October 31, 2025)": "Inscrição Antecipada (Até 31 de outubro de 2025)",
        "Standard (From November 1, 2025)": "Inscrição Normal (A partir de 1 de novembro de 2025)",
        "Students": "Estudantes",
        "Regular Participants": "Participantes Regulares",
        "Online Registration Form": "Formulário de Inscrição Online",
        "Registration form will be available soon.": "O formulário de inscrição estará disponível em breve.",

        # Abstract Submission Page
        "Abstract Submission": "Submissão de Resumos",
        "Submit your abstract to be considered for a presentation at the symposium.": "Envie seu resumo para ser considerado para uma apresentação no simpósio.",
        "Submission Guidelines": "Diretrizes para Submissão",
        "Abstracts must be written in English.": "Os resumos devem ser escritos em inglês.",
        "The abstract body should not exceed 300 words.": "O corpo do resumo não deve exceder 300 palavras.",
        "Please use the official template for formatting your abstract.": "Por favor, use o modelo oficial para formatar seu resumo.",
        "Download Abstract Template (.docx)": "Baixar Modelo de Resumo (.docx)",
        "Submission Deadline": "Prazo para Submissão",
        "All abstracts must be submitted by November 14, 2025.": "Todos os resumos devem ser enviados até 14 de novembro de 2025.",
        "Submit Your Abstract": "Envie Seu Resumo",
        "The submission portal will be available soon.": "O portal de submissão estará disponível em breve.",

        # Venue & Travel Page
        "Venue & Travel Information": "Informações sobre Local e Viagem",
        "Details about the event location and how to get there.": "Detalhes sobre o local do evento e como chegar lá.",
        "Symposium Venue": "Local do Simpósio",
        "The 5th BRICS-AGAC Symposium will be held at the Federal University of Paraíba (UFPB) in João Pessoa, Brazil.": "O 5º Simpósio BRICS-AGAC será realizado na Universidade Federal da Paraíba (UFPB) em João Pessoa, Brasil.",
        "The specific auditorium and campus details will be provided closer to the event date.": "O auditório específico e os detalhes do campus serão fornecidos mais perto da data do evento.",
        "UFPB Campus I, Castelo Branco, João Pessoa - PB, 58051-900, Brazil": "UFPB Campus I, Castelo Branco, João Pessoa - PB, 58051-900, Brasil",
        "Getting to João Pessoa": "Como Chegar a João Pessoa",
        "By Air": "De Avião",
        "João Pessoa is served by Presidente Castro Pinto International Airport (JPA), which receives flights from major Brazilian cities.": "João Pessoa é servida pelo Aeroporto Internacional Presidente Castro Pinto (JPA), que recebe voos das principais cidades brasileiras.",
        "By Bus": "De Ônibus",
        "The city's bus terminal (Terminal Rodoviário) connects João Pessoa to many cities in the Northeast and other regions of Brazil.": "O terminal rodoviário da cidade conecta João Pessoa a muitas cidades do Nordeste e outras regiões do Brasil.",
        "Local Transportation": "Transporte Local",
        "Taxis, ride-sharing services (like Uber), and local buses are readily available for getting around the city.": "Táxis, serviços de transporte por aplicativo (como Uber) e ônibus locais estão prontamente disponíveis para se locomover pela cidade.",

        # Accommodation Page
        "Accommodation": "Hospedagem",
        "Find recommended hotels and lodging options for your stay in João Pessoa.": "Encontre hotéis e opções de hospedagem recomendados para sua estadia em João Pessoa.",
        "Official Partner Hotels": "Hotéis Parceiros Oficiais",
        "We have partnered with the following hotels to offer special rates for symposium attendees. Please mention 'BRICS-AGAC 2025' when booking.": "Fizemos parceria com os seguintes hotéis para oferecer tarifas especiais para os participantes do simpósio. Por favor, mencione 'BRICS-AGAC 2025' ao fazer a reserva.",
        "Hotel Placeholder 1": "Hotel Modelo 1",
        "A brief description of the hotel, its amenities, and distance from the venue.": "Uma breve descrição do hotel, suas comodidades e distância do local do evento.",
        "Visit Website": "Visitar Site",
        "Hotel Placeholder 2": "Hotel Modelo 2",
        "Hotel Placeholder 3": "Hotel Modelo 3",

        # Explore João Pessoa Page
        "Explore João Pessoa": "Explore João Pessoa",
        "Discover the beauty and culture of our host city.": "Descubra a beleza e a cultura da nossa cidade anfitriã.",
        "About João Pessoa": "Sobre João Pessoa",
        "João Pessoa, the capital of Paraíba, is one of the oldest cities in Brazil and the easternmost city in the Americas. Known as 'the city where the sun rises first,' it boasts beautiful beaches, a rich cultural heritage, and lush green spaces.": "João Pessoa, capital da Paraíba, é uma das cidades mais antigas do Brasil e a cidade mais oriental das Américas. Conhecida como 'a cidade onde o sol nasce primeiro', possui belas praias, um rico patrimônio cultural e exuberantes áreas verdes.",
        "Tourist Attractions": "Atrações Turísticas",
        "Ponta do Seixas": "Ponta do Seixas",
        "The easternmost point of the Americas, offering breathtaking sunrise views.": "O ponto mais oriental das Américas, oferecendo vistas deslumbrantes do nascer do sol.",
        "Cabo Branco Lighthouse": "Farol do Cabo Branco",
        "A major landmark and a great spot for photos.": "Um marco importante e um ótimo local para fotos.",
        "Estação Cabo Branco": "Estação Cabo Branco",
        "A cultural and educational center designed by the renowned architect Oscar Niemeyer.": "Um centro cultural e educacional projetado pelo renomado arquiteto Oscar Niemeyer.",
        "Historic Center": "Centro Histórico",
        "Explore colonial architecture, beautiful churches, and charming squares.": "Explore a arquitetura colonial, belas igrejas e praças encantadoras.",
        "Tambaú Beach": "Praia de Tambaú",
        "A vibrant urban beach with a handicraft market and numerous restaurants.": "Uma vibrante praia urbana com um mercado de artesanato e inúmeros restaurantes.",
        "Areia Vermelha": "Areia Vermelha",
        "A temporary sandbank that appears at low tide, perfect for a unique boat trip.": "Um banco de areia temporário que aparece na maré baixa, perfeito para um passeio de barco único.",

        # BINGO Program Page
        "BINGO Program": "Programa BINGO",
        "Learn more about the BINGO Telescope project.": "Saiba mais sobre o projeto do Telescópio BINGO.",
        "The BINGO (Baryon Acoustic Oscillations from Integrated Neutral Gas Observations) telescope is a unique instrument being built in the hinterland of Paraíba, Brazil. Its primary goal is to map the distribution of neutral hydrogen gas to detect Baryon Acoustic Oscillations (BAOs) at radio frequencies. This will provide key data for understanding dark energy and the expansion of the universe.": "O telescópio BINGO (Oscilações Acústicas de Bárions a partir de Observações Integradas de Gás Neutro) é um instrumento único sendo construído no sertão da Paraíba, Brasil. Seu principal objetivo é mapear a distribuição de gás hidrogênio neutro para detectar Oscilações Acústicas de Bárions (BAOs) em frequências de rádio. Isso fornecerá dados cruciais para a compreensão da energia escura e da expansão do universo.",
        "The symposium will feature special sessions dedicated to the BINGO project, including its current status, scientific goals, and technological challenges.": "O simpósio contará com sessões especiais dedicadas ao projeto BINGO, incluindo seu status atual, objetivos científicos e desafios tecnológicos.",

        # Contact Page
        "Contact Us": "Contato",
        "Get in touch with the organizing committee.": "Entre em contato com o comitê organizador.",
        "For any inquiries regarding the symposium, please contact us at:": "Para quaisquer dúvidas sobre o simpósio, entre em contato conosco em:",
        "General Inquiries:": "Dúvidas Gerais:",
        "Local Organizing Committee:": "Comitê Organizador Local:",
        "Scientific Program:": "Programa Científico:",

        # Shirts Page
        "BRICS-AGAC 2025 Official Shirts": "Camisetas Oficiais BRICS-AGAC 2025",
        "Order your official symposium shirt and wear a piece of the event!": "Encomende sua camiseta oficial do simpósio e vista um pedaço do evento!",
        "Shirt Design": "Design da Camiseta",
        "Front": "Frente",
        "Back": "Costas",
        "The final design may have slight variations.": "O design final pode ter pequenas variações.",
        "Models & Sizes": "Modelos e Tamanhos",
        "Basic T-Shirt": "Camiseta Básica",
        "Baby Look (Women's Cut)": "Baby Look (Corte Feminino)",
        "Kids": "Infantil",
        "Size Chart": "Tabela de Tamanhos",
        "Order Form": "Formulário de Pedido",
        "Full Name": "Nome Completo",
        "Your full name": "Seu nome completo",
        "Email Address": "Endereço de Email",
        "Your email for confirmation": "Seu email para confirmação",
        "Shirt Model": "Modelo da Camiseta",
        "Select Model": "Selecione o Modelo",
        "Shirt Size": "Tamanho da Camiseta",
        "Select Size": "Selecione o Tamanho",
        "Quantity": "Quantidade",
        "Number of shirts": "Número de camisetas",
        "Total Price": "Preço Total",
        "R$ 0.00": "R$ 0,00",
        "Payment will be processed upon confirmation. Price per shirt: R$ 50.00.": "O pagamento será processado após a confirmação. Preço por camiseta: R$ 50,00.",
        "Submit Order": "Enviar Pedido",
    }


    files_to_process = [
        'abstract-submission/index.html',
        'accommodation/index.html',
        'bingo-program/index.html',
        'committees/index.html',
        'contact/index.html',
        'explore-joao-pessoa/index.html',
        'index.html',
        'programme/index.html',
        'registration/index.html',
        'shirts/index.html',
        'speakers/index.html',
        'venue-travel/index.html',
    ]

    for file in files_to_process:
        process_html_file(file, translations)

    print("Done.")
