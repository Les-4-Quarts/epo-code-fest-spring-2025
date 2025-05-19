import json
from googletrans import Translator
import asyncio
import polars


async def translate_text(translator, text):
    """Translate text to English using Google Translate API.
    Args:
        translator (Translator): The Google Translate API translator object.
        text (str): The text to translate.
    Returns:
        str: The translated text.
    """
    try:
        translation = await translator.translate(text, src='auto', dest='fr')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


async def label_descriptions(input_file, output_file="data/labeled_data.ndjson"):
    """Label patent descriptions with SDG.
    Args:
        descriptions (list): A list of tuples containing patent number, description number, and description text.
        output_file (str): The path to the output NDJSON file.
    """
    translator = Translator()

    already_labeled = polars.read_ndjson(output_file)
    descriptions = polars.read_json(input_file)

    # Filter out already labeled descriptions with patent number and description number
    descriptions = descriptions.filter(
        ~((descriptions['patent_number'].is_in(already_labeled['patent_number'])) &
          (descriptions['description_number'].is_in(already_labeled['description_number'])))
    )
    descriptions = descriptions.to_dicts()

    for desc in descriptions:
        patent_number = desc['patent_number']
        description_number = desc['description_number']
        description_text = desc['description_text']
        predicted_sdg = desc['sdg']

        # Translate the description text to English
        translated_text = await translate_text(translator, description_text)

        print(f"Patent Number: {patent_number}")
        print(f"Description Number: {description_number}")
        print(f"Description Text: {translated_text}")
        print(f"Predicted SDG: {predicted_sdg}")
        sdg = input(
            "Enter SDG label (0 for None, 1-17 for SDG1-SDG17): ").strip()

        # If no input, skip the labeling
        if not sdg:
            sdg = predicted_sdg
        else:
            sdg = f"SDG{sdg}" if sdg != "0" else "None"

        # Validate SDG input
        with open(output_file, 'a') as f:
            json.dump({
                "patent_number": patent_number,
                "description_number": description_number,
                "description_text": description_text,
                "sdg": sdg,
            }, f)
            f.write('\n')


if __name__ == "__main__":
    asyncio.run(label_descriptions(input_file="data/testset_v2_de_raw.json"))
