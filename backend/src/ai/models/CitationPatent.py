import re
import os
from typing import Tuple, List, Any  # Added Any for the client type
from api.config.logging_config import logger
from ai.models.prompt.sdg_citation_prompt import sdg_citation_prompt


class CitationPatent():
    """
    A class to generate citations and explanations for patents based on Sustainable Development Goals (SDGs).

    This class interacts with a language model to analyze patent text and identify relevant
    citations and explanations linked to a specific SDG.
    """

    def __init__(self, client: Any, model_name: str, temperature: float = 0.2, max_tokens: int = 20000):
        """
        Initializes the CitationPatent class.

        Args:
            client (Any): The client object used to interact with the language model.
                          (Specific type depends on the LLM client library used).
            model_name (str): The name of the language model to be used.
            temperature (float, optional): Controls randomness in the generation process.
                                           Lower values make the output more deterministic.
                                           Defaults to 0.2.
            max_tokens (int, optional): The maximum number of tokens to generate in the response.
                                        Defaults to 20000.
        """
        self.model_name: str = model_name
        self.client: Any = client
        self.temperature: float = temperature
        self.max_tokens: int = max_tokens

    def _get_citation_explanation(self, text: str) -> Tuple[str, str]:
        """
        Extracts citation and explanation content from a raw text response.

        The method assumes the input text contains XML-like tags `<citation>`
        and `<explanation>` delimiting the relevant content. It also expects
        a `</think>` tag preceding the main content.

        Args:
            text (str): The raw text string containing the citation and explanation.

        Returns:
            Tuple[str, str]: A tuple containing the extracted citation string
                             and explanation string. If a tag is not found,
                             the corresponding string will be empty.
        """
        # Assumes the relevant part of the text starts after "</think>"
        try:
            text_after_think: str = text.split("</think>", 1)[1]
        except IndexError:
            # Handle cases where "</think>" is not present
            logger.warning(
                "The '</think>' tag was not found in the response. Processing the entire text.")
            text_after_think = text

        citation_match: re.Match[str] | None = re.search(
            r'<citation>(.*?)</citation>', text_after_think, re.DOTALL)
        explanation_match: re.Match[str] | None = re.search(
            r'<explanation>(.*?)</explanation>', text_after_think, re.DOTALL)

        citation_content_regex: str = ""
        explanation_content_regex: str = ""

        if citation_match:
            citation_content_regex = citation_match.group(1).strip()

        if explanation_match:
            explanation_content_regex = explanation_match.group(1).strip()
        return citation_content_regex, explanation_content_regex

    def generate_response(self, patent_text: str, sdg: str) -> Tuple[str, str]:
        """
        Generates a citation and explanation for a given patent text and SDG.

        This method formats a prompt using the patent text and SDG, sends it
        to the language model, and then extracts the citation and explanation
        from the model's response.

        Args:
            patent_text (str): The text of the patent to be analyzed.
            sdg (str): The Sustainable Development Goal to which the patent relates.

        Returns:
            Tuple[str, str]: A tuple containing the generated citation string
                             and explanation string.
        """
        formatted_prompt: str = sdg_citation_prompt(patent_text, sdg)
        # Assuming self.client.generate returns a dictionary-like object
        # with a 'response' key, or a string directly.
        output: Any = self.client.generate(
            model=self.model_name,
            prompt=formatted_prompt,
            options={"temperature": self.temperature,
                     "max_tokens": self.max_tokens}
        )
        # Handle different possible output types from self.client.generate
        response: str
        if isinstance(output, dict):
            response = output.get('response', '').strip()
        elif isinstance(output, str):
            response = output.strip()
        else:
            # Fallback for unexpected output types
            logger.warning(
                f"Unexpected output type from LLM client: {type(output)}. Converting to string.")
            response = str(output).strip()

        return self._get_citation_explanation(response)

    # Modified to return str for citation_content based on _get_citation_explanation
    def citation(self, patent_text: str, sdg: str) -> Tuple[str, str]:
        """
        Provides a citation and explanation for a patent concerning a specific SDG.

        This is the main public method to get the citation and explanation.
        It calls `generate_response` to interact with the LLM and then
        logs the results.

        Args:
            patent_text (str): The text of the patent.
            sdg (str): The Sustainable Development Goal.

        Returns:
            Tuple[str, str]: A tuple where the first element is the citation string
                             (can be a single string, potentially with multiple citations
                             formatted within it, based on `_get_citation_explanation`'s current output)
                             and the second element is the explanation string.
        """
        citation_content: str
        explanation_content: str
        citation_content, explanation_content = self.generate_response(
            patent_text, sdg)
        logger.debug(f"Citation: {citation_content}")
        logger.debug(f"Explanation: {explanation_content}")

        return citation_content, explanation_content
