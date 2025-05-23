import json
from googletrans import Translator
import asyncio
import polars as pl
import os
from api.config.db_config import get_db_connection


def search_text_in_patents(search_text):
    """
    Search for patents containing the specified text in their title or abstract.
    """
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to search for patents
    query = """
        SELECT patent_number, description_number, description_text
        FROM patent_description
        WHERE description_text LIKE %s
        LIMIT 100
    """

    # Execute the query with the search text
    cursor.execute(query, (f'%{search_text}%',))

    # Fetch all matching patents
    results = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return results


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


async def label_descriptions_from_db(search_text, translate=True, output_file="labeled_patents.jsonl"):
    """
    Searches for patent descriptions in the database using a keyword and allows the user to manually assign SDG labels.
    Translates descriptions if specified.

    Args:
        search_text (str): Keyword to search for in the database.
        translate (bool): If True, translates text to French before labeling.

    Behavior:
        - Searches for patent descriptions in the database using the provided keyword.
        - Optionally translates descriptions to French.
        - Displays each description and predicted SDG label.
        - Prompts user to confirm or correct the SDG label.
        - Writes labeled data to an output JSONL file.
    """
    translator = Translator()  # Initialize translator

    # Search for descriptions in the database
    descriptions = search_text_in_patents(search_text)
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
        d[0], d[1]) not in already_labeled]
    total_remaining = len(remaining)

    print(f"\nTotal descriptions: {total}")
    print(f"Already labeled: {total - total_remaining}")
    print(f"Remaining to label: {total_remaining}")

    # Iterate over remaining descriptions
    for idx, desc in enumerate(remaining, 1):
        patent_number = desc[0]
        description_number = desc[1]
        description_text = desc[2]
        predicted_sdg = "None"  # Default prediction if not available

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
    # Launch manual labeling with a keyword search
    asyncio.run(label_descriptions_from_db("peace"))
