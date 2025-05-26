import re
import os
from typing import Tuple, List
from api.config.logging_config import logger
from ai.models.prompt.sdg_label_prompt import sdg_label_prompt


class Classify_patent():
    """
    Classifies patent text to identify relevant Sustainable Development Goals (SDGs).

    This class uses a language model to analyze patent descriptions and
    extract the SDGs they pertain to, along with a justification for the
    classification. It reads a prompt template from a file, formats it
    with the patent text, and then queries a specified model.
    """

    def __init__(self, client, model_name: str, prompt_name: str, temperature=0.2, max_tokens=20000):
        """Initializes the Classify_patent instance.

        Args:
            client: The client object used to interact with the language model.
            model_name (str): The name or identifier of the language model to be used.
            prompt_template_path (str): The file path to the prompt template.
                This template should contain a placeholder "{description}"
                which will be replaced by the patent text.
        """
        self.prompt_name = prompt_name
        self.model_name = model_name
        self.client = client
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _get_sdg_reason(self, text: str) -> Tuple[str, str]:
        """Extracts SDG (Sustainable Development Goal) and reason from a text.

        The input text is expected to contain <sdg> and <reason> XML-like tags
        enclosing the relevant information.

        Args:
            text (str): The input string, potentially containing SDG and reason
                information enclosed in <sdg>...</sdg> and <reason>...</reason>
                tags.

        Returns:
            Tuple[str, str]: A tuple containing two strings:
                - The content of the <sdg> tag, stripped of leading/trailing
                  whitespace.
                - The content of the <reason> tag, stripped of leading/trailing
                  whitespace.
                Returns empty strings for either if the corresponding tag is not found.
        """
        reason_match = re.search(r'<reason>(.*?)</reason>', text, re.DOTALL)
        sdg_match = re.search(r'<sdg>(.*?)</sdg>', text, re.DOTALL)

        reason_content_regex = ""
        sdg_content_regex = ""

        if reason_match:
            reason_content_regex = reason_match.group(1).strip()

        if sdg_match:
            sdg_content_regex = sdg_match.group(1).strip()
        return sdg_content_regex, reason_content_regex

    def _extract_sdgs(self, text: str) -> List[str]:
        """
        Extracts and standardizes SDG references from a given text.

        This method identifies SDG mentions in various formats, including:
        - "SDG" followed by a number (e.g., "SDG1", "SDG 2").
        - Numbers with sub-targets (e.g., "16.1", "3.4"), where the main number
          is extracted.
        - Standalone numbers (1-17) that appear at the beginning of the text
          or are preceded by common delimiters (commas, semicolons, colons, whitespace)
          and followed by delimiters or the end of the string.
        The matching is case-insensitive.

        Args:
            text (str): The input text to scan for SDG references.

        Returns:
            List[str]: A list of unique SDGs found, formatted as "SDG<number>"
                (e.g., ["SDG1", "SDG2"]), sorted numerically. Returns ["None"]
                if no valid SDGs (1-17) are found or if the input text is empty
                or not a string.
        """
        logger.debug(f"Extracting SDGs from text: {text[:100]}")
        if not text or not isinstance(text, str):
            # Modified to return ["None"] as per original logic for empty/invalid text
            return ["None"]

        sdg_numbers = set()  # Use set to avoid duplicates

        # Pattern 1: SDG followed by number with optional sub-target
        # Captures: SDG1, sdg 2, SDG13.4, etc.
        sdg_pattern = r'(?i)\bsdg\s*(\d{1,2})(?:\.\d+)?\b'
        sdg_matches = re.findall(sdg_pattern, text)
        for match in sdg_matches:
            number = int(match)
            if 1 <= number <= 17:
                sdg_numbers.add(number)

        # Pattern 2: Number with sub-target (e.g., "16.1", "3.4")
        # Look for patterns like X.Y where X is 1-17
        number_with_sub_pattern = r'\b(\d{1,2})\.\d+\b'
        sub_matches = re.findall(number_with_sub_pattern, text)
        for match in sub_matches:
            number = int(match)
            if 1 <= number <= 17:
                sdg_numbers.add(number)

        # Pattern 3: Standalone numbers at beginning or after delimiters
        standalone_pattern = r'(?:^|[,;:]\s*|(?<=\s))(\d{1,2})(?=\s*[,;]|\s*$|\s+)'
        standalone_matches = re.findall(standalone_pattern, text.strip())
        for match in standalone_matches:
            number = int(match)
            if 1 <= number <= 17:
                sdg_numbers.add(number)

        # Convert to sorted list of formatted strings
        result = [f"SDG{num}" for num in sorted(sdg_numbers)]

        return ["None"] if not result else result

    def generate_response(self, patent_text: str) -> Tuple[str, str]:
        """
        Generates a response from the language model for a given patent text.

        This method formats the prompt template with the patent text and sends
        it to the configured language model. It then extracts the SDG-related
        content and the reasoning from the model's response.

        Args:
            patent_text (str): The text of the patent to be analyzed.

        Returns:
            Tuple[str, str]: A tuple containing:
                - The content extracted from the <sdg> tag in the model's response.
                - The content extracted from the <reason> tag in the model's response.
        """
        formatted_prompt = sdg_label_prompt(self.prompt_name, patent_text)
        # Assuming self.client.generate returns a dictionary-like object
        # with a 'response' key.
        output = self.client.generate(
            model=self.model_name,
            prompt=formatted_prompt,
            options={"temperature": self.temperature,
                     "max_tokens": self.max_tokens}  # Example option
        )
        response = output.get('response', '').strip() if isinstance(
            output, dict) else str(output).strip()
        return self._get_sdg_reason(response)

    def analyze_patent(self, patent_text: str) -> Tuple[List[str], str]:
        """
        Classifies a patent text to determine relevant SDGs and the reasoning.

        This is the main method that orchestrates the classification process.
        It first calls the language model to get an initial classification and
        reasoning, then processes the SDG information to return a standardized list.

        Args:
            patent_text (str): The text of the patent to classify.

        Returns:
            Tuple[List[str], str]: A tuple containing:
                - A list of identified SDGs, standardized (e.g., ["SDG1", "SDG7"]).
                  Returns ["None"] if no SDGs are identified.
                - A string containing the reason for the classification.
        """
        logger.debug(f"Analyzing patent text: {patent_text[:100]}...")
        sdg_tag_content, reason = self.generate_response(patent_text)
        logger.debug(f"SDG Tag Content: {sdg_tag_content}")
        list_sdg = self._extract_sdgs(sdg_tag_content)

        return list_sdg, reason
