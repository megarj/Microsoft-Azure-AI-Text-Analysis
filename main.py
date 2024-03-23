# Importando as bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import text_analysis
import os
import re

# Solicitando ao usuário uma lista de nomes de empresas para pesquisa
# A entrada deve ser uma lista de nomes de empresas separadas por vírgulas
companies = input("Digite uma lista de empresas para pesquisar, separadas por vírgulas: ").split(',')

# Criando um objeto Service
# O objeto Service é usado para interagir com o driver do navegador
# Neste caso, estamos usando o ChromeDriverManager para gerenciar o driver do Chrome
service = Service(ChromeDriverManager().install())

# Passando o objeto Service para webdriver.Chrome
# Isso cria uma nova instância do navegador Chrome
# O navegador será controlado pelo script Python através do driver
driver = webdriver.Chrome(service=service)

# Iterando através da lista de empresas
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
            continue

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
        # Encontrando todos os botões "Mais" e clicando neles
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

# Imprimindo uma mensagem para informar que todas as análises de texto foram concluídas
print("Todas as análises de texto foram concluídas.")