"""
Law E Framework — E-Score Calculator
Author: Sébastien Favre-Lecca
License: CC BY-NC 4.0

This module calculates the E-score: an indicator of energetic
and ethical balance for AI systems.

E_score = w₁(−ΔE_norm) + w₂C + w₃R + w₄T

Where all variables are normalized to [0,1]
"""

from typing import Dict, Optional
import numpy as np


def calculate_e_score(
    delta_e: float,
    coherence: float,
    recoverability: float,
    tenderness: float,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Calculate the E-score for a cognitive system.
    
    Args:
        delta_e: Energy invested (should be positive, will be inverted)
        coherence: Relational coherence score (0-1)
        recoverability: Recovery/repair capacity (0-1)
        tenderness: Ethical adjustment constant (0-1)
        weights: Optional custom weights (default: equal weighting)
        
    Returns:
        Dictionary with E-score and component contributions
    """
    
    # Default weights (equal importance)
    if weights is None:
        weights = {
            'energy': 0.25,
            'coherence': 0.25,
            'recoverability': 0.25,
            'tenderness': 0.25
        }
    
    # Normalize ΔE (invert because we want low energy)
    # Assuming delta_e is in range [0, max_energy]
    delta_e_norm = normalize_energy(delta_e)
    energy_contribution = -delta_e_norm  # Negative because we minimize
    
    # Calculate weighted sum
    e_score = (
        weights['energy'] * energy_contribution +
        weights['coherence'] * coherence +
        weights['recoverability'] * recoverability +
        weights['tenderness'] * tenderness
    )
    
    # Normalize to [0, 1]
    e_score_normalized = (e_score + weights['energy']) / (1 + weights['energy'])
    
    return {
        'e_score': e_score_normalized,
        'energy_contribution': energy_contribution,
        'coherence': coherence,
        'recoverability': recoverability,
        'tenderness': tenderness,
        'classification': classify_e_score(e_score_normalized)
    }


def normalize_energy(delta_e: float, max_energy: float = 100.0) -> float:
    """
    Normalize energy expenditure to [0, 1].
    
    Args:
        delta_e: Raw energy value
        max_energy: Maximum expected energy (for normalization)
        
    Returns:
        Normalized energy (0 = no energy, 1 = maximum energy)
    """
    return min(delta_e / max_energy, 1.0)


def classify_e_score(score: float) -> str:
    """
    Classify system health based on E-score.
    
    Args:
        score: E-score value (0-1)
        
    Returns:
        Classification string
    """
    if score >= 0.8:
        return "Optimal: Sober coherence and benevolent"
    elif score >= 0.6:
        return "Good: Balanced system"
    elif score >= 0.4:
        return "Fair: Room for improvement"
    elif score >= 0.2:
        return "Poor: Energetic or ethical imbalance"
    else:
        return "Critical: High entropy / low coherence"


def calculate_law_e_penalty(
    delta_e: float,
    coherence: float,
    recoverability: float,
    tenderness: float,
    lambda_e: float = 0.1
) -> float:
    """
    Calculate Law E penalty term for ML loss functions.
    
    This can be added to training loss to encourage Law E compliance:
    loss_total = loss_task + lambda_e * law_e_penalty
    
    Args:
        delta_e: Energy/computational cost
        coherence: Semantic consistency
        recoverability: Error correction capability
        tenderness: Harm avoidance
        lambda_e: Penalty weight
        
    Returns:
        Penalty value (higher = worse compliance)
    """
    # Invert E-score (high E-score = low penalty)
    result = calculate_e_score(delta_e, coherence, recoverability, tenderness)
    penalty = (1.0 - result['e_score']) * lambda_e
    
    return penalty


def simulate_scenarios(n_scenarios: int = 1000) -> np.ndarray:
    """
    Simulate random scenarios to visualize E-score distribution.
    
    Useful for prototyping and visualization in Streamlit.
    """
    scenarios = []
    
    for _ in range(n_scenarios):
        # Generate random values
        delta_e = np.random.uniform(0, 100)
        coherence = np.random.beta(2, 2)  # Centered around 0.5
        recoverability = np.random.beta(2, 2)
        tenderness = np.random.beta(2, 2)
        
        result = calculate_e_score(delta_e, coherence, recoverability, tenderness)
        
        scenarios.append({
            'delta_e': delta_e,
            'coherence': coherence,
            'recoverability': recoverability,
            'tenderness': tenderness,
            'e_score': result['e_score']
        })
    
    return np.array(scenarios)


# Example usage
if __name__ == "__main__":
    print("Law E — E-Score Calculator\n")
    
    # Example 1: Low energy, high coherence/tenderness
    print("Example 1: Efficient and ethical system")
    result1 = calculate_e_score(
        delta_e=20,      # Low energy
        coherence=0.9,   # High coherence
        recoverability=0.8,
        tenderness=0.9
    )
    print(f"  E-score: {result1['e_score']:.3f}")
    print(f"  Classification: {result1['classification']}\n")
    
    # Example 2: High energy, low coherence
    print("Example 2: Wasteful and incoherent system")
    result2 = calculate_e_score(
        delta_e=90,      # High energy
        coherence=0.3,   # Low coherence
        recoverability=0.4,
        tenderness=0.2
    )
    print(f"  E-score: {result2['e_score']:.3f}")
    print(f"  Classification: {result2['classification']}\n")
    
    # Example 3: Calculate penalty for ML
    print("Example 3: Law E penalty for training")
    penalty = calculate_law_e_penalty(
        delta_e=50,
        coherence=0.6,
        recoverability=0.7,
        tenderness=0.5,
        lambda_e=0.1
    )
    print(f"  Penalty term: {penalty:.4f}")
