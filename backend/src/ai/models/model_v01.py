from ai.models.model_base import Model_base
from typing import List, Optional
from transformers import pipeline
from api.config.ai_config import ai_huggingface_token


class Model(Model_base):
    """
    Example concrete implementation of Model_base.
    """
    def __init__(self, ai_huggingface_token: str):
        # Initialize the classifier once
        self.classifier = pipeline(model="facebook/bart-large-mnli", token=ai_huggingface_token)

        # Define SDG label dictionary
        self.sdg_labels_dict = {
            "SDG1": "End poverty in all its forms everywhere", 
            "SDG2": "End hunger, achieve food security and improved nutrition and promote sustainable agriculture", 
            "SDG3": "Ensure healthy lives and promote well-being for all at all ages", 
            "SDG4": "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all", 
            "SDG5": "Achieve gender equality and empower all women and girls", 
            "SDG6": "Ensure availability and sustainable management of water and sanitation for all", 
            "SDG7": "Ensure access to affordable, reliable, sustainable and modern energy for all", 
            "SDG8": "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all", 
            "SDG9": "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation", 
            "SDG10": "Reduce inequality within and among countries", 
            "SDG11": "Make cities and human settlements inclusive, safe, resilient and sustainable", 
            "SDG12": "Ensure sustainable consumption and production patterns", 
            "SDG13": "Take urgent action to combat climate change and its impacts", 
            "SDG14": "Conserve and sustainably use the oceans, seas and marine resources for sustainable development", 
            "SDG15": "Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss", 
            "SDG16": "Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels", 
            "SDG17": "Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development"
        }

        # Precompute candidate label values
        self.candidate_label_values = list(self.sdg_labels_dict.values())


    def get_sdg_code_from_label(self, label: str) -> str:
        """Reverse lookup SDG code from full label text."""
        for code, text in self.sdg_labels_dict.items():
            if label == text:
                return code
        return "None"


    def classify_description(self, description: str) -> str:
        """
        Use the classifier to determine the most relevant SDG.
        """

        sdg_pred = "None"

        # If desc size > 20 word
        if len(description.split()) > 20:
            result = self.classifier(description, candidate_labels=self.candidate_label_values)
            
            if result["scores"][0] >= 0.18:
                top_label = result["labels"][0]
                sdg_pred = self.get_sdg_code_from_label(top_label)

        return sdg_pred