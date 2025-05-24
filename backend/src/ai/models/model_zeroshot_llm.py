from ai.models.model_base import Model_base
from typing import List, Optional
import re
from api.config.ai_config import ai_client
import os
import json
import time
from tqdm import tqdm
from datetime import datetime
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score, f1_score

class Model():

    def __init__(self, model_name, prompt_template_path):
        self.prompt_template_path = prompt_template_path
        self.model_name = model_name
        # Initialize prompt
        with open(prompt_template_path, "r") as f:
            self.prompt_template = f.read()

    def _get_sdg_reason(self, text):
        reason_match = re.search(r'<reason>(.*?)</reason>', text, re.DOTALL)
        sdg_match = re.search(r'<sdg>(.*?)</sdg>', text, re.DOTALL)

        reason_content_regex = ""
        sdg_content_regex = ""

        if reason_match:
            reason_content_regex = reason_match.group(1).strip()

        if sdg_match:
            sdg_content_regex = sdg_match.group(1).strip()

        return sdg_content_regex, reason_content_regex
        
    def _extract_all_sdgs(self, text):
        """
        Extracts all SDGs found in a text and returns them as a standardized list.
        
        This function detects multiple SDG references in various formats including:
        - SDG followed by number (e.g., "SDG1", "SDG 2")
        - Numbers with sub-targets (e.g., "16.1", "3.4")
        - Standalone numbers at the beginning or after delimiters
        - Case-insensitive matching
        
        Args:
            text (str): The input text to analyze
            
        Returns:
            list: A list of unique SDGs found in the format ["SDG1", "SDG2", ...], 
                sorted numerically, or empty list if none found
        """
        if not text or not isinstance(text, str):
            return []
        
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
        # More careful matching to avoid false positives
        # Look for numbers that are:
        # - At the start of the string followed by delimiter or end
        # - After comma/semicolon/colon followed by delimiter or end
        # - After whitespace followed by delimiter or end
        standalone_pattern = r'(?:^|[,;:]\s*|(?<=\s))(\d{1,2})(?=\s*[,;]|\s*$|\s+)'
        standalone_matches = re.findall(standalone_pattern, text.strip())
        for match in standalone_matches:
            number = int(match)
            if 1 <= number <= 17:
                sdg_numbers.add(number)
        
        # Convert to sorted list of formatted strings
        result = [f"SDG{num}" for num in sorted(sdg_numbers)]

        return ["None"] if not result else result

    def classify_description(self, description: str):
        """
        Use the classifier to determine the most relevant SDG.
        """
        try:
            formatted_prompt = self.prompt_template.replace("{description}", description)
            # Generate the SDG classification
            response_data = ai_client.generate(
                model=self.model_name,
                prompt=formatted_prompt,
                options={"temperature": 0.2}
            )
            # Get the raw text output from the model's response
            raw_output_text = response_data.get('response', '').strip()
            sdg_balise, reason_balise = self._get_sdg_reason(raw_output_text)

            return sdg_balise, reason_balise
        
        except Exception as e:
            print(f"Error in classification: {e}")
            return "error", "error"

    def run_evaluation(self, testset_path: str, output_path: str):
        """
        Runs evaluation on a JSONL test dataset, classifying each description and saving results.

        If the specified output path already exists, appends a numeric suffix (_1, _2, ...) 
        to avoid overwriting the existing file.

        For each line in the test set:
            - Extracts the 'description_text' field
            - Measures the prediction time
            - Classifies the description using `classify_description`
            - Saves the enriched line with classification results and prediction time

        At the end, appends a metadata entry containing:
            - model_name
            - testset_path
            - prompt_template_path (if available)
            - creation date

        Args:
            testset_path (str): Path to the input .jsonl test dataset.
            output_path (str): Desired path to save the output .jsonl file.

        Returns:
            None
        """

        def get_safe_output_path(path):
            """Generates a non-conflicting file path by appending a numeric suffix if needed."""
            base, ext = os.path.splitext(path)
            counter = 1
            while os.path.exists(path):
                path = f"{base}_{counter}{ext}"
                counter += 1
            return path

        # Ensure the output file won't overwrite an existing file
        safe_output_path = get_safe_output_path(output_path)

        # Read all lines for progress tracking
        with open(testset_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(safe_output_path, "w", encoding="utf-8") as out_f:
            for line in tqdm(lines, desc="Running evaluation"):
                data = json.loads(line)
                description_text = data.get("description_text", "")

                # Rename sdg in true_sdg
                if "sdg" in data:
                    data["true_sdg"] = data.pop("sdg")

                # Time the classification
                start_time = time.time()
                sdg_balise, reason_balise = self.classify_description(description_text)
                prediction_time = time.time() - start_time

                # Add classification results and timing to the entry
                data.update({
                    "sdg_balise": sdg_balise,
                    "reason_balise": reason_balise,
                    "prediction_time": prediction_time
                })

                # Write enriched data to output
                out_f.write(json.dumps(data) + "\n")

            # Append metadata at the end
            meta_data = {
                "meta_data": {
                    "model_name": self.model_name,
                    "testset_path": testset_path,
                    "prompt_template_path": getattr(self, "prompt_template_path", "N/A"),
                    "date_creation": datetime.now().isoformat()
                }
            }
            out_f.write(json.dumps(meta_data) + "\n")

    def show_evaluation_mono(self, evaluation_path: str):
        """
        Evaluates the predictions in a previously generated evaluation .jsonl file.

        Each prediction line must contain:
            - "sdg": the ground truth SDG label (e.g., "SDG3")
            - "sdg_balise": predicted SDG(s) as a string (e.g., "SDG1, SDG3, SDG7")

        A prediction is considered correct if the ground truth SDG is among the predicted SDGs.

        Statistics reported:
            - Total predictions and correct ones
            - Overall accuracy
            - Average and total prediction time
            - SDG-specific accuracy breakdown
            - Sample of incorrect predictions

        Args:
            evaluation_path (str): Path to the JSONL evaluation file created by `run_evaluation`.

        Returns:
            None
        """

        results = []
        meta_data = {}
        total_predictions = 0
        correct_predictions = 0
        total_time = 0.0
        sdg_breakdown = defaultdict(lambda: {"correct": 0, "total": 0})

        # Read and evaluate each line
        with open(evaluation_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                
                if "meta_data" in data:
                    meta_data = data["meta_data"]
                    continue  # Skip metadata line
                
                # To avoid empty line
                if "patent_number" in data:
                    true_sdg = data.get("true_sdg", "").strip()
                    predicted_sdg_raw = data.get("sdg_balise", "")
                    predicted_sdg_list = self._extract_all_sdgs(predicted_sdg_raw)

                    is_correct = true_sdg in predicted_sdg_list
                    total_predictions += 1
                    if is_correct:
                        correct_predictions += 1

                    prediction_time = data.get("prediction_time", 0.0)
                    total_time += prediction_time

                    sdg_breakdown[true_sdg]["total"] += 1
                    if is_correct:
                        sdg_breakdown[true_sdg]["correct"] += 1

                    results.append({
                        "patent_number": data.get("patent_number", "N/A"),
                        "description_text": data.get("description_text", ""),
                        "true_sdg": true_sdg,
                        "predicted_sdg": predicted_sdg_list,
                        "is_correct": is_correct
                    })

        # Compute summary statistics
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0.0
        avg_prediction_time = total_time / total_predictions if total_predictions > 0 else 0.0
        predictions_per_second = total_predictions / total_time if total_time > 0 else 0.0
        incorrect_predictions_count = total_predictions - correct_predictions

        # Print metadata
        print(f"\n=== META DATA ===")
        for key, value in meta_data.items():
            print(f"{key}: {value}")

        # Print summary
        print(f"\n=== EVALUATION RESULTS ===")
        print(f"Total predictions: {total_predictions}")
        print(f"Correct predictions: {correct_predictions}")
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Average prediction time: {avg_prediction_time:.4f} seconds")
        print(f"Predictions per second: {predictions_per_second:.2f}")
        print(f"Incorrect predictions: {incorrect_predictions_count}")
        print(f"Results loaded from: {evaluation_path}")

        # Show SDG breakdown
        print(f"\n=== SDG BREAKDOWN ===")
        for sdg, stats in sorted(sdg_breakdown.items()):
            sdg_accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            print(f"{sdg}: {stats['correct']}/{stats['total']} ({sdg_accuracy:.2%})")

        # Show some examples of incorrect predictions
        incorrect_results = [r for r in results if not r["is_correct"]]
        if incorrect_results:
            print(f"\n=== SAMPLE INCORRECT PREDICTIONS ===")
            for i, result in enumerate(incorrect_results[:5]):
                print(f"\nExample {i+1}:")
                print(f"Patent: {result['patent_number']}")
                print(f"Description: {result['description_text'][:100]}...")
                print(f"True SDG: {result['true_sdg']}")
                print(f"Predicted SDG: {result['predicted_sdg']}")

# NOT IMPLEMENTED YET
    def show_evaluation_multi(self, evaluation_path: str):
        """
        Evaluates multi-label predictions in a .jsonl file where:
        - "sdg" is the ground truth list of SDGs (e.g., ["SDG3", "SDG7"])
        - "sdg_balise" is a comma-separated string of predicted SDGs (e.g., "SDG3, SDG6, SDG12")

        Evaluation Metrics:
            - Exact Match Ratio (subset accuracy)
            - Micro-averaged Precision, Recall, F1 (good for imbalanced data)
            - Macro-averaged Precision, Recall, F1 (treats each SDG equally)
            - Per-SDG breakdown (correct/total and accuracy)
            - Average prediction time
            - Error examples (mismatched predictions)

        Args:
            evaluation_path (str): Path to the JSONL file with predictions

        Returns:
            None
        """

        all_true_sets = []
        all_pred_sets = []
        all_sdg_set = set()
        total_time = 0.0
        exact_match_count = 0
        total_samples = 0
        meta_data = {}
        results = []
        sdg_breakdown = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

        # First pass: collect all data and determine the complete set of SDGs
        with open(evaluation_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                if "meta_data" in data:
                    meta_data = data["meta_data"]
                    continue  # Skip metadata

                total_samples += 1
                true_sdg = data.get("true_sdg", [])
                pred_sdg_raw = data.get("sdg_balise", "")
                pred_sdg = self._extract_all_sdgs(pred_sdg_raw)

                true_set = set(true_sdg)
                pred_set = set(pred_sdg)

                all_sdg_set.update(true_set)
                all_sdg_set.update(pred_set)
                
                all_true_sets.append(true_set)
                all_pred_sets.append(pred_set)

                total_time += data.get("prediction_time", 0.0)

                # For Exact Match Ratio
                if true_set == pred_set:
                    exact_match_count += 1

                results.append({
                    "patent_number": data.get("patent_number", "N/A"),
                    "description_text": data.get("description_text", ""),
                    "true_sdg": list(true_set),
                    "predicted_sdg": list(pred_set),
                    "is_exact_match": true_set == pred_set
                })

        # Now create binary vectors with consistent length
        sorted_sdgs = sorted(all_sdg_set)
        all_true_labels = []
        all_pred_labels = []
        
        for true_set, pred_set in zip(all_true_sets, all_pred_sets):
            true_binary = [1 if sdg in true_set else 0 for sdg in sorted_sdgs]
            pred_binary = [1 if sdg in pred_set else 0 for sdg in sorted_sdgs]
            
            all_true_labels.append(true_binary)
            all_pred_labels.append(pred_binary)
            
            # Calculate per-SDG breakdown
            for label in sorted_sdgs:
                if label in true_set and label in pred_set:
                    sdg_breakdown[label]["tp"] += 1
                elif label not in true_set and label in pred_set:
                    sdg_breakdown[label]["fp"] += 1
                elif label in true_set and label not in pred_set:
                    sdg_breakdown[label]["fn"] += 1

        # Metrics
        micro_precision = precision_score(all_true_labels, all_pred_labels, average="micro", zero_division=0)
        micro_recall = recall_score(all_true_labels, all_pred_labels, average="micro", zero_division=0)
        micro_f1 = f1_score(all_true_labels, all_pred_labels, average="micro", zero_division=0)

        macro_precision = precision_score(all_true_labels, all_pred_labels, average="macro", zero_division=0)
        macro_recall = recall_score(all_true_labels, all_pred_labels, average="macro", zero_division=0)
        macro_f1 = f1_score(all_true_labels, all_pred_labels, average="macro", zero_division=0)

        avg_prediction_time = total_time / total_samples if total_samples > 0 else 0.0
        predictions_per_second = total_samples / total_time if total_time > 0 else 0.0

        # Print metadata
        print(f"\n=== META DATA ===")
        for key, value in meta_data.items():
            print(f"{key}: {value}")

        # === PRINT RESULTS ===
        print("\n=== MULTI-LABEL EVALUATION RESULTS ===")
        print(f"Total samples: {total_samples}")
        print(f"Exact match count: {exact_match_count}")
        print(f"Exact match ratio: {exact_match_count/total_samples:.4f}")
        print(f"Micro Precision: {micro_precision:.4f}")
        print(f"Micro Recall:    {micro_recall:.4f}")
        print(f"Micro F1-score:  {micro_f1:.4f}")
        print(f"Macro Precision: {macro_precision:.4f}")
        print(f"Macro Recall:    {macro_recall:.4f}")
        print(f"Macro F1-score:  {macro_f1:.4f}")
        print(f"Total prediction time: {total_time:.2f} seconds")
        print(f"Average prediction time: {avg_prediction_time:.4f} seconds")
        print(f"Predictions per second: {predictions_per_second:.2f}")

        # === SDG BREAKDOWN ===
        print("\n=== SDG-WISE BREAKDOWN ===")
        for sdg in sorted_sdgs:
            stats = sdg_breakdown[sdg]
            total = stats["tp"] + stats["fn"]
            accuracy = stats["tp"] / total if total > 0 else 0.0
            print(f"{sdg}: TP={stats['tp']}, FP={stats['fp']}, FN={stats['fn']} → Accuracy: {accuracy:.2%}")

        # === EXAMPLES OF ERRORS ===
        incorrect = [r for r in results if not r["is_exact_match"]]
        if incorrect:
            print("\n=== SAMPLE INCORRECT PREDICTIONS ===")
            for i, r in enumerate(incorrect[:5]):
                print(f"\nExample {i+1}:")
                print(f"Patent: {r['patent_number']}")
                print(f"Description: {r['description_text'][:100]}...")
                print(f"True SDGs: {r['true_sdg']}")
                print(f"Predicted SDGs: {r['predicted_sdg']}")
