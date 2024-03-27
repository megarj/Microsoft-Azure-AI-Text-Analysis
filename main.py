from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import text_analysis

def save_reviews(company):
    # Inicia o webdriver
    driver = webdriver.Chrome()

    # Acessa a página de pesquisa do Google
    driver.get(f"https://www.google.com/search?q={company} reviews")

    # Aguarda até que o elemento com a class 'gws-localreviews__general-reviews-block' esteja visível
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'gws-localreviews__general-reviews-block')))

    # Encontra todos os elementos com a class 'Jtu6Td'
    reviews = driver.find_elements_by_class_name('Jtu6Td')

    # Abre um novo arquivo para escrita
    with open(f"inputs/{company}_reviews.txt", 'w', encoding='utf-8') as file:
        # Para cada review
        for review in reviews:
            # Escreve o texto do review no arquivo
            file.write(review.text)
            file.write('\n---\n')

    # Fecha o webdriver
    driver.quit()

def process_input_files():
    # Lista todos os arquivos na pasta 'inputs'
    input_files = os.listdir('inputs')

    # Para cada arquivo na pasta 'inputs'
    for file in input_files:
        # Remove a extensão do nome do arquivo
        base_name = os.path.splitext(file)[0]

        # Verifica se o arquivo não começa com 'analise_'
        if not base_name.startswith('analise_'):
            # Verifica se existe um arquivo correspondente na pasta 'inputs'
            if not os.path.exists(f'inputs/analise_{base_name}.txt'):
                try:
                    # Se não, executa a análise de texto
                    text_analysis.main(base_name + '.txt')
                except Exception as e:
                    # Se ocorrer um erro ao realizar a análise de texto, imprime uma mensagem com o motivo do erro
                    print(f"Falha ao realizar análise de texto para {base_name}. Motivo: {str(e)}")
                    return False
    return True

# Pergunta ao usuário se ele quer inserir nomes de empresas ou se já adicionou os arquivos txt manualmente
option = input("Você quer inserir nomes de empresas (digite 1) ou já adicionou os arquivos txt manualmente (digite 2)? ")

if option == '1':
    # Se o usuário escolher inserir nomes de empresas, pergunte quais empresas ele quer pesquisar
    companies = input("Por favor, insira os nomes das empresas que você quer pesquisar, separados por vírgula: ").split(',')

    # Para cada empresa na lista
    for company in companies:
        # Removendo espaços em branco no início e no fim do nome da empresa
        # Convertendo o nome da empresa para minúsculas
        # Removendo caracteres especiais do nome da empresa
        company = re.sub(r'\W+', '', company.strip().lower())

        # Verificando se o arquivo de análise já existe
        if os.path.exists(f"inputs/analise_{company}_reviews.txt"):
            # Perguntando ao usuário se ele quer sobrescrever o arquivo com uma nova análise
            overwrite = input(f"A análise para a empresa {company} já existe. Você quer sobrescrever com uma nova análise? (s/n): ")
            if overwrite.lower() != 's':
                exit()

        # Criando um objeto Service
        # O objeto Service é usado para interagir com o driver do navegador
        # Neste caso, estamos usando o ChromeDriverManager para gerenciar o driver do Chrome
        service = Service(ChromeDriverManager().install())

        # Passando o objeto Service para webdriver.Chrome
        # Isso cria uma nova instância do navegador Chrome
        # O navegador será controlado pelo script Python através do driver
        driver = webdriver.Chrome(service=service)

        # Navegando para a página de pesquisa do Google
        driver.get(f"https://www.google.com/search?q={company}")

        try:
            # Clicando no botão "Ver todas as avaliações do Google"
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-async-trigger="reviewDialog"]'))
            )
            button.click()
        except:
            # Se a empresa não tiver uma página do Google Meu Negócio ou avaliações, imprime uma mensagem e pula para a próxima empresa
            print(f"A empresa {company} não possui Google Meu Negócio ou avaliações.")
            continue

        # Aguardando as avaliações serem carregadas
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.jxjCjc'))
        )

        try:
            # Encontrando todos os botões "Mais" e executando o click
            more_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.review-more-link'))
            )
            for button in more_buttons:
                if button.is_displayed():  # Verifica se o botão está visível
                    button.click()

            # Obtendo as avaliações
            reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.jxjCjc'))
            )
            # Abrindo um arquivo para escrita
            with open(f"inputs/{company}_reviews.txt", "w", encoding="utf8") as f:
                for review in reviews:
                    # Obtendo o texto da avaliação
                    text = review.text
                    # Escrevendo o texto da avaliação no arquivo
                    f.write(text + "\n\n")
                    f.write('---\n')
            # Imprimindo uma mensagem para informar que as avaliações foram salvas com sucesso
            print(f"Avaliações salvas com sucesso para {company}.")
        except Exception as e:
            # Se ocorrer um erro ao salvar as avaliações, imprime uma mensagem com o motivo do erro
            print(f"Falha ao salvar avaliações para {company}. Motivo: {str(e)}")

    # Fechando o navegador
    driver.quit()

    # Se o usuário escolher para baixar as avaliações atuais.
    if process_input_files():
        # Imprimindo uma mensagem para informar que todas as análises de texto foram concluídas
        print("Todas as análises baixadas foram realizadas com sucesso.")


elif option == '2':
    # Se o usuário escolher que já adicionou os arquivos txt manualmente, chama a função process_input_files
    if process_input_files():
        # Imprimindo uma mensagem para informar que todas as análises de texto foram concluídas
        print("Todas as análises de texto em inputs foram realizadas com sucesso.")