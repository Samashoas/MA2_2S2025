import sympy as sp
from sympy import symbols
from sympy import fourier_series, pi, sin
import matplotlib.pyplot as plt
import numpy as np

# Definir la variable simbólica
t = symbols('t')

# Definir la función original (función escalón)
xt = sp.Piecewise((1, t < 1), (0, t > 1))

# Calcular la serie de Fourier
s = fourier_series(xt, (t, 0, 2))
s_truncated = s.scale(1).truncate(7)

print("Serie de Fourier truncada:")
print(s_truncated)

# Crear valores para graficar
t_vals = np.linspace(0, 4, 1000)  # Graficamos 2 períodos

# Función original
def original_function(t_val):
    return np.piecewise(t_val, 
                       [t_val % 2 < 1, t_val % 2 >= 1], 
                       [1, 0])

# Convertir la serie de Fourier a función numérica
s_func = sp.lambdify(t, s_truncated, 'numpy')

# Crear la gráfica
plt.figure(figsize=(12, 6))

# Función original
plt.subplot(1, 2, 1)
plt.plot(t_vals, original_function(t_vals), 'b-', linewidth=2, label='Función original')
plt.title('Función Original (Escalón)')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.ylim(-0.5, 1.5)

# Serie de Fourier
plt.subplot(1, 2, 2)
plt.plot(t_vals, original_function(t_vals), 'b--', alpha=0.7, label='Función original')
plt.plot(t_vals, s_func(t_vals), 'r-', linewidth=2, label='Serie de Fourier (7 términos)')
plt.title('Aproximación con Serie de Fourier')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.ylim(-0.5, 1.5)

plt.tight_layout()
plt.show()