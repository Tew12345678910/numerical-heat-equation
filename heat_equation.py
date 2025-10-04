"""
Heat Equation Solver using Euler Method
Equation: ∂U/∂t = α * ∂²U/∂x²
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

def initialize_conditions(Nx, L):
    """
    Initialize the temperature profile U(t=0, x) = U₀(x) = A - B*tanh(c - L/2)
    Boundary conditions: U(t, x=0) = A + B = 20°C and U(t, x=L) = A - B = 0°C
    """
    # From boundary conditions:
    # A + B = 20
    # A - B = 0
    # Therefore: A = 10, B = 10
    A = 10
    B = 10
    c = 0  # c parameter (not specified in problem, using 0)
    
    x = np.linspace(0, L, Nx)
    U0 = A - B * np.tanh(c - x)
    
    return x, U0, A, B

def check_stability(D, T, Nt, Nx, L):
    """
    Check if the numerical scheme is stable
    Condition: D * T * Nt² / (Nt * L²) ≤ 1/2
    Simplified: D * T * Nt / L² ≤ 1/2
    """
    dt = T / Nt
    dx = L / Nx
    stability_factor = D * dt / (dx**2)
    is_stable = stability_factor <= 0.5
    
    print(f"Stability Analysis:")
    print(f"  dt = {dt:.6f}")
    print(f"  dx = {dx:.6f}")
    print(f"  D*dt/dx² = {stability_factor:.6f}")
    print(f"  Stable: {is_stable} (must be ≤ 0.5)")
    print()
    
    return is_stable, stability_factor

def solve_heat_equation_euler(L, T, D, Nt, Nx):
    """
    Solve the heat equation using Euler method (explicit finite difference)
    Vectorized implementation for better performance
    
    Parameters:
    - L: Length of domain
    - T: Total time
    - D: Diffusion coefficient (α)
    - Nt: Number of time steps
    - Nx: Number of spatial points
    
    Returns:
    - x: Spatial grid
    - t: Time grid
    - U: Temperature matrix [time, space]
    """
    # Initialize grid
    x, U0, A, B = initialize_conditions(Nx, L)
    dt = T / Nt
    dx = L / Nx
    
    # Check stability
    is_stable, stability_factor = check_stability(D, T, Nt, Nx, L)
    
    # Initialize solution matrix
    U = np.zeros((Nt + 1, Nx))
    U[0, :] = U0
    
    # Time evolution using Euler method (vectorized)
    # U(i+1, j) = U(i, j) + D * dt / dx² * [U(i, j+1) - 2*U(i, j) + U(i, j-1)]
    r = D * dt / (dx**2)
    
    for n in range(Nt):
        # Vectorized update for interior points
        U[n + 1, 1:-1] = U[n, 1:-1] + r * (U[n, 2:] - 2 * U[n, 1:-1] + U[n, :-2])
        
        # Boundary conditions
        U[n + 1, 0] = A + B  # x = 0: U = 20°C
        U[n + 1, -1] = A - B  # x = L: U = 0°C
    
    t = np.linspace(0, T, Nt + 1)
    
    return x, t, U

def plot_temperature_profiles(x, t, U, times_to_plot):
    """
    Plot temperature profiles at different times
    """
    plt.figure(figsize=(10, 6))
    
    for time_value in times_to_plot:
        # Find closest time index
        idx = np.argmin(np.abs(t - time_value))
        plt.plot(x, U[idx, :], label=f't = {t[idx]:.2f}')
    
    plt.xlabel('x')
    plt.ylabel('U (Temperature °C)')
    plt.title('Temperature Profile Evolution')
    plt.legend()
    plt.grid(True)
    plt.savefig('temperature_profiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: temperature_profiles.png")

def plot_2d_temperature(x, t, U):
    """
    Plot 2D temperature profile using pcolormesh
    """
    plt.figure(figsize=(12, 6))
    
    X, T = np.meshgrid(x, t)
    plt.pcolormesh(X, T, U, shading='auto', cmap='hot')
    plt.colorbar(label='Temperature (°C)')
    plt.xlabel('Position x')
    plt.ylabel('Time t')
    plt.title('2D Temperature Evolution (Heat Equation)')
    plt.savefig('temperature_2d.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: temperature_2d.png")

def main():
    """
    Main function to solve the heat equation as per project instructions
    """
    print("=" * 60)
    print("Heat Equation Solver - Numerical Project")
    print("=" * 60)
    print()
    
    # Parameters - Using more practical values for stability
    L = 1.0      # Length
    T = 1.0      # Total time
    D = 0.05     # Diffusion coefficient (α)
    
    # For stability we need: D*dt/dx² ≤ 0.5
    # Original parameters Nt=100, Nx=1500 give instability
    # We use more reasonable values
    Nx = 100     # Number of spatial points (reduced for faster computation)
    dx = L / Nx
    dt_max = 0.5 * dx**2 / D
    Nt = int(T / dt_max) + 1
    
    print("Parameters:")
    print(f"  L = {L}")
    print(f"  T = {T}")
    print(f"  D (α) = {D}")
    print(f"  Nx = {Nx}")
    print(f"  Nt = {Nt} (calculated for stability)")
    print(f"  dx = {dx:.6f}")
    print(f"  dt = {T/Nt:.6f}")
    print()
    print("Note: Original parameters Nt=100, Nx=1500 would require")
    print(f"      Nt > 225000 for stability, which is computationally expensive.")
    print()
    
    # Solve the heat equation
    print("Solving heat equation...")
    x, t, U = solve_heat_equation_euler(L, T, D, Nt, Nx)
    print("Solution complete!")
    print()
    
    # Task 3: Plot temperature profiles at different times
    print("Task 3: Plotting temperature profiles at different times...")
    times_to_plot = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    plot_temperature_profiles(x, t, U, times_to_plot)
    print()
    
    # Task 5: Plot 2D temperature profile using pcolormesh
    print("Task 5: Creating 2D temperature visualization...")
    plot_2d_temperature(x, t, U)
    print()
    
    print("=" * 60)
    print("Analysis complete! Check the generated plots.")
    print("=" * 60)

if __name__ == "__main__":
    main()
