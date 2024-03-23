# Importando as bibliotecas necessárias
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

# Esta função é usada para autenticar o cliente do Azure Text Analytics
def authenticate_client():
    # Recuperando a chave e o endpoint do Azure Text Analytics das variáveis de ambiente
    ta_key = os.getenv("AZURE_LANGUAGE_KEY")
    ta_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    
    # Criando uma instância de AzureKeyCredential com a chave recuperada
    ta_credential = AzureKeyCredential(ta_key)
    
    # Criando uma instância de TextAnalyticsClient com o endpoint e a credencial
    text_analytics_client = TextAnalyticsClient(
            endpoint=ta_endpoint,
            credential=ta_credential)
    
    # Retornando o cliente autenticado
    return text_analytics_client

# Esta função é usada para analisar o texto usando o cliente do Azure Text Analytics
def analyze_text(client: TextAnalyticsClient, documents: list):
    # Mapeando os sentimentos em inglês para português
    sentiment_map = {"positive": "positivo", "neutral": "neutro", "negative": "negativo"}
    
    # Inicializando a lista de resultados
    result = []
    
    # Processando os documentos em lotes de 10
    for i in range(0, len(documents), 10):
        # Criando um lote com até 10 documentos
        batch = [doc for doc in documents[i:i+10] if doc.strip()]
        
        # Se o lote não estiver vazio
        if batch:
            # Analisando o sentimento dos documentos no lote
            response = client.analyze_sentiment(documents=batch)
            
            # Extraindo as principais frases dos documentos no lote
            key_phrases_response = client.extract_key_phrases(documents=batch)
            
            # Para cada documento e suas principais frases
            for doc, key_phrases in zip(response, key_phrases_response):
                # Se não houve erro na análise do documento
                if not doc.is_error:
                    # Traduzindo o sentimento para português
                    sentiment = sentiment_map.get(doc.sentiment, doc.sentiment)
                    
                    # Adicionando o sentimento do documento ao resultado
                    result.append("Sentimento do Documento: {}".format(sentiment))
                    
                    # Adicionando as pontuações de confiança ao resultado
                    result.append("Pontuações gerais: positivo={0:.2f}; neutro={1:.2f}; negativo={2:.2f} \n".format(
                        doc.confidence_scores.positive,
                        doc.confidence_scores.neutral,
                        doc.confidence_scores.negative,
                    ))
                    
                    # Adicionando as principais frases ao resultado
                    result.append("Principais frases: {}".format(", ".join(key_phrases.key_phrases)))
                else:
                    # Adicionando o erro ao resultado
                    result.append("Erro no documento: {}".format(doc.error))
    
    # Retornando o resultado
    return result
def main(filename):
    # Autenticando o cliente
    client = authenticate_client()
    
    # Verifica se existe um arquivo de análise correspondente
    if os.path.exists(f'inputs/analise_{filename}'):
        print(f"Análise de texto para {filename} já foi realizada.")
        return

    print(f"Processando análise de texto para {filename}...")
    
    # Abrindo o arquivo para leitura
    with open(os.path.join('inputs', filename), 'r', encoding='utf-8') as file:
        # Lendo o texto do arquivo
        text = file.read()
    
    comments = text.split('---\n')
    
    # Abrindo um novo arquivo para escrita
    with open(os.path.join('inputs', 'analise_' + filename), 'w', encoding='utf-8') as file:
        # Para cada comentário
        for comment in comments:
            # Se o comentário não estiver vazio
            if comment.strip():
                # Analisando o comentário
                result = analyze_text(client, [comment])
                
                # Escrevendo o comentário original no arquivo
                file.write(comment)
                
                # Escrevendo a análise no arquivo
                file.write('\n'.join(result))
                file.write('\n---\n')

# Chamando a função principal
if __name__ == "__main__":
    main()