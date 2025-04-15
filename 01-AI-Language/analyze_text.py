from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        ai_key = os.getenv("AI_SERVICE_KEY")

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_lang_client = TextAnalyticsClient(ai_endpoint, credential)


        # Analyze each text file in the reviews folder
        reviews_folder = "reviews"
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print("\n-------------\n" + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print("\n" + text)

            # Get language
            language = ai_lang_client.detect_language(documents=[text])[0]
            print("\nLanguage: {}".format(language.primary_language.name))
            print("\nScore: {}".format(language.primary_language.confidence_score))

            # Get sentiment
            sentiment = ai_lang_client.analyze_sentiment(documents=[text])[0]
            print("\nSentiment: {}".format(sentiment.sentiment))
            print("\nPositive Score: {}".format(sentiment.confidence_scores.positive))
            print("\nNegative Score: {}".format(sentiment.confidence_scores.negative))
            print("\nNeutral Score: {}".format(sentiment.confidence_scores.neutral))

            # Get key phrases
            key_phrase_list= ai_lang_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(key_phrase_list) > 0:
                print("\nKey Phrases:")
                for phrase in key_phrase_list:
                    print("\t{}".format(phrase))

            # Get entities
            entities_detect = ai_lang_client.recognize_entities(documents=[text])[0]
            entities_list = entities_detect.entities
            print("\nCount of Entities: {}".format(len(entities_list)))
            for entity in entities_list:
                print(f"Text:{entity.text}; category: {entity.category}")

            # Get PII entities
            pii_entities_detect = ai_lang_client.recognize_pii_entities(documents=[text])[0]
            pii_entities_list = pii_entities_detect.entities
            print("\nCount of PII Entities: {}".format(len(pii_entities_list)))
            if len(pii_entities_list) >0 :
                for pii_entity in pii_entities_list:
                    print(f"Text: {pii_entity.text}; category: {pii_entity.category}")

            # Get linked entities
            linked_entities_list = ai_lang_client.recognize_linked_entities(documents=[text])[0].entities
            if len(linked_entities_list) > 0:
                print("\nLinked Entities:")
                for linked_entity in linked_entities_list:
                    print(f"{linked_entity.name} -- {linked_entity.url}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()