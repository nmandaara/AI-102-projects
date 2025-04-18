from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        ai_project_name = os.getenv('QA_PROJECT_NAME')
        ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        qa_client = QuestionAnsweringClient(ai_endpoint, credential)

        # Submit a question and display the answer
        while True:
            user_question = input("\nQuestion: \n")
            if user_question.lower() == "quit":
                break
            response = qa_client.get_answers(question=user_question, project_name=ai_project_name, deployment_name=ai_deployment_name)

            for candidate in response.answers:
                print(candidate.answer)
                print("Confidence: {}".format(candidate.confidence))
                print("Source: {}".format(candidate.source))
                
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()