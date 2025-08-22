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
    # This function is now more careful. It will only translate a tag if it has direct text content.
    if tag.string and tag.string.strip():
        original_text = tag.string.strip()
        if original_text in translations and not tag.has_attr('data-lang-en'):
            portuguese_text = translations[original_text]
            tag['data-lang-en'] = original_text
            tag['data-lang-pt'] = portuguese_text

def process_html_file(filepath, translations):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    add_lang_switcher(soup)

    # Translate all specified tags
    tags_to_translate = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'li', 'strong', 'button', 'label', 'small', 'td', 'th']
    for tag in soup.find_all(tags_to_translate):
         translate_element(tag, translations)

    # Special handling for the page <title>
    if soup.title and soup.title.string:
        original_title = soup.title.string.strip()
        if original_title in translations:
            soup.title['data-lang-en'] = original_title
            soup.title['data-lang-pt'] = translations[original_title]


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(formatter="html5")))

if __name__ == "__main__":
    translations = {
        # =====================================================================
        # == General / Shared Content
        # =====================================================================
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

        # =====================================================================
        # == Page Titles
        # =====================================================================
        "BRICS-AGAC 2025 | 5th Symposium | João Pessoa, Brazil": "BRICS-AGAC 2025 | 5º Simpósio | João Pessoa, Brasil",
        "Committees | BRICS-AGAC 2025": "Comitês | BRICS-AGAC 2025",
        "Invited Speakers | BRICS-AGAC 2025": "Palestrantes Convidados | BRICS-AGAC 2025",
        "Programme | BRICS-AGAC 2025": "Programação | BRICS-AGAC 2025",
        "Event Shirts | BRICS-AGAC 2025": "Camisetas do Evento | BRICS-AGAC 2025",
        "Registration | BRICS-AGAC 2025": "Inscrição | BRICS-AGAC 2025",
        "Abstract Submission | BRICS-AGAC 2025": "Submissão de Resumos | BRICS-AGAC 2025",
        "Venue & Travel | BRICS-AGAC 2025": "Local e Viagem | BRICS-AGAC 2025",
        "Accommodation | BRICS-AGAC 2025": "Hospedagem | BRICS-AGAC 2025",
        "Explore João Pessoa | BRICS-AGAC 2025": "Explore João Pessoa | BRICS-AGAC 2025",
        "BINGO Program | BRICS-AGAC 2025": "Programa BINGO | BRICS-AGAC 2025",
        "Contact Us | BRICS-AGAC 2025": "Contato | BRICS-AGAC 2025",

        # =====================================================================
        # == Index Page (index.html)
        # =====================================================================
        "5th BRICS-AGAC Symposium 2025": "5º Simpósio BRICS-AGAC 2025",
        "Register Now": "Inscreva-se Agora",
        "View Programme": "Ver Programação",
        "Welcome to BRICS-AGAC 2025": "Bem-vindo ao BRICS-AGAC 2025",
        "Welcome to the 5th Symposium of the BRICS Association on Gravity, Astrophysics and Cosmology (BRICS-AGAC 2025), to be held in the vibrant city of João Pessoa, Brazil, in December 2025. This symposium continues the tradition of fostering collaboration and sharing cutting-edge research among scientists from BRICS nations and around the globe.": "Bem-vindo ao 5º Simpósio da Associação BRICS de Gravitação, Astrofísica e Cosmologia (BRICS-AGAC 2025), a ser realizado na vibrante cidade de João Pessoa, Brasil, em dezembro de 2025. Este simpósio continua a tradição de promover a colaboração e o compartilhamento de pesquisas de ponta entre cientistas das nações do BRICS e de todo o mundo.",
        "We invite you to explore the frontiers of cosmology, astrophysics, and gravitational physics in a stimulating and collaborative environment. Join us for insightful talks, engaging discussions, and networking opportunities with leading experts and young researchers in the field.": "Convidamos você a explorar as fronteiras da cosmologia, astrofísica e física gravitacional em um ambiente estimulante e colaborativo. Junte-se a nós para palestras perspicazes, discussões envolventes e oportunidades de networking com especialistas renomados e jovens pesquisadores da área.",
        "Important Dates": "Datas Importantes",
        "Registration & Abstract Submission Opens: Now Open": "Inscrições e Submissão de Resumos: Já abertas",
        "Registration & Abstract Submission Deadline: November 14, 2025": "Prazo para Inscrição e Submissão de Resumos: 14 de novembro de 2025",
        "Symposium Dates: December 9-12, 2025": "Datas do Simpósio: 9 a 12 de dezembro de 2025",
        "Organizers & Supporters": "Organizadores e Apoiadores",
        "Host Institution": "Instituição Anfitriã",
        "Federal University of Paraíba (UFPB)": "Universidade Federal da Paraíba (UFPB)",
        "(The exact auditorium will be announced soon)": "(O auditório exato será anunciado em breve)",
        "Organized by": "Organizado por",
        "BRICS Association on Gravity, Astrophysics and Cosmology": "Associação BRICS de Gravitação, Astrofísica e Cosmologia",
        "Supported by": "Apoiado por",
        "SECTIES (State Secretariat for Science, Technology, Innovation and Higher Education of Paraíba)": "SECTIES (Secretaria de Estado da Ciência, Tecnologia, Inovação e Ensino Superior da Paraíba)",

        # =====================================================================
        # == Committees Page (committees/index.html)
        # =====================================================================
        "Organizing Committees": "Comitês Organizadores",
        "Meet the teams behind BRICS-AGAC 2025.": "Conheça as equipes por trás do BRICS-AGAC 2025.",
        "International Scientific Committee (ISC)": "Comitê Científico Internacional (ISC)",
        "Local Organizing Committee (LOC)": "Comitê Organizador Local (LOC)",
        "TS for the 'Esperança no Espaço' Project": "TS do Projeto 'Esperança no Espaço'",

        # =====================================================================
        # == Speakers Page (speakers/index.html)
        # =====================================================================
        "Invited Speakers": "Palestrantes Convidados",
        "Esteemed experts sharing their insights at BRICS-AGAC 2025.": "Renomados especialistas compartilhando seus conhecimentos no BRICS-AGAC 2025.",
        "Speakers will be announced soon.": "Os palestrantes serão anunciados em breve.",

        # =====================================================================
        # == Programme Page (programme/index.html)
        # =====================================================================
        "Conference Programme": "Programação da Conferência",
        "Schedule of events for BRICS-AGAC 2025.": "Cronograma de eventos para o BRICS-AGAC 2025.",
        "Programme will be announced soon.": "A programação será anunciada em breve.",

        # =====================================================================
        # == Registration Page (registration/index.html)
        # =====================================================================
        "Join us for BRICS-AGAC 2025 in João Pessoa!": "Junte-se a nós no BRICS-AGAC 2025 em João Pessoa!",
        "All participants are required to register. The registration fee includes access to all scientific sessions, conference materials, coffee breaks, welcome reception, and certificate of participation.": "Todos os participantes devem se inscrever. A taxa de inscrição inclui acesso a todas as sessões científicas, materiais da conferência, coffee breaks, recepção de boas-vindas e certificado de participação.",
        "Registration Fees": "Taxas de Inscrição",
        "Category": "Categoria",
        "Fee": "Taxa",
        "Regular Participant (Professors/Researchers)": "Participante Regular (Professores/Pesquisadores)",
        "Post-doctoral Participant": "Participante de Pós-doutorado",
        "Student Participant": "Participante Estudante",
        "(Proof of status required)": "(Comprovação de status necessária)",
        "Payment Methods": "Métodos de Pagamento",
        "To confirm your registration, please follow these steps carefully:": "Para confirmar sua inscrição, por favor, siga estes passos cuidadosamente:",
        "Use the subject line: \"Registration Payment - [Your Full Name]\".": "Use a linha de assunto: \"Pagamento de Inscrição - [Seu Nome Completo]\".",
        "Registration Process": "Processo de Inscrição",
        "To register for BRICS-AGAC 2025, please complete the external registration form. During registration, you will be required to submit your abstract. You will also have the option to express interest in the technical visit to the BINGO Telescope and to request an invitation letter for visa purposes.": "Para se inscrever no BRICS-AGAC 2025, por favor, preencha o formulário de inscrição externo. Durante a inscrição, você deverá submeter seu resumo. Você também terá a opção de expressar interesse na visita técnica ao Telescópio BINGO e de solicitar uma carta-convite para fins de visto.",
        "REGISTER NOW (via Google Forms)": "INSCREVA-SE AGORA (via Google Forms)",
        "Cancellation Policy": "Política de Cancelamento",
        "For registration cancellations, a 40% refund of the paid fee is applicable. Cancellation requests must be sent to the official event email address before the event start date.": "Para cancelamentos de inscrição, é aplicável um reembolso de 40% da taxa paga. Os pedidos de cancelamento devem ser enviados para o endereço de e-mail oficial do evento antes da data de início do evento.",
        "Important Notes:": "Notas Importantes:",
        "Student registration requires a valid student ID or a letter from your institution.": "A inscrição de estudante requer uma carteira de estudante válida ou uma carta da sua instituição.",
        "For any registration queries, please contact": "Para quaisquer dúvidas sobre a inscrição, entre em contato com",

        # =====================================================================
        # == Abstract Submission Page (abstract-submission/index.html)
        # =====================================================================
        "Share your research at BRICS-AGAC 2025.": "Compartilhe sua pesquisa no BRICS-AGAC 2025.",
        "Call for Abstracts": "Chamada de Resumos",
        "We invite submissions for oral and poster presentations for the 5th BRICS-AGAC Symposium. This is an excellent opportunity to present your work to an international audience of experts and peers in Gravity, Astrophysics, and Cosmology.": "Convidamos submissões para apresentações orais e de pôsteres para o 5º Simpósio BRICS-AGAC. Esta é uma excelente oportunidade para apresentar seu trabalho a uma audiência internacional de especialistas e colegas em Gravitação, Astrofísica e Cosmologia.",
        "Guidelines for Submission": "Diretrizes para Submissão",
        "Abstracts must be written in English.": "Os resumos devem ser escritos em inglês.",
        "The abstract body should not exceed": "O corpo do resumo não deve exceder",
        "300 words": "300 palavras",
        "Please indicate your preference for oral or poster presentation (the scientific committee will make the final decision).": "Por favor, indique sua preferência por apresentação oral ou em pôster (o comitê científico tomará a decisão final).",
        "Blind Submission:": "Submissão Cega:",
        "To ensure an unbiased selection process, please do not include your name or any identifying information in the abstract text. Submissions containing author names or affiliations will not be considered.": "Para garantir um processo de seleção imparcial, por favor, não inclua seu nome ou qualquer informação de identificação no texto do resumo. Submissões contendo nomes de autores ou afiliações não serão consideradas.",
        "Submissions should be made via the online submission portal, as indicated below.": "As submissões devem ser feitas através do portal de submissão online, conforme indicado abaixo.",
        "Scientific Themes/Topics": "Temas/Tópicos Científicos",
        "Abstracts are welcome in, but not limited to, the following areas:": "Resumos são bem-vindos nas seguintes áreas, mas não se limitando a elas:",
        "Early Universe Cosmology": "Cosmologia do Universo Primordial",
        "Inflationary Models": "Modelos Inflacionários",
        "Dark Matter & Dark Energy": "Matéria Escura e Energia Escura",
        "Large Scale Structure": "Estrutura em Larga Escala",
        "Cosmic Microwave Background": "Radiação Cósmica de Fundo em Micro-ondas",
        "Gravitational Waves: Theory & Observation": "Ondas Gravitacionais: Teoria e Observação",
        "Black Hole Physics & Astrophysics": "Física e Astrofísica de Buracos Negros",
        "Neutron Stars & Compact Objects": "Estrelas de Nêutrons e Objetos Compactos",
        "Modified Theories of Gravity": "Teorias Modificadas da Gravidade",
        "Quantum Gravity & Quantum Cosmology": "Gravidade Quântica e Cosmologia Quântica",
        "Numerical Relativity & Simulations": "Relatividade Numérica e Simulações",
        "Multi-messenger Astrophysics": "Astrofísica de Multi-mensageiros",
        "Important Dates for Abstract Submission": "Datas Importantes para Submissão de Resumos",
        "Abstract Submission Deadline:": "Prazo para Submissão de Resumos:",
        "November 14, 2025": "14 de novembro de 2025",
        "Note:": "Nota:",
        "Official acceptance letters will be provided upon request for participants who require them for visa applications or funding purposes.": "Cartas de aceitação oficiais serão fornecidas mediante solicitação para participantes que precisem delas para pedidos de visto ou fins de financiamento.",
        "How to Submit": "Como Submeter",
        "Abstracts must be submitted directly via the official registration form. The submission is a required step to complete your registration.": "Os resumos devem ser submetidos diretamente através do formulário de inscrição oficial. A submissão é um passo obrigatório para completar sua inscrição.",
        "SUBMIT ABSTRACT VIA REGISTRATION FORM": "SUBMETER RESUMO VIA FORMULÁRIO DE INSCRIÇÃO",
        "Book of Abstracts": "Livro de Resumos",
        "Accepted abstracts will be compiled into the official Book of Abstracts for the symposium. A digital copy will be made available to all registered participants.": "Os resumos aceitos serão compilados no Livro de Resumos oficial do simpósio. Uma cópia digital será disponibilizada a todos os participantes registrados.",
        "Link to Book of Abstracts (PDF - available after review and compilation):": "Link para o Livro de Resumos (PDF - disponível após revisão e compilação):",
        "For any queries regarding abstract submission, please contact the scientific committee at": "Para quaisquer dúvidas sobre a submissão de resumos, entre em contato com o comitê científico em",

        # =====================================================================
        # == Venue & Travel Page (venue-travel/index.html)
        # =====================================================================
        "Venue & Travel Information": "Informações sobre Local e Viagem",
        "Discover João Pessoa and how to reach the conference.": "Descubra João Pessoa e como chegar à conferência.",
        "Conference Venue": "Local da Conferência",
        "The 5th BRICS-AGAC Symposium will be held at the": "O 5º Simpósio BRICS-AGAC será realizado na",
        "Federal University of Paraíba (UFPB)": "Universidade Federal da Paraíba (UFPB)",
        ". The exact auditorium will be announced soon.": ". O auditório exato será anunciado em breve.",
        "Address:": "Endereço:",
        "UFPB - Campus I, Castelo Branco, João Pessoa, Paraíba, Brazil": "UFPB - Campus I, Castelo Branco, João Pessoa, Paraíba, Brasil",
        "This modern complex on the university campus is designed to host academic, scientific, and cultural events, offering an excellent infrastructure for an international conference. It is conveniently located with access to local amenities and other university facilities.": "Este moderno complexo no campus universitário é projetado para sediar eventos acadêmicos, científicos e culturais, oferecendo uma excelente infraestrutura para uma conferência internacional. Está convenientemente localizado com acesso a comodidades locais e outras instalações da universidade.",
        "View larger map": "Ver mapa ampliado",
        "About João Pessoa": "Sobre João Pessoa",
        "João Pessoa, the capital of the state of Paraíba, is one of the oldest cities in Brazil and is renowned for its lush greenery, beautiful urban beaches, and rich cultural heritage. It is famously known as \"the city where the sun rises first\" in the Americas, due to its location at Ponta do Seixas, the easternmost point of the continent.": "João Pessoa, capital do estado da Paraíba, é uma das cidades mais antigas do Brasil e é conhecida por sua vegetação exuberante, belas praias urbanas e rico patrimônio cultural. É famosa como \"a cidade onde o sol nasce primeiro\" nas Américas, devido à sua localização na Ponta do Seixas, o ponto mais oriental do continente.",
        "Visitors can enjoy a relaxed atmosphere, warm hospitality, and a variety of attractions, from historic colonial architecture to modern cultural centers. The city boasts a pleasant tropical climate, making it an inviting destination year-round.": "Os visitantes podem desfrutar de uma atmosfera descontraída, hospitalidade calorosa e uma variedade de atrações, desde a arquitetura colonial histórica até os modernos centros culturais. A cidade possui um clima tropical agradável, tornando-se um destino convidativo durante todo o ano.",
        "Getting to João Pessoa": "Como Chegar a João Pessoa",
        "By Air": "De Avião",
        "The primary airport serving the city is": "O principal aeroporto que serve a cidade é o",
        "João Pessoa-Presidente Castro Pinto International Airport (JPA)": "Aeroporto Internacional João Pessoa-Presidente Castro Pinto (JPA)",
        ". It receives domestic flights from major Brazilian cities and some international connections.": ". Ele recebe voos domésticos das principais cidades brasileiras e algumas conexões internacionais.",
        "From the airport to your hotel or the conference venue, options include:": "Do aeroporto para o seu hotel ou para o local da conferência, as opções incluem:",
        "Taxis:": "Táxis:",
        "Taxis are readily available at the airport. The estimated fare to the UFPB campus area is typically between BRL 50-70.": "Táxis estão prontamente disponíveis no aeroporto. A tarifa estimada para a área do campus da UFPB geralmente fica entre R$ 50-70.",
        "Ride-Sharing Apps:": "Aplicativos de Transporte:",
        "Services like Uber are available. The estimated fare to the UFPB campus area is typically between BRL 30-45.": "Serviços como Uber estão disponíveis. A tarifa estimada para a área do campus da UFPB geralmente fica entre R$ 30-45.",
        "Airport Transfers:": "Transfers de Aeroporto:",
        "Pre-booked shuttle services can be arranged through various local tourism agencies, such as Quality Receptivo, Luck Receptivo, and Jampatur.": "Serviços de shuttle pré-agendados podem ser organizados através de várias agências de turismo locais, como Quality Receptivo, Luck Receptivo e Jampatur.",
        "By Road": "De Carro",
        "João Pessoa is well-connected by federal highways if you are traveling from nearby cities or states. Intercity buses arrive at the main bus terminal (Rodoviária de João Pessoa).": "João Pessoa é bem conectada por rodovias federais se você estiver viajando de cidades ou estados vizinhos. Ônibus intermunicipais chegam ao terminal rodoviário principal (Rodoviária de João Pessoa).",
        "Visa Information": "Informações sobre Visto",
        "Participants from some countries may require a visa to enter Brazil. Please check the official": "Participantes de alguns países podem precisar de um visto para entrar no Brasil. Por favor, verifique o",
        "Brazil's Ministry of Foreign Affairs Consular Portal": "Portal Consular do Ministério das Relações Exteriores do Brasil",
        "for the most current visa requirements for your country.": "oficial para os requisitos de visto mais atuais para o seu país.",
        "Official invitation letters for visa purposes will be provided to registered participants upon request after abstract acceptance and registration payment.": "Cartas-convite oficiais para fins de visto serão fornecidas aos participantes registrados mediante solicitação após a aceitação do resumo e o pagamento da inscrição.",
        "Restaurant Suggestions": "Sugestões de Restaurantes",
        "Explore the local cuisine of João Pessoa. Here are some restaurant suggestions located near the conference venue at UFPB.": "Explore a culinária local de João Pessoa. Aqui estão algumas sugestões de restaurantes localizados perto do local da conferência na UFPB.",
        "On-Campus at UFPB": "No Campus da UFPB",
        "Restaurante Universitário (RU)": "Restaurante Universitário (RU)",
        "Phone:": "Telefone:",
        "The organizing committee is exploring the possibility of providing free lunch vouchers for participants.": "O comitê organizador está explorando a possibilidade de fornecer vales-refeição gratuitos para os participantes.",
        "Cozinha Caseira (near Central de Aulas)": "Cozinha Caseira (próximo à Central de Aulas)",
        "Off-Campus (Bancários Neighborhood)": "Fora do Campus (Bairro dos Bancários)",

        # =====================================================================
        # == Accommodation Page (accommodation/index.html)
        # =====================================================================
        "Accommodation in João Pessoa": "Hospedagem em João Pessoa",
        "Find a comfortable place to stay during the conference.": "Encontre um lugar confortável para ficar durante a conferência.",
        "We recommend that hotel reservations be made": "Recomendamos que as reservas de hotel sejam feitas",
        "after your registration is confirmed": "após a confirmação da sua inscrição",
        "to ensure negotiated rates and better prices. The city is a tourist destination and the event period coincides with the high holiday season, so we suggest that reservations be made in advance to ensure availability at the hotels of your choice.": "para garantir tarifas negociadas e melhores preços. A cidade é um destino turístico e o período do evento coincide com a alta temporada de férias, por isso sugerimos que as reservas sejam feitas com antecedência para garantir a disponibilidade nos hotéis de sua escolha.",
        "The conference organizers do not have block bookings with these hotels unless specified. Please book directly with the hotel or through your preferred booking platform. Mentioning BRICS-AGAC 2025 *might* provide a conference rate at some establishments, but this is not guaranteed.": "Os organizadores da conferência não possuem bloqueios de quartos com esses hotéis, a menos que especificado. Por favor, reserve diretamente com o hotel ou através de sua plataforma de reserva preferida. Mencionar BRICS-AGAC 2025 *pode* fornecer uma tarifa de conferência em alguns estabelecimentos, mas isso não é garantido.",
        "Rates (daily):": "Diárias:",
        "Notes:": "Observações:",
        "Ask for Evellyn for the negotiated rate.": "Pergunte por Evellyn pela tarifa negociada.",
        "Mention the event and the negotiated rate.": "Mencione o evento e a tarifa negociada.",
        "Mention the hotel and city when booking.": "Mencione o hotel e a cidade ao reservar.",
        "Additional Tips for Booking": "Dicas Adicionais para Reserva",
        "Consider proximity to the conference venue and public transport.": "Considere a proximidade com o local da conferência e o transporte público.",
        "Check reviews on platforms like Booking.com, TripAdvisor, or Google Maps.": "Verifique as avaliações em plataformas como Booking.com, TripAdvisor ou Google Maps.",
        "Look for amenities that are important to you (e.g., Wi-Fi, breakfast included, gym).": "Procure por comodidades que são importantes para você (ex: Wi-Fi, café da manhã incluso, academia).",
        "Airbnb and other short-term rental options are also available in João Pessoa.": "Airbnb e outras opções de aluguel de curto prazo também estão disponíveis em João Pessoa.",
        "For specific accommodation for invited speakers and committee members, arrangements will be communicated directly by the LOC.": "Para hospedagem específica para palestrantes convidados e membros do comitê, os arranjos serão comunicados diretamente pelo LOC.",

        # =====================================================================
        # == Explore João Pessoa Page (explore-joao-pessoa/index.html)
        # =====================================================================
        "Discover the charms of Paraíba's capital during your stay.": "Descubra os encantos da capital da Paraíba durante a sua estadia.",
        "Make the most of your visit to João Pessoa by exploring its beautiful sights, rich culture, and delicious cuisine. Here are a few recommendations:": "Aproveite ao máximo sua visita a João Pessoa explorando suas belas paisagens, rica cultura e culinária deliciosa. Aqui estão algumas recomendações:",
        "Tambaú Beach (Praia de Tambaú)": "Praia de Tambaú",
        "One of the city's main urban beaches, bustling with activity, beachfront restaurants, and artisan shops. Perfect for a stroll or enjoying fresh coconut water.": "Uma das principais praias urbanas da cidade, movimentada com atividades, restaurantes à beira-mar e lojas de artesanato. Perfeita para um passeio ou para desfrutar de uma água de coco fresca.",
        "Cabo Branco Lighthouse (Farol do Cabo Branco)": "Farol do Cabo Branco",
        "An iconic lighthouse marking the easternmost point of continental Brazil (before Ponta do Seixas). Offers panoramic views of the coastline.": "Um farol icônico que marca o ponto mais oriental do Brasil continental (antes da Ponta do Seixas). Oferece vistas panorâmicas da costa.",
        "Ponta do Seixas": "Ponta do Seixas",
        "The true easternmost point of the Americas. Visit at sunrise to be among the first to see the sun on the continent. Nearby natural pools (Piscinas Naturais do Seixas) are accessible at low tide.": "O verdadeiro ponto mais oriental das Américas. Visite ao nascer do sol para estar entre os primeiros a ver o sol no continente. As piscinas naturais do Seixas, nas proximidades, são acessíveis na maré baixa.",
        "Historic Center (Centro Histórico)": "Centro Histórico",
        "Explore colonial architecture, including the São Francisco Cultural Center (a baroque masterpiece), churches, and charming squares like Praça Antenor Navarro.": "Explore a arquitetura colonial, incluindo o Centro Cultural São Francisco (uma obra-prima barroca), igrejas e praças charmosas como a Praça Antenor Navarro.",
        "Estação Cabo Branco – Ciência, Cultura e Artes": "Estação Cabo Branco – Ciência, Cultura e Artes",
        "A cultural complex designed by Oscar Niemeyer, featuring exhibitions on science, art, and technology, plus an observation tower with stunning city views.": "Um complexo cultural projetado por Oscar Niemeyer, com exposições sobre ciência, arte e tecnologia, além de uma torre de observação com vistas deslumbrantes da cidade.",
        "Areia Vermelha Island": "Ilha de Areia Vermelha",
        "A temporary sandbar island that appears at low tide, accessible by boat. Offers clear waters for swimming and snorkeling. A popular day trip.": "Uma ilha de areia temporária que aparece na maré baixa, acessível por barco. Oferece águas claras para nadar e mergulhar. Um passeio de um dia popular.",
        "Local Cuisine & Culture": "Culinária e Cultura Local",
        "Don't miss trying Paraíba's local cuisine! Sample dishes like \"carne de sol com macaxeira\" (sun-dried beef with cassava), fresh seafood, and tropical fruit juices. The region is also known for its vibrant Forró music and dance, and rich handicraft traditions.": "Não deixe de experimentar a culinária local da Paraíba! Prove pratos como \"carne de sol com macaxeira\", frutos do mar frescos e sucos de frutas tropicais. A região também é conhecida por sua vibrante música e dança de Forró, e ricas tradições de artesanato.",
        "[Placeholder for more specific tips on restaurants or cultural experiences. E.g., \"Visit the Mercado de Artesanato Paraibano for local crafts.\"]": "[Espaço para dicas mais específicas sobre restaurantes ou experiências culturais. Ex: \"Visite o Mercado de Artesanato Paraibano para artesanato local.\"]",

        # =====================================================================
        # == BINGO Program Page (bingo-program/index.html)
        # =====================================================================
        "Exclusive tour to the BINGO Telescope.": "Tour exclusivo para o Telescópio BINGO.",
        "Technical Tour: BINGO Telescope": "Visita Técnica: Telescópio BINGO",
        "Join us for an exclusive two-day technical tour to the BINGO Telescope construction site in Aguiar, located in the hinterlands of Paraíba. This is a unique opportunity to witness the development of a next-generation instrument in global cosmology.": "Junte-se a nós para uma visita técnica exclusiva de dois dias ao local de construção do Telescópio BINGO em Aguiar, localizado no sertão da Paraíba. Esta é uma oportunidade única para testemunhar o desenvolvimento de um instrumento de próxima geração na cosmologia global.",
        "Please note: The technical visit to the BINGO telescope is exclusively for registered event participants and is not open to the general public.": "Atenção: A visita técnica ao telescópio BINGO é exclusiva para os participantes inscritos no evento e não é aberta ao público em geral.",
        "Transportation": "Transporte",
        "Round Trip Bus": "Ônibus de Ida e Volta",
        "Per person": "Por pessoa",
        "A 50-seat bus will be provided. Seats are limited and allocated on a first-come, first-served basis. If demand exceeds capacity, the organization will consider arranging additional transport.": "Será disponibilizado um ônibus de 50 lugares. Os assentos são limitados e alocados por ordem de chegada. Se a procura exceder a capacidade, a organização considerará a possibilidade de providenciar transporte adicional.",
        "Accommodation in Sousa": "Hospedagem em Sousa",
        "Please note that accommodation in the nearby city of Sousa is the responsibility of each participant. The organization suggests the following hotels:": "Informamos que a hospedagem na cidade vizinha de Sousa é de responsabilidade de cada participante. A organização sugere os seguintes hotéis:",
        "A unique dinosaur-themed hotel.": "Um hotel único com tema de dinossauros.",
        "Room Type": "Tipo de Quarto",
        "Rate": "Tarifa",
        "Individual": "Individual",
        "Double": "Duplo",
        "Triple": "Triplo",
        "Quadruple": "Quádruplo",
        "Master Suite": "Suíte Master",
        "Luxury": "Luxo",
        "Deluxe Individual": "Deluxe Individual",
        "Deluxe Double": "Deluxe Duplo",
        "Another excellent accommodation option.": "Outra excelente opção de hospedagem.",
        "Double/Couple": "Duplo/Casal",
        "Payment & Instructions for the Round Trip Bus (R$ 150.00)": "Pagamento e Instruções para o Ônibus de Ida e Volta (R$ 150,00)",
        "Bank Transfer": "Transferência Bancária",
        "Bank:": "Banco:",
        "Agency:": "Agência:",
        "Account:": "Conta:",
        "Name:": "Nome:",
        "This is a payment account. If a CPF/CNPJ (Brazilian tax ID) is requested, you may proceed without entering it.": "Esta é uma conta de pagamento. Se um CPF/CNPJ for solicitado, você pode prosseguir sem inseri-lo.",
        "PIX (Brazil Only)": "PIX (Apenas Brasil)",
        "Key Type:": "Tipo de Chave:",
        "PIX Key:": "Chave PIX:",
        "E-mail": "E-mail",
        "Mandatory Steps After Payment": "Passos Obrigatórios Após o Pagamento",
        "To confirm your participation in the BINGO technical visit, please follow these steps carefully:": "Para confirmar sua participação na visita técnica do BINGO, por favor, siga estes passos cuidadosamente:",
        "Send Proof of Payment:": "Envie o Comprovante de Pagamento:",
        "After payment, you **must** email the receipt to": "Após o pagamento, você **deve** enviar o recibo por email para",
        "Specify Email Subject:": "Especifique o Assunto do Email:",
        "Use the subject line: \"BINGO Visit Payment - [Your Full Name]\".": "Use a linha de assunto: \"Pagamento Visita BINGO - [Seu Nome Completo]\".",
        "Await Confirmation:": "Aguarde a Confirmação:",
        "Your participation is only guaranteed after our team verifies your payment. A confirmation email will be sent to you.": "Sua participação só é garantida após nossa equipe verificar seu pagamento. Um email de confirmação será enviado a você.",
        "Note: This payment is for the round trip bus to the BINGO Telescope. Accommodation is not included.": "Nota: Este pagamento é para o ônibus de ida e volta para o Telescópio BINGO. A hospedagem não está incluída.",

        # =====================================================================
        # == Contact Page (contact/index.html)
        # =====================================================================
        "We're here to help with your inquiries about BRICS-AGAC 2025.": "Estamos aqui para ajudar com suas dúvidas sobre o BRICS-AGAC 2025.",
        "Email Contacts": "Contatos de Email",
        "For specific inquiries, please use the appropriate email address below:": "Para dúvidas específicas, por favor, use o endereço de email apropriado abaixo:",
        "Primary Contact for General Inquiries:": "Contato Principal para Dúvidas Gerais:",
        "Send us a Message": "Envie-nos uma Mensagem",
        "Alternatively, you can use the form below for general questions.": "Alternativamente, você pode usar o formulário abaixo para perguntas gerais.",
        "Your Name": "Seu Nome",
        "Your Email": "Seu Email",
        "Subject": "Assunto",
        "Message": "Mensagem",
        "Send Message": "Enviar Mensagem",

        # =====================================================================
        # == Shirts Page (shirts/index.html)
        # =====================================================================
        "Order Your BRICS-AGAC 2025 Souvenir Shirts": "Encomende Suas Camisetas de Lembrança do BRICS-AGAC 2025",
        "The Official BRICS-AGAC 2025 Shirt": "A Camiseta Oficial do BRICS-AGAC 2025",
        "Front View": "Vista Frontal",
        "Back View": "Vista Traseira",
        "Place Your Order": "Faça Seu Pedido",
        "Select your desired models and sizes below. You must provide your name, email, and select at least one shirt to submit the form.": "Selecione seus modelos e tamanhos desejados abaixo. Você deve fornecer seu nome, e-mail e selecionar pelo menos uma camiseta para enviar o formulário.",
        "Measurements are taken as shown: (A) Width and (B) Height.": "As medidas são tiradas como mostrado: (A) Largura e (B) Altura.",
        "Enter your full name": "Digite seu nome completo",
        "example@email.com": "exemplo@email.com",
        "A classic-fit t-shirt for all-day comfort.": "Uma camiseta de corte clássico para conforto o dia todo.",
        "Size": "Tamanho",
        "Width (A)": "Largura (A)",
        "Height (B)": "Altura (B)",
        "Qty": "Qtd",
        "P (Small)": "P (Pequeno)",
        "M (Medium)": "M (Médio)",
        "G (Large)": "G (Grande)",
        "GG (XL)": "GG (GG)",
        "XGG (XXL)": "XGG (XGG)",
        "Baby Look (Fitted)": "Baby Look (Justa)",
        "A stylish, fitted t-shirt for a more modern look.": "Uma camiseta elegante e justa para um visual mais moderno.",
        "Kids T-Shirt": "Camiseta Infantil",
        "Comfortable and durable, perfect for young attendees.": "Confortável e durável, perfeita para os jovens participantes.",
        "2 Years": "2 Anos",
        "4 Years": "4 Anos",
        "6 Years": "6 Anos",
        "8 Years": "8 Anos",
        "10 Years": "10 Anos",
        "12 Years": "12 Anos",
        "Payment & Instructions": "Pagamento e Instruções",
        "To confirm your t-shirt order, please follow these steps carefully:": "Para confirmar seu pedido de camiseta, por favor, siga estes passos cuidadosamente:",
        "Use the subject line: \"T-Shirt Payment - [Your Full Name]\".": "Use a linha de assunto: \"Pagamento Camiseta - [Seu Nome Completo]\".",
        "T-Shirt Delivery": "Entrega da Camiseta",
        "The delivery method for the t-shirts will be decided by the event organization. All buyers will be informed about the delivery details later via the contact email provided in the order form.": "O método de entrega das camisetas será decidido pela organização do evento. Todos os compradores serão informados sobre os detalhes da entrega posteriormente através do e-mail de contato fornecido no formulário de pedido.",
        "Submit My Choices & Proceed to Payment": "Enviar Minhas Escolhas e Prosseguir para o Pagamento",
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
