# metrics/statistics.py
import numpy as np

def calculate_wigner_surmise_gue(s: np.ndarray) -> np.ndarray:
    """
    Calcula a distribuição teórica de Wigner para o GUE (Gaussian Unitary Ensemble).
    Muitas vezes associada à classe de universalidade quântica dos zeros da Zeta.
    Formula: P(s) = (32 / pi^2) * s^2 * exp(-4 * s^2 / pi)
    """
    return (32.0 / (np.pi ** 2)) * (s ** 2) * np.exp(-4.0 * (s ** 2) / np.pi)

def calculate_wigner_surmise_goe(s: np.ndarray) -> np.ndarray:
    """
    Calcula a distribuição teórica de Wigner para o GOE (Gaussian Orthogonal Ensemble).
    Formula: P(s) = (pi / 2) * s * exp(-pi * s^2 / 4)
    """
    return (np.pi / 2.0) * s * np.exp(-np.pi * (s ** 2) / 4.0)

def evaluate_spectral_distance(observed_gaps: np.ndarray) -> dict:
    """
    Métrica Quantitativa Pura (Axioma 3).
    Compara os gaps extraídos do motor do GER com os modelos estatísticos universais
    usando a distância L1 (erro absoluto integrado) ou erro quadrático médio (MSE).
    """
    if len(observed_gaps) == 0:
        return {"error": "Espectro vazio"}
        
    # Gera um histograma densidade dos gaps observados
    counts, bin_edges = np.histogram(observed_gaps, bins='auto', density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    
    # Curvas teóricas nos mesmos centros de bins
    theory_gue = calculate_wigner_surmise_gue(bin_centers)
    theory_goe = calculate_wigner_surmise_goe(bin_centers)
    theory_poisson = np.exp(-bin_centers) # Caso puramente aleatório / não correlacionado
    
    # Cálculo das distâncias (MSE)
    mse_gue = np.mean((counts - theory_gue) ** 2)
    mse_goe = np.mean((counts - theory_goe) ** 2)
    mse_poisson = np.mean((counts - theory_poisson) ** 2)
    
    return {
        "mse_gue": float(mse_gue),
        "mse_goe": float(mse_goe),
        "mse_poisson": float(mse_poisson)
    }
  
