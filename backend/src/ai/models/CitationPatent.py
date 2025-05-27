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
        Extracts <summary> elements and <citation><explanation> pairs from text.

        The method assumes the input text contains XML-like tags `<citation>`
        and `<explanation>` delimiting the relevant content. It also expects
        a `</think>` tag preceding the main content.

        Args:
            text: The text to analyze

        Returns:
            Tuple containing (summary_content, formatted_citations_explanations)
        """
        logger.debug(f"Raw text for citation/explanation extraction: {text}")
        # Remove the part before </think> if it exists
        if "</think>" in text:
            text = text.split("</think>", 1)[1]

        # Extract summary if it exists
        summary_match = re.search(
            r'<summary>\s*(.*?)\s*</summary>', text, re.DOTALL)
        summary_content = summary_match.group(
            1).strip() if summary_match else ""

        # Extract all citation/explanation pairs
        citation_explanation_pairs = []

        # Find all citations
        citation_matches = re.finditer(
            r'<citation>\s*(.*?)\s*<\/citation>', text, re.DOTALL | re.IGNORECASE
        )

        for citation_match in citation_matches:
            citation_content = citation_match.group(1).strip()
            citation_end = citation_match.end()

            # Find the corresponding explanation after the citation
            remaining_text = text[citation_end:]
            explanation_match = re.search(
                r'\s*<explanation>\s*(.*?)\s*<\/explanation>', remaining_text, re.DOTALL | re.IGNORECASE
            )

            if explanation_match:
                explanation_content = explanation_match.group(1).strip()
                citation_explanation_pairs.append(
                    (citation_content, explanation_content)
                )

        logger.debug(
            f"Extracted summary: {summary_content}")
        logger.debug(
            f"Extracted {len(citation_explanation_pairs)} citation/explanation pairs.")

        # Format the citation/explanation pairs
        formatted_pairs = []
        for i, (citation, explanation) in enumerate(citation_explanation_pairs, 1):
            formatted_pair = f"**Citation {i}:**\n{citation}\n**Explanation {i}:**\n{explanation}"
            formatted_pairs.append(formatted_pair)

        formatted_citations_explanations = "\n\n".join(formatted_pairs)

        return summary_content, formatted_citations_explanations

    def generate_response(self, patent_text: str, sdg: str, reason: str) -> Tuple[str, str]:
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
        logger.debug(
            f"Generating response for SDG: {sdg} with reason: {reason}")

        if sdg != "None":
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

            summary_content, formatted_citations_explanations = self._get_citation_explanation(
                response)

        # If not a SDG the previous model already made an explanation
        else:
            summary_content, formatted_citations_explanations = reason, ""

        return summary_content, formatted_citations_explanations

    # Modified to return str for citation_content based on _get_citation_explanation
    def citation(self, patent_text: str, sdg: str, reason: str) -> Tuple[str, str]:
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
        logger.debug(
            f"Generating citation for SDG: {sdg} with reason: {reason}")
        summary_content, formatted_citations_explanations = self.generate_response(
            patent_text, sdg, reason)
        logger.debug(f"Citation: {summary_content}")
        logger.debug(f"Explanation: {formatted_citations_explanations}")

        return summary_content, formatted_citations_explanations
