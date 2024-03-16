from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

def authenticate_client():
    ta_key = os.getenv("AZURE_LANGUAGE_KEY")
    ta_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    ta_credential = AzureKeyCredential(ta_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=ta_endpoint,
            credential=ta_credential)
    return text_analytics_client

def analyze_text(client, documents):
    sentiment_map = {
        'positive': 'positivo',
        'neutral': 'neutro',
        'negative': 'negativo',
    }
    result = []
    for i in range(0, len(documents), 10):
        batch = [doc for doc in documents[i:i+10] if doc.strip()]
        if batch:
            response = client.analyze_sentiment(documents=batch)
            for doc in response:
                if not doc.is_error:
                    sentiment = sentiment_map.get(doc.sentiment, doc.sentiment)
                    result.append("Sentimento do Documento: {}".format(sentiment))
                    result.append("Pontuações gerais: positivo={0:.2f}; neutro={1:.2f}; negativo={2:.2f} \n".format(
                        doc.confidence_scores.positive,
                        doc.confidence_scores.neutral,
                        doc.confidence_scores.negative,
                    ))
                else:
                    result.append("Erro no documento: {}".format(doc.error))
    return result

def main():
    client = authenticate_client()
    for filename in os.listdir('inputs'):
        if filename.endswith('.txt'):
            with open(os.path.join('inputs', filename), 'r', encoding='utf-8') as file:
                text = file.read()
            comments = text.split('---\n')
            with open(os.path.join('inputs', 'analise_' + filename), 'w', encoding='utf-8') as file:
                for comment in comments:
                    if comment.strip():
                        result = analyze_text(client, [comment])
                        file.write(comment)  # Write the original comment
                        file.write('\n'.join(result))  # Write the analysis
                        file.write('\n---\n')

if __name__ == "__main__":
    main()