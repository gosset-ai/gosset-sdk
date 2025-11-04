"""
Example usage of the GossetClient

This script demonstrates how to use the GossetClient to interact with the Gosset API.
"""
import os
from gosset_sdk import GossetClient


def main():
    # Initialize the client with your API key
    # You can either pass it directly or set GOSSET_API_KEY environment variable
    api_key = os.environ.get("GOSSET_API_KEY")
    
    if not api_key:
        print("Error: Please set GOSSET_API_KEY environment variable")
        print("Example: export GOSSET_API_KEY='your_api_key_here'")
        return
    
    # Create the client (can also use as context manager with 'with' statement)
    client = GossetClient(api_key=api_key)
    
    print("=" * 80)
    print("Gosset API Client Example")
    print("=" * 80)
    print()
    
    # Example 1: Get available filters
    print("1. Getting available filters...")
    print("-" * 80)
    try:
        filters = client.get_filters()
        print(f"Available phases: {filters.get('phase', [])}")
        print(f"Available statuses: {filters.get('status', [])[:5]}...")  # Show first 5
        print(f"Available masking types: {filters.get('masking_type', [])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Example 2: Search for trials
    print("2. Searching for Phase 3 trials with comparator...")
    print("-" * 80)
    try:
        trials = client.get_trials(
            phase="3",
            has_comparator=True,
            limit=5,
            sort_by="-completion_date"
        )
        print(f"Found {trials['total']} matching trials")
        print(f"Showing first {len(trials['results'])} results:")
        for trial in trials['results']:
            nct_id = trial.get('nct_id', 'N/A')
            phase = trial.get('highest_phase', 'N/A')
            date = trial.get('completion_date', 'N/A')
            print(f"  - {nct_id} (Phase {phase}, Completed: {date})")
        
        # Show aggregate stats
        if 'stats' in trials:
            stats = trials['stats']
            print(f"\nAggregate Statistics:")
            print(f"  - Average arm size: {stats.get('average_arm_size', 0):.1f}")
            print(f"  - Trials with biomarkers: {stats.get('trials_with_biomarkers', 0)}")
            print(f"  - Trials with endpoint data: {stats.get('trials_with_endpoint_data', 0)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Example 3: Predict trial success from natural language
    print("3. Predicting trial success from natural language...")
    print("-" * 80)
    try:
        query = """
        Analyze the success probability for a Phase 2 trial of a BRAF inhibitor
        in melanoma with:
        - 80 patients per arm
        - Targeted therapy
        - Has a comparator arm (standard chemotherapy)
        - Small molecule
        - Double-blind randomized design
        """
        
        result = client.predict_trial_success(query=query, return_id=True)
        
        print(f"Query: {query.strip()}")
        print()
        print(f"Prediction: {result['ref']['meta']['prediction']}")
        print(f"Probability: {result['ref']['meta']['probability']:.2%}")
        print()
        print(f"Extracted Parameters:")
        for key, value in result.get('extracted_parameters', {}).items():
            print(f"  - {key}: {value}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Example 4: Predict trial success with structured parameters
    print("4. Predicting trial success with structured parameters...")
    print("-" * 80)
    try:
        trial_params = {
            "highest_phase": 3.0,
            "avg_arm_size": 150,
            "has_comparator": True,
            "therapy_type": ["targeted"],
            "targets": ["EGFR"],
            "diseases": ["non-small cell lung cancer"],
            "modalities": ["Small molecule"],
            "moa": ["inhibitor"],
            "has_designations": True,
            "masking_type": "Double Blind",
            "allocation": "Randomized"
        }
        
        result = client.predict_trial_success_direct(
            trial_params=trial_params,
            return_id=True
        )
        
        print(f"Trial Parameters:")
        for key, value in trial_params.items():
            print(f"  - {key}: {value}")
        print()
        print(f"Prediction: {result['ref']['meta']['prediction']}")
        print(f"Probability: {result['ref']['meta']['probability']:.2%}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Example 5: Get PTRS statistics
    print("5. Getting PTRS statistics for Phase 3 trials...")
    print("-" * 80)
    try:
        stats = client.get_ptrs_stats(phase=3)
        print(f"Total Phase 3 trials: {stats['total_trials']}")
        print(f"Trials with endpoint data: {stats['trials_with_endpoint_data']}")
        print(f"Success rate (one endpoint): {stats['average_met_endpoints_one']:.2%}")
        print(f"Success rate (all endpoints): {stats['average_met_endpoints_all']:.2%}")
        print(f"Average arm size: {stats['average_arm_size']:.1f}")
        print(f"Trials with comparator: {stats['trials_with_comparator']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Example 6: Classify a disease
    print("6. Classifying a disease...")
    print("-" * 80)
    try:
        result = client.classify_disease("Non-small cell lung cancer")
        print(f"Disease: Non-small cell lung cancer")
        print(f"Disease classes: {result.get('disease_classes', [])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Close the client
    client.close()
    
    print("=" * 80)
    print("Example completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

