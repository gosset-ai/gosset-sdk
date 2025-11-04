"""
Gosset API Client

A Python client for interacting with the Gosset Drug Database API.
"""
import os
from typing import Optional, Dict, Any, List
import requests


class GossetAPIError(Exception):
    """Raised when the API returns an error response"""
    pass


class GossetClient:
    """
    Client for interacting with the Gosset Drug Database API.
    
    Args:
        api_key: Your Gosset API key (Bearer token). 
                 If not provided, will check GOSSET_API_KEY environment variable.
        base_url: API base URL. Defaults to https://api-dev.gosset.ai
        timeout: Request timeout in seconds. Defaults to 30.
    
    Example:
        >>> client = GossetClient(api_key="your_api_key")
        >>> trials = client.get_trials(phase="3", limit=10)
        >>> print(f"Found {trials['total']} trials")
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        self.api_key = api_key or os.environ.get("GOSSET_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via api_key parameter or "
                "set GOSSET_API_KEY environment variable."
            )
        
        base_url = base_url or os.environ.get("GOSSET_API_URL", "https://api.gosset.ai")
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an API request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            # Handle errors
            if response.status_code == 401:
                raise GossetAPIError("Authentication failed. Check your API key.")
            elif response.status_code == 429:
                raise GossetAPIError("Rate limit exceeded. Please try again later.")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', response.text)
                except:
                    error_msg = response.text
                raise GossetAPIError(f"API error ({response.status_code}): {error_msg}")
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise GossetAPIError(f"Request failed: {str(e)}")
    
    def get_trials(
        self,
        offset: int = 0,
        limit: int = 50,
        sort_by: str = "-completion_date",
        phase: Optional[str] = None,
        diseases: Optional[str] = None,
        targets: Optional[str] = None,
        modalities: Optional[str] = None,
        drug_names: Optional[str] = None,
        sponsor: Optional[str] = None,
        status: Optional[str] = None,
        masking_type: Optional[str] = None,
        allocation: Optional[str] = None,
        has_comparator: Optional[bool] = None,
        multi_arm: Optional[bool] = None,
        combination_therapy: Optional[bool] = None,
        has_success_data: Optional[bool] = None,
        has_designations: Optional[bool] = None,
        industry_only: Optional[bool] = None,
        completion_date_min: Optional[str] = None,
        completion_date_max: Optional[str] = None,
        avg_arm_size_min: Optional[int] = None,
        avg_arm_size_max: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get clinical trials with comprehensive filtering.
        
        Args:
            offset: Number of results to skip (for pagination)
            limit: Maximum number of results to return (max 100)
            sort_by: Field to sort by. Prefix with '-' for descending order
            phase: Trial phase(s), comma-separated (e.g., "2,3")
            diseases: Disease IDs, comma-separated
            targets: Target IDs, comma-separated
            modalities: Modality IDs, comma-separated
            drug_names: Drug IDs, comma-separated
            sponsor: Sponsor IDs, comma-separated
            status: Trial status(es), comma-separated
            masking_type: Masking type(s), comma-separated
            allocation: Allocation type(s), comma-separated
            has_comparator: Filter by trials with/without comparator
            multi_arm: Filter by trials with/without multiple arms
            combination_therapy: Filter by combination therapy trials
            has_success_data: Filter by trials with success data
            has_designations: Filter by trials with FDA designations
            industry_only: Filter for industry-sponsored trials only
            completion_date_min: Minimum completion date (YYYY-MM-DD)
            completion_date_max: Maximum completion date (YYYY-MM-DD)
            avg_arm_size_min: Minimum average arm size
            avg_arm_size_max: Maximum average arm size
            **kwargs: Additional filter parameters
        
        Returns:
            Dict containing:
                - results: List of trial objects
                - total: Total number of matching trials
                - offset: Current offset
                - limit: Current limit
                - stats: Aggregate statistics
        
        Example:
            >>> trials = client.get_trials(
            ...     phase="3",
            ...     has_comparator=True,
            ...     limit=10
            ... )
            >>> print(f"Found {trials['total']} trials")
            >>> for trial in trials['results']:
            ...     print(trial.get('nct_id'))
        """
        # Build request payload
        payload = {
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        
        # Add optional filters
        if phase is not None:
            payload["phase"] = phase
        if diseases is not None:
            payload["diseases"] = diseases
        if targets is not None:
            payload["targets"] = targets
        if modalities is not None:
            payload["modalities"] = modalities
        if drug_names is not None:
            payload["drug_names"] = drug_names
        if sponsor is not None:
            payload["sponsor"] = sponsor
        if status is not None:
            payload["status"] = status
        if masking_type is not None:
            payload["masking_type"] = masking_type
        if allocation is not None:
            payload["allocation"] = allocation
        if has_comparator is not None:
            payload["has_comparator"] = str(has_comparator).lower()
        if multi_arm is not None:
            payload["multi_arm"] = str(multi_arm).lower()
        if combination_therapy is not None:
            payload["combination_therapy"] = str(combination_therapy).lower()
        if has_success_data is not None:
            payload["has_success_data"] = str(has_success_data).lower()
        if has_designations is not None:
            payload["has_designations"] = str(has_designations).lower()
        if industry_only is not None:
            payload["industry_only"] = str(industry_only).lower()
        if completion_date_min is not None:
            payload["completion_date_min"] = completion_date_min
        if completion_date_max is not None:
            payload["completion_date_max"] = completion_date_max
        if avg_arm_size_min is not None:
            payload["avg_arm_size_min"] = avg_arm_size_min
        if avg_arm_size_max is not None:
            payload["avg_arm_size_max"] = avg_arm_size_max
        
        # Add any additional kwargs
        payload.update(kwargs)
        
        return self._request("POST", "/v2/trials/", data=payload)
    
    def predict_trial_success(
        self,
        query: str,
        return_id: bool = True
    ) -> Dict[str, Any]:
        """
        Predict clinical trial success probability from natural language description.
        
        This endpoint uses AI to extract structured parameters from your natural
        language description, then runs the ML model to predict success probability.
        
        Args:
            query: Natural language description of the trial
            return_id: If True, return only reference. If False, include full data
        
        Returns:
            Dict containing:
                - ref: Reference object with prediction results
                - extracted_parameters: Parameters extracted from the query
                - original_query: Your original query
        
        Example:
            >>> result = client.predict_trial_success(
            ...     query=\"\"\"Analyze the success probability for a Phase 3 trial 
            ...     of pembrolizumab in non-small cell lung cancer with PD-1 targeting, 
            ...     200 patients per arm, randomized double-blind design, has comparator 
            ...     (chemotherapy), monoclonal antibody, and includes biomarker selection 
            ...     (PD-L1 positive)\"\"\"
            ... )
            >>> print(f"Prediction: {result['ref']['meta']['prediction']}")
            >>> print(f"Probability: {result['ref']['meta']['probability']:.2%}")
        """
        if not query:
            raise ValueError("query is required")
        
        payload = {
            "query": query,
            "return_id": return_id
        }
        
        return self._request("POST", "/v2/trials/ptrs/predict/", data=payload)
    
    def predict_trial_success_direct(
        self,
        trial_params: Dict[str, Any],
        return_id: bool = True
    ) -> Dict[str, Any]:
        """
        Predict clinical trial success probability using structured parameters.
        
        This endpoint accepts pre-structured trial parameters and runs the ML model
        directly. It's faster than the natural language endpoint and has higher rate limits.
        
        Args:
            trial_params: Dictionary of trial parameters including:
                - highest_phase (float): 1.0, 2.0, 3.0, or 4.0
                - avg_arm_size (int): Average number of patients per arm
                - has_comparator (bool): Whether trial has a comparator arm
                - multi_arm (bool): Whether trial has multiple arms
                - combination_therapy (bool): Whether uses combination therapy
                - therapy_type (list): e.g., ["targeted"], ["non-targeted"]
                - targets (list): Molecular targets, e.g., ["EGFR", "PD-1"]
                - drug_names (list): Drug names
                - diseases (list): Disease/indication names
                - modalities (list): e.g., ["Monoclonal antibody"]
                - moa (list): Mechanisms of action, e.g., ["inhibitor"]
                - biomarkers (list): Biomarkers used
                - sponsors (list): Sponsor companies
                - industry_collaborators (bool): Has industry collaboration
                - has_designations (bool): Has FDA designations
                - masking_type (str): "Double Blind", "Single Blind", "Open Label", "None"
                - allocation (str): "Randomized", "Non-Randomized"
            return_id: If True, return only reference. If False, include full data
        
        Returns:
            Dict containing:
                - ref: Reference object with prediction results
        
        Example:
            >>> result = client.predict_trial_success_direct(
            ...     trial_params={
            ...         "highest_phase": 3.0,
            ...         "avg_arm_size": 200,
            ...         "has_comparator": True,
            ...         "therapy_type": ["targeted"],
            ...         "targets": ["PD-1"],
            ...         "diseases": ["non-small cell lung cancer"],
            ...         "modalities": ["Monoclonal antibody"],
            ...         "masking_type": "Double Blind",
            ...         "allocation": "Randomized"
            ...     }
            ... )
            >>> print(f"Prediction: {result['ref']['meta']['prediction']}")
            >>> print(f"Probability: {result['ref']['meta']['probability']:.2%}")
        """
        if not trial_params:
            raise ValueError("trial_params is required")
        
        payload = {
            "trial_params": trial_params,
            "return_id": return_id
        }
        
        return self._request("POST", "/v2/trials/ptrs/predict-direct/", data=payload)
    
    def classify_disease(
        self,
        disease_name: str,
        disease_desc: str = ""
    ) -> Dict[str, Any]:
        """
        Classify a disease to get disease class IDs.
        
        Args:
            disease_name: Name of the disease
            disease_desc: Optional description of the disease
        
        Returns:
            Dict containing:
                - disease_classes: List of disease class IDs
        
        Example:
            >>> result = client.classify_disease("Alopecia")
            >>> print(result['disease_classes'])
        """
        payload = {
            "disease_name": disease_name,
            "disease_desc": disease_desc
        }
        
        return self._request("POST", "/v2/trials/disease-class/", data=payload)
    
    def get_filters(self, doid: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available filter options for trials.
        
        Args:
            doid: Optional disease ID to filter options by
        
        Returns:
            Dict containing available filter values for:
                - phase
                - status
                - masking_type
                - allocation
                - primary_endpoints
                - line_of_treatment
                - inclusion_mutations
                - exclusion_mutations
                - biomarkers
                - stages
                - sponsor_class
                - therapy_type
                - actions
                - modality_classes
                - disease_classes
                - diseases
                - average_arm_size (with min/max)
        
        Example:
            >>> filters = client.get_filters()
            >>> print(f"Available phases: {filters['phase']}")
            >>> print(f"Available statuses: {filters['status']}")
        """
        params = {}
        if doid is not None:
            params["doid"] = doid
        
        return self._request("GET", "/v2/trials/filters/", params=params)
    
    def get_ptrs_stats(
        self,
        disease_classes: Optional[List[str]] = None,
        phase: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get aggregate trial statistics without returning individual trials.
        
        Args:
            disease_classes: List of disease class IDs to filter by
            phase: Phase number to filter by (1, 2, 3, or 4)
        
        Returns:
            Dict containing aggregate statistics:
                - total_trials
                - trials_with_endpoint_data
                - average_met_endpoints_one
                - average_met_endpoints_all
                - average_progressed
                - average_arm_size
                - trials_with_comparator
                - multi_arm_trials
                - trials_with_genomics
                - trials_with_biomarkers
        
        Example:
            >>> stats = client.get_ptrs_stats(phase=3)
            >>> print(f"Total Phase 3 trials: {stats['total_trials']}")
            >>> print(f"Success rate: {stats['average_met_endpoints_one']:.2%}")
        """
        payload = {}
        
        if disease_classes is not None:
            payload["disease_classes"] = disease_classes
        if phase is not None:
            payload["phase"] = phase
        
        return self._request("POST", "/v2/trials/ptrs/", data=payload)
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

