from dotenv import load_dotenv
import os
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
# import namespaces

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        translatorRegion = os.getenv('COG_SERVICE_REGION')
        translatorKey = os.getenv('COG_SERVICE_KEY')
        translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

        # Create client using endpoint and key
        credential = AzureKeyCredential(translatorKey)
        translation_client = TextTranslationClient(endpoint=translator_endpoint, credential=credential, region=translatorRegion)
        
        ## Choose target language
        language_response = translation_client.get_supported_languages(scope="translation")
        print(f" Supported Languages: {len(language_response.translation)}")
        target_language = "te"
        supported_language = False
        print(language_response.keys)
        while supported_language == False:
            target_language = input()
            if target_language in language_response.translation.keys():
                supported_language = True
            else:
                print(f" {target_language} is not a supported language")
    
        # Translate text
        input_text = ""
        while input_text.lower() != "quit":
            input_text = input()
            if input_text != "quit":
                input_text_elements = [InputTextItem(text=input_text)]
                translate_response = translation_client.translate(body=input_text_elements, to_language=[target_language])
                translation = translate_response[0] if translate_response else None
                if translation:
                    source_language = translation.detected_language
                    for translated_text in translation.translations:
                        print({translated_text.text})



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()