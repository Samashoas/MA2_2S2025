import sympy as sp
from sympy import symbols, pi, Piecewise
import matplotlib.pyplot as plt
import numpy as np

# Definir la variable simbólica
t = symbols('t')

# Definir la función original con T = 2π
# x(t) = {-t, -π < t < 0; t, 0 < t < π}
xt = Piecewise((-t, (t >= -pi) & (t < 0)), 
               (t, (t >= 0) & (t <= pi)))

print("Función definida:")
print("x(t) = -t para -π ≤ t < 0")
print("x(t) = t para 0 ≤ t ≤ π")
print("Período T = 2π")

# Calcular la serie de Fourier con período 2π
s = sp.fourier_series(xt, (t, -pi, pi))
s_truncated = s.truncate(10)  # Usar más términos para mejor aproximación

print("\nSerie de Fourier truncada (10 términos):")
print(s_truncated)

# Crear valores para graficar
t_vals = np.linspace(-3*np.pi, 3*np.pi, 2000)  # Graficamos 3 períodos

# Función original periódica
def original_function(t_val):
    # Normalizar al período [-π, π]
    t_normalized = ((t_val + np.pi) % (2*np.pi)) - np.pi
    
    result = np.zeros_like(t_val)
    
    # Para -π ≤ t < 0: x(t) = -t
    mask1 = (t_normalized >= -np.pi) & (t_normalized < 0)
    result[mask1] = -t_normalized[mask1]
    
    # Para 0 ≤ t ≤ π: x(t) = t
    mask2 = (t_normalized >= 0) & (t_normalized <= np.pi)
    result[mask2] = t_normalized[mask2]
    
    return result

# Convertir la serie de Fourier a función numérica
s_func = sp.lambdify(t, s_truncated, 'numpy')

# Crear la gráfica
plt.figure(figsize=(15, 8))

# Función original
plt.subplot(2, 2, 1)
plt.plot(t_vals, original_function(t_vals), 'b-', linewidth=2, label='Función original')
plt.title('Función Original x(t)\nx(t) = -t para -pi <= t < 0\nx(t) = t para 0 <= t <= pi')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
# Marcar los límites del período
for i in range(-3, 4):
    plt.axvline(x=i*np.pi, color='r', linestyle='--', alpha=0.5)

# Serie de Fourier
plt.subplot(2, 2, 2)
plt.plot(t_vals, original_function(t_vals), 'b--', alpha=0.7, linewidth=1, label='Función original')
plt.plot(t_vals, s_func(t_vals), 'r-', linewidth=2, label='Serie de Fourier (10 términos)')
plt.title('Aproximación con Serie de Fourier')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Zoom en un período
plt.subplot(2, 2, 3)
t_period = np.linspace(-np.pi, np.pi, 500)
plt.plot(t_period, original_function(t_period), 'b-', linewidth=3, label='Función original')
plt.plot(t_period, s_func(t_period), 'r--', linewidth=2, label='Serie de Fourier')
plt.title('Un Período: [-π, π]')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Error de aproximación
plt.subplot(2, 2, 4)
error = s_func(t_vals) - original_function(t_vals)
plt.plot(t_vals, error, 'g-', linewidth=1, label='Error de aproximación')
plt.title('Error: Serie de Fourier - Función Original')
plt.xlabel('t')
plt.ylabel('Error')
plt.grid(True)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)

plt.tight_layout()
plt.show()

# Mostrar los primeros coeficientes de Fourier
print("\nPrimeros coeficientes de Fourier:")
print("La función es impar, por lo que solo tiene términos seno:")
print("La serie debería ser de la forma: suma de bn*sin(nt) donde bn = 4/(n²π) para n impar")