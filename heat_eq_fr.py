import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

#Paramètres
L = 1.0           #longueur du couloir (m)
T = 1.0           #durée totale de la simulation (s)
D = 0.05          #coefficient de diffusion thermique (m²/s)

Nx = 100          #nombre de points spatiaux
Nt = 1500         #nombre de pas de temps (stable)
Nt_unstable = 50  #version instable pour comparaison

#Grilles d'espace et de temps / space and time grids
x = np.linspace(0, L, Nx) #array of Nx evenly spaced points between 0 and L
dx = x[1] - x[0] #spacing of two neighbours

#Constantes du problème (°C)
A = 10.0
B = 10.0

#Conditions aux limites / Given boundary conditions
U1 = A + B   # 20 °C ; U(t,x=0)
U2 = A - B  #  0 °C ; U(t,x=L)

#CONDITION INITIALE
def initial_profile(x):
    """ Profil initial : U(0, x) = A - B * tanh((x - L/2)/scale) """
    scale = 0.1  #contrôle la pente de la tanh
    return A - B * np.tanh((x - L/2) / scale)

U0 = initial_profile(x)

#EULER
def explicit_heat(U_init, Nx, Nt, L, T, D, U1, U2):
    """ ∂U/∂t = D ∂²U/∂x² """
    dx = L / (Nx - 1)
    dt = T / Nt
    alpha = D * dt / dx**2  #facteur de stabilité

    U_all = np.zeros((Nt + 1, Nx))
    U_all[0, :] = U_init.copy()

    U = U_init.copy()
    for n in range(Nt):
        U_new = U.copy()
        U_new[1:-1] = U[1:-1] + alpha * (U[2:] - 2 * U[1:-1] + U[:-2])
        #Conditions aux limites
        U_new[0] = U1
        U_new[-1] = U2
        U_all[n + 1] = U_new
        U = U_new

    return U_all, alpha, dt


#RÉSOLUTION ET TEST DE STABILITÉ
U_stable, alpha_stable, dt_stable = explicit_heat(U0, Nx, Nt, L, T, D, U1, U2)
U_unstable, alpha_unstable, dt_unstable = explicit_heat(U0, Nx, Nt_unstable, L, T, D, U1, U2)

print(f"dx = {dx:.5e}")
print(f"Stable case:   dt = {dt_stable:.5e}, alpha = {alpha_stable:.5e}")
print(f"Unstable case: dt = {dt_unstable:.5e}, alpha = {alpha_unstable:.5e}")


#VISUALISATIONS
# (a) Profils de température à différents instants
times_to_plot = np.arange(0, T + 1e-9, 0.1)
indices = (times_to_plot / dt_stable).round().astype(int)

plt.figure(figsize=(8, 5))
for t, idx in zip(times_to_plot, indices):
    plt.plot(x, U_stable[idx], label=f"t={t:.1f}s")
plt.xlabel("x (m)")
plt.ylabel("Température (°C)")
plt.title("Profils de température au cours du temps (schéma stable)")
plt.legend(fontsize="small")
plt.grid(True)
plt.show()

# (b) Comparaison schéma stable vs instable
plt.figure(figsize=(8, 5))
plt.plot(x, U_stable[-1], label=f"Stable (Nt={Nt}, α={alpha_stable:.3f})")
plt.plot(x, U_unstable[-1], '--', label=f"Instable (Nt={Nt_unstable}, α={alpha_unstable:.3f})")
plt.xlabel("x (m)")
plt.ylabel("Température (°C)")
plt.title("Comparaison à t = 1 s — Schéma stable vs instable")
plt.legend()
plt.grid(True)
plt.show()

# (c) Carte de chaleur U(x,t)
t_grid = np.linspace(0, T, Nt + 1)
X, Tgrid = np.meshgrid(x, t_grid)

plt.figure(figsize=(8, 5))
plt.pcolormesh(X, Tgrid, U_stable, shading='auto', cmap='hot')
plt.xlabel("x (m)")
plt.ylabel("t (s)")
plt.title("Évolution de la température U(x,t)")
plt.colorbar(label="Température (°C)")
plt.show()

# (d) Animation de l'évolution du profil
fig, ax = plt.subplots(figsize=(7, 4))
line, = ax.plot(x, U_stable[0])
ax.set_xlim(0, L)
ax.set_ylim(np.min(U_stable), np.max(U_stable))
ax.set_xlabel("x (m)")
ax.set_ylabel("Température (°C)")

def animate(frame):
    line.set_ydata(U_stable[frame])
    ax.set_title(f"Évolution du profil (t = {frame * dt_stable:.3f} s)")
    return (line,)

anim = animation.FuncAnimation(fig, animate, frames=np.arange(0, Nt+1, Nt//100), interval=50)
plt.show()

# (e) Vérification de la stabilité pour différentes valeurs de Nt
Nt_list = [50, 200, 500, 1000, 1500, 3000]
print("\nVérification de la condition de stabilité (α < 0.5):")
print("---------------------------------------------------")
for Nt_val in Nt_list:
    dt = T / Nt_val
    alpha = D * dt / dx**2
    print(f"Nt = {Nt_val:4d} -> α = {alpha:.4f}  {'(Stable)' if alpha < 0.5 else '(Instable)'}")
