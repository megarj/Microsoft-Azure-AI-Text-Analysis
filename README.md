<img src="https://hermes.dio.me/lab_projects/badges/dc92e499-6ec6-4c82-af3f-00c40538ca80.png" alt="Trabalhando com Análise de Texto na AZURE AI Text Analytics" width="200">

---
# Análise de Sentimentos com Azure AI Text Analytics

Este script Python exemplifica a utilização do serviço Azure AI Text Analytics para analisar o sentimento de avaliações do Google para uma lista de empresas fornecida pelo usuário.

⚠️ **Atenção**: Ao final dos seus testes não se esqueça de apagar os recursos ⚠️

[🧹Não sabe como apagar? 👉 Veja aqui](https://learn.microsoft.com/pt-pt/azure/ai-services/multi-service-resource?pivots=azportal&tabs=windows#clean-up-resources)

## 🔗 Links de Referência

[📝Documentação Azure AI Text Analytics](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&viewFallbackFrom=azure-python-preview&preserve-view=true)

[😺 Repositorio GIT azure-sdk-for-python com exemplos](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/textanalytics/azure-ai-textanalytics/samples)

## Índice

1. [Requisitos](#requisitos)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Como Usar](#como-usar)
4. [Exemplo de Uso](#exemplo-de-uso) 
5. [Recursos do Azure Text Analytics](#recursos-do-azure-text-analytics)
6. [Licença](#licença)

## Requisitos

- Python 3.x
- Conta no Azure com o serviço Text Analytics habilitado  [Não tem? 👉 Crie aqui sua conta Gratuita](https://azure.microsoft.com/pt-pt/free/)
- Chave e Endpoint da API [Não tem? 👉 Veja aqui](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#get-the-api-key)

## Instalação e Configuração

1. Configure as variáveis de ambiente com o endpoint e a chave da API do Azure Text Analytics:
   
   Para usuários do Linux:

   ```bash
   export TEXT_ANALYTICS_ENDPOINT=<seu_endpoint>
   export TEXT_ANALYTICS_KEY=<sua_chave>

 Para usuários do Windows:

   - Abra o menu Iniciar e pesquise por "Variáveis de ambiente".
   - Clique em "Editar variáveis de ambiente do sistema".
   - Na janela de Propriedades do sistema, clique no botão "Variáveis de ambiente".
   - Na seção "Variáveis do sistema", clique em "Novo..." para adicionar uma nova variável.
   - Em "Nome da variável", insira `TEXT_ANALYTICS_ENDPOINT`.
   - Em "Valor da variável", insira o endpoint do Azure Vision.
   - Repita as etapas anteriores para adicionar a chave da API, utilizando `TEXT_ANALYTICS_KEY` como nome da variável e sua chave como valor.
   - Clique em "OK" para fechar todas as janelas de configuração.


⚠️ **Atenção**: Nunca exponha sua key ou endpoint diretamente no código ⚠️

⚠️ **Atenção**: Se estiver com o terminal aberto terá de reiniciá-lo para que entenda as novas variáveis de ambiente ⚠️


2. Clone este repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/megarj/Microsoft-Azure-AI-Text-Analysis.git
   ```

3. Navegue até o diretório do projeto:

   ```bash
   cd Microsoft-Azure-AI-Text-Analysis
   ```

4. Crie e ative um ambiente virtual Python:
   
    ### Windows:
    ```bash
    python -m venv escolha-nome-ambiente
    escolha-nome-ambiente\Scripts\activate
    ```
    ### Linux:
    ```bash
    python -m venv escolha-nome-ambiente
    source escolha-nome-ambiente/bin/activate
    ```

Essas instruções criam e ativam um ambiente virtual Python no respectivo sistema operacional. Certifique-se de substituir `escolha-nome-ambiente` pelo nome desejado para o seu ambiente virtual.

5. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

6. **Navegador Web:** Este projeto usa o Selenium para automatizar um navegador web. Por padrão, usamos o Google Chrome, mas você pode alterar para qualquer navegador suportado pelo Selenium. Os navegadores suportados pelo Selenium incluem Google Chrome, Firefox, Safari, Edge, entre outros. Certifique-se de ter o navegador de sua escolha instalado em seu computador. Você pode baixar o Google Chrome do [site oficial do Google Chrome](https://www.google.com/chrome/). Se você optar por usar um navegador diferente, certifique-se de atualizar o código e o driver do navegador conforme necessário.

## Como Usar

Este projeto pode ser usado de duas maneiras:

1. **Se você quer coletar avaliações do Google e analisá-las:** Execute o seguinte comando:

   ```bash
   python main.py
   ```

   **Digite a opção 1**   
   Quando solicitado, digite uma lista de empresas para pesquisar, separadas por vírgulas. O script irá coletar as avaliações do Google Meu Negócio para cada empresa, salvar as avaliações apenas da primeira página aberta para fins de testes em arquivos de texto na pasta `inputs`, analisar as avaliações e salvar os resultados da análise em novos arquivos com o prefixo `analise_`.

2. **Se você já tem o texto a ser analisado:** Coloque o arquivo de texto (ou arquivos, se tiver mais de um) na pasta `inputs` e execute o seguinte comando:

   ```bash
   python main.py
   ```

   **Digite a opção 2**   
   Isso irá analisar o texto e salvar um novo arquivo em `inputs` com o prefixo `analise_` seguido pelo nome do arquivo de texto original. Por exemplo, se o arquivo de texto original se chama `meu_texto.txt`, o arquivo de análise será `analise_meu_texto.txt`.

⚠️ **Atenção**: Este script serve apenas para facilitar os testes. Para produção, deve ser utilizada a API oficial do Google. Mais informações podem ser encontradas na [documentação oficial da API Google My Business](https://developers.google.com/my-business/content/overview?hl=pt-br).

## Exemplo de Uso

Aqui está um exemplo de como um texto é analisado usando este projeto. 

### Texto Original
```
Vinicius Viana
Local Guide·130 comentários·544 fotos
5 dias atrás
NOVA
É uma parada obrigatória quando se fala em turismo no centro histórico de São Paulo. Achei o ambiente bem legal, muita coisa interessante. Os estúdios de tatuagem e body piercing transmitem segurança, qualidade e preço justo. Super recomendo a visita.
```	
###  Texto Analisado
```
Vinicius Viana
Local Guide·130 comentários·544 fotos
5 dias atrás
NOVA
É uma parada obrigatória quando se fala em turismo no centro histórico de São Paulo. Achei o ambiente bem legal, muita coisa interessante. Os estúdios de tatuagem e body piercing transmitem segurança, qualidade e preço justo. Super recomendo a visita.

Sentimento do Documento: positivo
Pontuações gerais: positivo=0.84; neutro=0.16; negativo=0.01 

Principais frases: centro histórico, São Paulo, preço, Vinicius Viana, Local Guide, comentários, estúdios, body piercing, segurança, 544 fotos, NOVA, parada, turismo, ambiente, coisa, tatuagem, qualidade, visita
```
## Recursos do Azure Text Analytics

| Recurso                               | Descrição                                                                 |
|---------------------------------------|---------------------------------------------------------------------------|
| [Análise de Sentimento](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#analyze-sentiment)                     | Analisa o sentimento do texto.                                            |
| [Reconher Entidades](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#recognize-entities)                    | Reconhece e categoriza entidades no texto.                                |
| [Reconhecer Entidades Vinculadas](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#recognize-linked-entities)                    | Reconhece e desambigua a identidade de cada entidade(por exemplo, determinar se a ocorrência Marte se refere ao planeta ou ao Deus romano da guerra)                                |
| [Reconhecer entidades PII](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#recognize-pii-entities)                    | Reconhece e categoriza entidades de PII (Informações de Identificação Pessoal) em seu texto de entrada, como Números da Previdência Social, informações de conta bancária, números de cartão de crédito e muito mais                                |
| [Extrair frases-chave](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#extract-key-phrases)                       | Determina os pontos de discussão main em seu texto de entrada. Por exemplo, para o texto de entrada "A comida estava deliciosa e havia uma equipe maravilhosa", a API retorna: "comida" e "equipe maravilhosa".                                      |
| [Detectar o idioma](https://learn.microsoft.com/pt-br/python/api/azure-ai-textanalytics/azure.ai.textanalytics.TextAnalyticsClient?view=azure-python#extract-key-phrases-documents--language-none----kwargs-)                   | Determina o idioma de seu texto de entrada, incluindo a pontuação de confiança do idioma previsto.            |
| [Análise de entidades de saúde](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#healthcare-entities-analysis)             |Extrai entidades reconhecidas dentro do domínio de saúde e identifica relações entre entidades dentro do documento de entrada e links para fontes de informações conhecidas em vários bancos de dados conhecidos, como UMLS, CHV, MSH etc.            |
| [Análise múltipla](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#multiple-analysis)                     |Executa várias análises em um conjunto de documentos em uma única solicitação.                               |
| [Reconhecimento de Entidade Personalizada](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_recognize_custom_entities.py)             | Reconhece entidades personalizadas no texto.                              |
| [Classificação personalizada de rótulo único](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_single_label_classify.py)    | Classifica o texto em uma única categoria personalizada.                  |
| [Classificação de vários rótulos personalizados](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_multi_label_classify.py)    | Classifica o texto em várias categorias personalizadas. Por exemplo, resumos de filmes podem ser categorizados em vários gêneros de filmes como "Ação", "Comédia" ou "Drama", etc.                  |
| [Resumo extrativo](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_extract_summary.py)              | Extrai as frases mais relevantes do texto.                                |
| [Resumo abstrativo](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.3.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_abstract_summary.py)             | Gera um resumo abstrato do texto.                                         |

> Para mais exemplos de como utilizar esses recursos, consulte a [documentação oficial da API Azure Text Analytics](https://learn.microsoft.com/pt-br/python/api/overview/azure/ai-textanalytics-readme?view=azure-python&preserve-view=true#get-the-api-key).

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

Gostou, achou útil? Considere dar uma estrela 😉

[![Estrelas](https://img.shields.io/github/stars/megarj/Microsoft-Azure-AI-Text-Analysis.svg)](https://github.com/megarj/Microsoft-Azure-AI-Text-Analysis.git)