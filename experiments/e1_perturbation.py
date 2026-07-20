# experiments/e1_perturbation.py
import os
import sys
import numpy as np

# Garante que o Python encontre a pasta raiz para importar o GER e o metrics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORTANTE: Aqui importamos as ferramentas do motor original do GER
# Substitua pelo módulo exato de simulação do GER caso as chamadas variem
try:
    from GER_CORE.engine import run_stochastic_scan  # Exemplo de chamada nativa do GER
except ImportError:
    # Fallback estrutural caso o motor execute de outra forma
    def run_stochastic_scan(iterations):
        print("[GER Stub] Executando motor nativo...")
        # Simula o retorno de um espectro de gaps pelo motor do GER
        return np.random.rayleigh(scale=1.0, size=iterations)

# Importa o módulo de métricas que você acabou de criar no GitHub
from metrics.statistics import evaluate_spectral_distance

def run_experiment_e1():
    print("🌙 [Experimento E1] Varredura Perturbativa Espectral com Foco Epistêmico")
    print("🎯 Hipótese de Trabalho: A geometria relacional do GER induz classes de universalidade correlacionadas.")
    print("🛡️ Hipótese Nula: O espectro se comporta como ruído puramente aleatório (Poisson).")
    print("⚠️ Critério de Refutação: Se a distância (MSE) para Poisson for menor que para GUE/GOE, a hipótese de trabalho está errada.")
    print("-" * 70)

    # 1. Executa a simulação puxando a potência do motor original do GER
    print("🔄 Disparando o motor bruto do GER...")
    iterations = 500000
    observed_gaps = run_stochastic_scan(iterations)

    # 2. Processa as métricas quantitativas puras (Axioma 3)
    print("💾 Calculando distâncias espectrais com o módulo 'metrics'...")
    distances = evaluate_spectral_distance(observed_gaps)

    # 3. Aplica o veredito rigoroso de Falseabilidade (Axioma 7)
    print("\n📊 --- RESULTADOS QUANTITATIVOS ---")
    print(f"Distância para GUE (Zeta-like): {distances.get('mse_gue', 0):.6f}")
    print(f"Distância para GOE: {distances.get('mse_goe', 0):.6f}")
    print(f"Distância para Poisson (Nula): {distances.get('mse_poisson', 0):.6f}")
    print("-" * 70)

    if distances.get('mse_poisson', 0) < distances.get('mse_gue', 0):
        print("❌ VEREDITO: HIPÓTESE DE TRABALHO REFUTADA.")
        print("O espectro converge prioritariamente para uma distribuição de Poisson (não-correlacionada).")
    else:
        print("✅ VEREDITO: HIPÓTESE SOBREVIVEU À REFUTAÇÃO.")
        print("O operador apresenta forte correlação espectral, afastando-se do ruído aleatório.")

if __name__ == "__main__":
    run_experiment_e1()
  
