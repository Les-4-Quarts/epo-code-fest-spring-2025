from ai.models.model_base import Model_base
from typing import List, Optional
from transformers import pipeline
import re
from api.config.ai_config import ai_client, ai_model


class Model(Model_base):
    """
    Example concrete implementation of Model_base.
    """
    def __init__(self):
        # Initialize prompt
        with open("sdg_label_prompt.md", "r") as f:
            self.prompt_template = f.read()


    def classify_description(self, description: str) -> str:
        """
        Use the classifier to determine the most relevant SDG.
        """
        try:
            formatted_prompt = self.prompt_template.replace("{description}", description)
            # Generate the SDG classification
            response_data = ai_client.generate(
                model=ai_model, # Make sure this model is available in your Ollama instance
                prompt=formatted_prompt
                # You might want to add other parameters like 'stream=False'
                # or options within a dictionary if your client version supports it.
                # Example: options={"temperature": 0.7}
            )
            # Get the raw text output from the model's response
            # The actual key for the response text is usually 'response'
            raw_output_text = response_data.get('response', '').strip()
            
            print(f"llm_output = {raw_output_text}")

            # Extract SDG from raw output
            # Nouveau motif regex
            sdg_pattern = r'<sdg>\s*(\d{1,2})'

            # Recherche dans le texte brut
            matches = re.findall(sdg_pattern, raw_output_text, re.IGNORECASE)

            if matches:
                # Convertit en entier pour normaliser (ex: "01" -> 1) et filtre sur 1 à 17
                sdg_numbers = [int(match) for match in matches if 1 <= int(match) <= 17]
                if sdg_numbers:
                    return f"SDG{sdg_numbers[0]}"

            return "None"
            
        except Exception as e:
            print(f"Error in classification: {e}")
            return "None"