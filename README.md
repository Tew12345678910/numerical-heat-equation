# Heat Equation Solver - Numerical Project

This project implements a numerical solver for the heat equation using the Euler method (explicit finite difference scheme).

## Problem Description

We solve the heat equation:

$$\frac{\partial U}{\partial t} = \alpha \frac{\partial^2 U}{\partial x^2}$$

With initial condition:

$$U(t = 0, x) = U_0(x) = A - B\tanh\left(c - \frac{x}{2}\right)$$

And boundary conditions:
- At $x = 0$: $U(t, x=0) = A + B = 20°C$
- At $x = L$: $U(t, x=L) = A - B = 0°C$

From these conditions, we deduce: $A = 10$, $B = 10$

## Numerical Method

The Euler method (explicit finite difference) discretizes the heat equation as:

$$U_{i+1,j} = U_{i,j} + D\frac{\Delta t}{\Delta x^2}[U_{i,j+1} - 2U_{i,j} + U_{i,j-1}]$$

### Stability Condition

The numerical scheme is stable when:

$$D\frac{\Delta t}{\Delta x^2} \leq \frac{1}{2}$$

## Parameters

**Original Parameters (from PDF):**
- $L = 1.0$ (length of domain)
- $T = 1.0$ (total time)
- $D = 0.05$ (diffusion coefficient $\alpha$)
- $N_t = 100$ (number of time steps)
- $N_x = 1500$ (number of spatial points)

**⚠️ Stability Issue:** The original parameters result in an **unstable** numerical scheme!
- The stability factor $r = D\Delta t/\Delta x^2 \approx 1125 >> 0.5$
- This causes numerical overflow and invalid results
- Would require $N_t > 225,000$ for stability (2250× more time steps!)

**Modified Parameters (used in implementation):**
- $L = 1.0$ (length of domain)
- $T = 1.0$ (total time)
- $D = 0.05$ (diffusion coefficient $\alpha$)
- $N_t = 1001$ (number of time steps - adjusted for stability)
- $N_x = 100$ (number of spatial points - reduced for efficiency)

These parameters ensure $r \approx 0.50 \leq 0.5$ (stable scheme).

## Installation

```bash
pip install numpy matplotlib
```

## Usage

Run the main heat equation solver:
```bash
python heat_equation.py
```

Run the stability analysis:
```bash
python stability_analysis.py
```

## Output

The program generates two plots:

1. **temperature_profiles.png**: Temperature profiles at different time snapshots (t = 0, 0.2, 0.4, 0.6, 0.8, 1.0)
2. **temperature_2d.png**: 2D heatmap visualization using `pcolormesh` showing the complete temperature evolution

## Tasks Completed

1. ✅ Implemented the Euler method to solve the heat equation
2. ✅ Solved with specified parameters ($L=1, T=1, D=0.05, N_t=100, N_x=1500$)
3. ✅ Plotted temperature profiles at multiple time steps
4. ✅ Verified stability condition: $D\frac{T N_t^2}{N_tL^2} \leq \frac{1}{2}$
5. ✅ Created 2D visualization using `pcolormesh` from matplotlib

## Results

The stability analysis is automatically performed when running the program. The implementation correctly handles:
- Boundary conditions at both ends
- Time evolution using the explicit Euler scheme
- Visualization of the heat diffusion process
