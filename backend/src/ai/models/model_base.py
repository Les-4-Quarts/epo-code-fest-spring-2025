from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
import time
from pathlib import Path
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

class Model_base(ABC):
    """
    Abstract base class (non-instantiable) for classification models 
    and summary generation related to SDGs (Sustainable Development Goals).
    
    This class defines the common interface that all concrete models 
    inheriting from this class must implement.
    """

    # SDGs liste
    SDGS = [
        "SDG1", "SDG2", "SDG3", "SDG4", "SDG5", "SDG6", "SDG7", "SDG8", 
        "SDG9", "SDG10", "SDG11", "SDG12", "SDG13", "SDG14", "SDG15", "SDG16", "SDG17"
    ]

    def __init__(self):
        """
        Private constructor to prevent direct instantiation.
        """
        if self.__class__ is Model_base:
            raise TypeError("The Model_base class cannot be instantiated directly")
    
    @abstractmethod
    def classify_description(self, description: str) -> str:
        """
        Classifies a description according to the SDGs.
        
        Args:
            description (str): The description to classify
            
        Returns:
            str: The corresponding SDG or empty string if no match
        """
        pass
    

    def generate_summary(self, descriptions: List[str], sdg: str) -> str:
        """
        Generates a summary of why the descriptions 
        are related to the specified SDG.
        
        Args:
            descriptions (List[str]): List of descriptions to analyze
            sdg (str): The target SDG
            
        Returns:
            str: The summary explaining the links to the SDG
        """
        return "not implemented"
    
    def evaluation(self, testset_path: str = "testset.jsonl", output_path: str = "evaluation_results.jsonl") -> Dict[str, Any]:
        """
        Generic evaluation function for all models.
        Evaluates classification performance on a JSONL test dataset.
        
        Args:
            testset_path (str): Path to the JSONL test file
            output_path (str): Path for the output JSONL file with results
            
        Returns:
            Dict[str, Any]: Evaluation metrics including accuracy, timing, and detailed results
        """

        # Check if test file exists
        if not Path(testset_path).exists():
            return {"error": f"Test file {testset_path} not found"}
        
        # Initialize metrics
        results = []
        correct_predictions = 0
        total_predictions = 0
        start_time = time.time()
        
        # First pass to count total lines for progress bar
        total_lines = 0
        try:
            with open(testset_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        total_lines += 1
        except Exception as e:
            print(f"Warning: Could not count lines for progress bar: {e}")
        
        # Process each line in the JSONL file
        try:
            with open(testset_path, 'r', encoding='utf-8') as f:
                # Create progress bar if tqdm is available
                if tqdm is not None:
                    progress_bar = tqdm(total=total_lines, desc="Evaluating", unit="descriptions")
                else:
                    progress_bar = None
                
                for line_num, line in enumerate(f, 1):
                    # Skip empty lines
                    if not line.strip():
                        continue
                    
                    # Update progress bar
                    if progress_bar is not None:
                        progress_bar.update(1)
                        progress_bar.set_postfix({
                            'accuracy': f"{correct_predictions}/{total_predictions}" if total_predictions > 0 else "0/0"
                        })
                        
                    try:
                        # Parse JSON line
                        data = json.loads(line.strip())
                        
                        # Extract required fields
                        patent_number = data.get("patent_number", "")
                        description_number = data.get("description_number", "")
                        description_text = data.get("description_text", "")
                        true_sdg = data.get("sdg", "")

                        print(f"true_sdg = {true_sdg}")
                        
                        # Skip if missing required fields
                        if not description_text or not true_sdg:
                            print(f"Warning: Skipping line {line_num} - missing required fields")
                            continue
                        
                        # Classify the description
                        prediction_start = time.time()
                        try:
                            predicted_sdg = self.classify_description(description_text)
                            # Ensure predicted_sdg is a string
                            if predicted_sdg is None:
                                predicted_sdg = ""
                            predicted_sdg = str(predicted_sdg)
                        except Exception as e:
                            print(f"Error in classification for line {line_num}: {e}")
                            predicted_sdg = ""
                        
                        prediction_time = time.time() - prediction_start
                        
                        # Check if prediction is correct
                        is_correct = predicted_sdg == true_sdg
                        if is_correct:
                            correct_predictions += 1
                        total_predictions += 1
                        
                        # Store result
                        result = {
                            "patent_number": patent_number,
                            "description_number": description_number,
                            "description_text": description_text,
                            "true_sdg": true_sdg,
                            "predicted_sdg": predicted_sdg,
                            "is_correct": is_correct,
                            "prediction_time": prediction_time,
                            "line_number": line_num
                        }
                        results.append(result)
                        
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON on line {line_num}: {e}")
                        continue
                    except Exception as e:
                        print(f"Error processing line {line_num}: {e}")
                        continue
                
                # Close progress bar
                if progress_bar is not None:
                    progress_bar.close()
        
        except FileNotFoundError:
            return {"error": f"Cannot open file {testset_path}"}
        except Exception as e:
            return {"error": f"Unexpected error reading file: {str(e)}"}
        
        # Check if we have any valid predictions
        if total_predictions == 0:
            return {"error": "No valid predictions made - check your test file format"}
        
        # Calculate total time
        total_time = time.time() - start_time
        
        # Calculate metrics
        accuracy = correct_predictions / total_predictions
        avg_prediction_time = sum(r["prediction_time"] for r in results) / len(results)
        
        # Save detailed results to JSONL file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Write summary as first line (metadata)
                summary_metadata = {
                    "_metadata": True,
                    "evaluation_summary": {
                        "accuracy": accuracy,
                        "correct_predictions": correct_predictions,
                        "total_predictions": total_predictions,
                        "total_evaluation_time": total_time,
                        "average_prediction_time": avg_prediction_time,
                        "predictions_per_second": total_predictions / total_time if total_time > 0 else 0,
                        "incorrect_predictions_count": total_predictions - correct_predictions,
                        "testset_file": testset_path,
                        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                f.write(json.dumps(summary_metadata, ensure_ascii=False) + '\n')
                
                # Write detailed results
                for result in results:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Warning: Could not save results to {output_path}: {e}")
        
        # Prepare summary metrics
        evaluation_metrics = {
            "accuracy": accuracy,
            "correct_predictions": correct_predictions,
            "total_predictions": total_predictions,
            "total_evaluation_time": total_time,
            "average_prediction_time": avg_prediction_time,
            "predictions_per_second": total_predictions / total_time if total_time > 0 else 0,
            "incorrect_predictions_count": total_predictions - correct_predictions,
            "output_file": output_path,
            "testset_file": testset_path
        }
        
        # Add SDG-wise breakdown
        sdg_breakdown = {}
        for result in results:
            true_sdg = result["true_sdg"]
            if true_sdg not in sdg_breakdown:
                sdg_breakdown[true_sdg] = {"total": 0, "correct": 0}
            
            sdg_breakdown[true_sdg]["total"] += 1
            if result["is_correct"]:
                sdg_breakdown[true_sdg]["correct"] += 1
        
        # Calculate accuracy for each SDG
        for sdg, stats in sdg_breakdown.items():
            stats["accuracy"] = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        
        evaluation_metrics["sdg_breakdown"] = sdg_breakdown
        
        # Print summary
        print(f"\n=== EVALUATION RESULTS ===")
        print(f"Total predictions: {total_predictions}")
        print(f"Correct predictions: {correct_predictions}")
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Average prediction time: {avg_prediction_time:.4f} seconds")
        print(f"Predictions per second: {evaluation_metrics['predictions_per_second']:.2f}")
        print(f"Incorrect predictions: {evaluation_metrics['incorrect_predictions_count']}")
        print(f"Results saved to: {output_path}")
        
        # Show SDG breakdown
        print(f"\n=== SDG BREAKDOWN ===")
        for sdg, stats in sorted(sdg_breakdown.items()):
            print(f"{sdg}: {stats['correct']}/{stats['total']} ({stats['accuracy']:.2%})")
        
        # Show some examples of incorrect predictions
        incorrect_results = [r for r in results if not r["is_correct"]]
        if incorrect_results:
            print(f"\n=== SAMPLE INCORRECT PREDICTIONS ===")
            for i, result in enumerate(incorrect_results[:5]):  # Show first 5 incorrect
                print(f"\nExample {i+1}:")
                print(f"Patent: {result['patent_number']}")
                print(f"Description: {result['description_text'][:100]}...")
                print(f"True SDG: {result['true_sdg']}")
                print(f"Predicted SDG: {result['predicted_sdg']}")
        
        return evaluation_metrics