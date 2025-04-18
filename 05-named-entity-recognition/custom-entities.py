from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
# import namespaces


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        project_name = os.getenv('PROJECT')
        deployment_name = os.getenv('DEPLOYMENT')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        text_client = TextAnalyticsClient(ai_endpoint, credential)

        # Read each text file in the ads folder
        batchedDocuments = []
        ads_folder = 'ads'
        files = os.listdir(ads_folder)
        for file_name in files:
            # Read the file contents
            text = open(os.path.join(ads_folder, file_name), encoding='utf8').read()
            batchedDocuments.append(text)

        # Extract entities
        operation = text_client.begin_recognize_custom_entities(
            documents=batchedDocuments,
            project_name=project_name,
            deployment_name=deployment_name
        )
        document_results = operation.result()

        for doc, entity_results in zip(files, document_results):
            if entity_results.kind == "CustomEntityRecognition":
                for entity in entity_results.entities:
                    print(f"\nEntity {entity.text} has category {entity.category} with confidence score of {entity.confidence_score}")
            elif entity_results.error is True:
                print(f"\t Error with code {entity_results.error.code} and message {entity_results.error.message}")


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()