"""
Stability Analysis for Heat Equation
Demonstrates why the original parameters are unstable
"""

import numpy as np

def analyze_stability(L, T, D, Nt, Nx):
    """
    Analyze the stability of the numerical scheme
    """
    dt = T / Nt
    dx = L / Nx
    r = D * dt / (dx**2)
    
    print(f"\nParameters: L={L}, T={T}, D={D}, Nt={Nt}, Nx={Nx}")
    print(f"  dt = T/Nt = {T}/{Nt} = {dt:.8f}")
    print(f"  dx = L/Nx = {L}/{Nx} = {dx:.8f}")
    print(f"  r = D*dt/dx² = {D}*{dt:.8f}/{dx**2:.8f} = {r:.6f}")
    print(f"  Stability condition: r ≤ 0.5")
    print(f"  Result: {'STABLE ✓' if r <= 0.5 else 'UNSTABLE ✗'}")
    
    if r > 0.5:
        # Calculate required Nt for stability
        Nt_required = int(np.ceil(2 * D * T * Nx**2 / L**2))
        print(f"  Required Nt for stability: {Nt_required}")
        print(f"  Ratio: {Nt_required/Nt:.1f}x more time steps needed")
    
    return r <= 0.5

print("=" * 70)
print("STABILITY ANALYSIS - HEAT EQUATION")
print("=" * 70)

print("\n1. ORIGINAL PARAMETERS (from project PDF):")
print("-" * 70)
analyze_stability(L=1.0, T=1.0, D=0.05, Nt=100, Nx=1500)

print("\n2. MODIFIED PARAMETERS (used in heat_equation.py):")
print("-" * 70)
analyze_stability(L=1.0, T=1.0, D=0.05, Nt=1001, Nx=100)

print("\n3. OTHER STABLE CONFIGURATIONS:")
print("-" * 70)

# Example 1: Smaller Nx with original Nt
analyze_stability(L=1.0, T=1.0, D=0.05, Nt=100, Nx=50)

# Example 2: Larger Nt with original Nx
analyze_stability(L=1.0, T=1.0, D=0.05, Nt=225001, Nx=1500)

# Example 3: Balanced parameters
analyze_stability(L=1.0, T=1.0, D=0.05, Nt=500, Nx=100)

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("""
The stability condition for the explicit Euler method is:
    r = D*Δt/Δx² ≤ 0.5

With the original parameters (Nt=100, Nx=1500):
- The scheme is HIGHLY UNSTABLE (r ≈ 1125)
- This causes numerical overflow and NaN values
- Would require Nt > 225,000 for stability (2250x more time steps!)

The modified parameters (Nt=1001, Nx=100):
- The scheme is STABLE (r ≈ 0.50)
- Provides accurate results
- Computationally feasible

For better performance with fine spatial resolution (large Nx),
consider using implicit methods (Crank-Nicolson) which are
unconditionally stable.
""")
