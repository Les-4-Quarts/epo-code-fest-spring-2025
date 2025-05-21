import json
from googletrans import Translator
import asyncio
import polars as pl
import os


async def translate_text(translator, text):
    """
    Asynchronously translates a given text to French using Google Translate API.

    Args:
        translator: An instance of the Translator class.
        text (str): The input text to be translated.

    Returns:
        str: The translated text in French. If an error occurs, returns the original text.
    """
    try:
        translation = await translator.translate(text, src='auto', dest='fr')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


async def label_descriptions(file_name, translate=True):
    """
    Loads patent descriptions and allows the user to manually assign SDG labels.
    Translates descriptions if specified and skips already labeled ones.

    Args:
        file_name (str): Name of the JSONL file containing patent descriptions.
        translate (bool): If True, translates text to French before labeling.

    Behavior:
        - Reads patent descriptions from a raw JSONL file.
        - Optionally translates descriptions to French.
        - Displays each description and predicted SDG label.
        - Prompts user to confirm or correct the SDG label.
        - Writes labeled data to an output JSONL file.
    """

    input_file = f"raw/{file_name}"
    output_file = file_name.rsplit('.jsonl', 1)[0] + '_labeled.jsonl'

    translator = Translator()  # Initialize translator

    # Load all descriptions from file
    descriptions = pl.read_ndjson(input_file).to_dicts()
    total = len(descriptions)

    # Load already labeled descriptions to avoid duplicates
    already_labeled = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                item = json.loads(line)
                already_labeled.add(
                    (item["patent_number"], item["description_number"]))

    # Filter out already labeled descriptions
    remaining = [d for d in descriptions if (
        d["patent_number"], d["description_number"]) not in already_labeled]
    total_remaining = len(remaining)

    print(f"\nTotal descriptions: {total}")
    print(f"Already labeled: {total - total_remaining}")
    print(f"Remaining to label: {total_remaining}")

    # Iterate over remaining descriptions
    for idx, desc in enumerate(remaining, 1):
        patent_number = desc["patent_number"]
        description_number = desc["description_number"]
        description_text = desc["description_text"]
        predicted_sdg = desc.get("sdg", "None")

        # Translate description if enabled
        if translate:
            translated_text = await translate_text(translator, description_text)
        else:
            translated_text = description_text

        # Display description info
        print("\n==============================")
        print(f"[{idx}/{total_remaining}]")
        print(f"Patent Number: {patent_number}")
        print(f"Description Number: {description_number}")
        if translate:
            print(f"\nDescription:\n{description_text}")
        print(f"\nTranslated Description:\n{translated_text}")
        print(f"\nPredicted SDG: {predicted_sdg}")
        print("==============================")

        # User input for SDG label
        sdg_input = input(
            "Enter SDG label (1-17), 0 for None, or press Enter to keep prediction: ").strip()
        final_sdg = f"SDG{sdg_input}" if sdg_input and sdg_input != "0" else (
            "None" if sdg_input == "0" else predicted_sdg)

        # Save labeled result
        with open(output_file, "a", encoding="utf-8") as f:
            json.dump({
                "patent_number": patent_number,
                "description_number": description_number,
                "description_text": description_text,
                "sdg": final_sdg
            }, f)
            f.write("\n")


if __name__ == "__main__":
    # Launch manual labeling

    # Patrice
    # asyncio.run(label_descriptions("testset_v1_en_raw_pat.jsonl", translate=False))

    # Quentin
    # asyncio.run(label_descriptions("testset_v1_en_raw_quentin.jsonl"))
