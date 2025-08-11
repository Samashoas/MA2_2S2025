import sympy as sp
from sympy import symbols, pi, Piecewise, fourier_series, integrate, cos, sin
import matplotlib.pyplot as plt
import numpy as np

# Definir la variable simbólica
t = symbols('t')

# Definir la función original con T = 2π (período de 0 a 2π)
# f(t) = {t², 0 ≤ t < π; 0, π < t ≤ 2π}
ft = Piecewise((t**2, (t >= 0) & (t < pi)), 
               (0, (t > pi) & (t <= 2*pi)))

# Calcular los coeficientes de Fourier manualmente
print("Calculando coeficientes de Fourier...")

# a0 (componente DC)
a0 = (1/pi) * integrate(t**2, (t, 0, pi))
print(f"a0 = {a0}")

# Coeficientes an
def calcular_an(n):
    return (1/pi) * integrate(t**2 * cos(n*t), (t, 0, pi))

# Coeficientes bn (serán cero por simetría)
def calcular_bn(n):
    return (1/pi) * integrate(t**2 * sin(n*t), (t, 0, pi))

# Calcular los primeros coeficientes
coeficientes_a = [float(a0)]
coeficientes_b = [0]

for n in range(1, 7):
    an = calcular_an(n)
    bn = calcular_bn(n)
    coeficientes_a.append(float(an))
    coeficientes_b.append(float(bn))
    print(f"a{n} = {an}, b{n} = {bn}")

# Crear valores para graficar
t_vals = np.linspace(-6*np.pi, 6*np.pi, 2000)

# Función original periódica
def original_function(t_val):
    # Normalizar al período [0, 2π]
    t_normalized = t_val % (2*np.pi)
    
    result = np.zeros_like(t_val)
    
    # Para 0 ≤ t < π: f(t) = t²
    mask1 = (t_normalized >= 0) & (t_normalized < np.pi)
    result[mask1] = t_normalized[mask1]**2
    
    # Para π < t ≤ 2π: f(t) = 0
    mask2 = (t_normalized > np.pi) & (t_normalized <= 2*np.pi)
    result[mask2] = 0
    
    # En t = π (discontinuidad), valor promedio
    mask_disc = np.abs(t_normalized - np.pi) < 0.01
    result[mask_disc] = np.pi**2 / 2
    
    return result

# Función de la serie de Fourier usando los coeficientes calculados
def serie_fourier(t_val, n_terms=6):
    result = coeficientes_a[0] / 2  # a0/2
    
    for n in range(1, min(n_terms, len(coeficientes_a))):
        result += coeficientes_a[n] * np.cos(n * t_val)
        result += coeficientes_b[n] * np.sin(n * t_val)
    
    return result

# Crear la serie matemática formateada (valores aproximados)
a0_val = float(a0)
a1_val = float(calcular_an(1))
a2_val = float(calcular_an(2))
a3_val = float(calcular_an(3))
a4_val = float(calcular_an(4))
a5_val = float(calcular_an(5))

serie_matematica_linea1 = f'${a0_val/2:.3f} + {a1_val:.3f}\\cos(t) + {a2_val:.3f}\\cos(2t) + {a3_val:.3f}\\cos(3t) + {a4_val:.3f}\\cos(4t) + {a5_val:.3f}\\cos(5t) + \\cdots$'

serie_completa_matematica = (
    r'$f(t) = \frac{\pi^2}{3} + \sum_{n=1}^{\infty} \frac{4(-1)^n}{n^2}\cos(nt)$'
)

# Crear la gráfica con espacio adicional para la serie
fig = plt.figure(figsize=(16, 14))

# Crear un layout con espacio para mostrar la serie
gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 2, 2], hspace=0.5, wspace=0.3)

# Título principal
ax_title = fig.add_subplot(gs[0, :])
ax_title.text(0.5, 0.7, 'SERIE DE FOURIER - FUNCIÓN CUADRÁTICA A TROZOS', 
            ha='center', va='center', fontsize=18, fontweight='bold',
            transform=ax_title.transAxes)
ax_title.text(0.5, 0.3, 'f(t) = t² para 0 ≤ t < π;  f(t) = 0 para π < t ≤ 2π', 
            ha='center', va='center', fontsize=14,
            transform=ax_title.transAxes)
ax_title.axis('off')

# Mostrar la serie de Fourier con formato matemático
ax_serie = fig.add_subplot(gs[1, :])
ax_serie.text(0.5, 0.8, 'Serie de Fourier (primeros términos):', 
            ha='center', va='center', fontsize=14, fontweight='bold',
            transform=ax_serie.transAxes)

# Primera línea con los primeros términos calculados
ax_serie.text(0.5, 0.5, serie_matematica_linea1, 
            ha='center', va='center', fontsize=10, 
            transform=ax_serie.transAxes, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

# Serie completa con notación matemática teórica
ax_serie.text(0.5, 0.1, serie_completa_matematica, 
            ha='center', va='center', fontsize=12, 
            transform=ax_serie.transAxes)
ax_serie.axis('off')

# Función original
ax1 = fig.add_subplot(gs[2, 0])
ax1.plot(t_vals, original_function(t_vals), 'b-', linewidth=2, label='Función original')
ax1.set_title('Función Original f(t) - Cuadrática a Trozos', fontsize=12, fontweight='bold')
ax1.set_xlabel('t')
ax1.set_ylabel('f(t)')
ax1.grid(True)
ax1.legend()
ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
# Marcar los límites del período
for i in range(-3, 4):
    ax1.axvline(x=i*2*np.pi, color='r', linestyle='--', alpha=0.5)
    ax1.axvline(x=i*2*np.pi + np.pi, color='g', linestyle=':', alpha=0.5)

# Serie de Fourier
ax2 = fig.add_subplot(gs[2, 1])
ax2.plot(t_vals, original_function(t_vals), 'b--', alpha=0.7, linewidth=1, label='Función original')
ax2.plot(t_vals, serie_fourier(t_vals), 'r-', linewidth=2, label='Serie de Fourier (6 términos)')
ax2.set_title('Aproximación con Serie de Fourier', fontsize=12, fontweight='bold')
ax2.set_xlabel('t')
ax2.set_ylabel('f(t)')
ax2.grid(True)
ax2.legend()
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Zoom en un período
ax3 = fig.add_subplot(gs[3, 0])
t_period = np.linspace(0, 2*np.pi, 1000)
ax3.plot(t_period, original_function(t_period), 'b-', linewidth=3, label='Función original')
ax3.plot(t_period, serie_fourier(t_period), 'r--', linewidth=2, label='Serie de Fourier')
ax3.set_title('Un Período: [0, 2π]', fontsize=12, fontweight='bold')
ax3.set_xlabel('t')
ax3.set_ylabel('f(t)')
ax3.grid(True)
ax3.legend()
ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax3.axvline(x=np.pi, color='g', linestyle=':', alpha=0.7)
ax3.set_xlim(0, 2*np.pi)

# Espectro de amplitud
ax4 = fig.add_subplot(gs[3, 1])
frequencies = []
amplitudes = []

# Componente DC
frequencies.append(0)
amplitudes.append(abs(coeficientes_a[0]/2))

# Coeficientes calculados
for n in range(1, len(coeficientes_a)):
    freq = n / (2*np.pi)
    frequencies.append(freq)
    # Magnitud del coeficiente
    amp = np.sqrt(coeficientes_a[n]**2 + coeficientes_b[n]**2)
    amplitudes.append(abs(amp))

ax4.stem(frequencies, amplitudes, linefmt='b-', markerfmt='bo', basefmt='k-')
ax4.set_title('Espectro de Amplitud', fontsize=12, fontweight='bold')
ax4.set_xlabel('Frecuencia (Hz)')
ax4.set_ylabel('Amplitud')
ax4.grid(True)
ax4.set_xlim(-0.1, 0.8)

# Añadir información de características
info_text = (
    "Características:\n"
    f"• Componente DC: a₀/2 = {coeficientes_a[0]/2:.3f}\n"
    "• Solo términos coseno (bₙ = 0)\n"
    "• Período: T = 2π"
)

ax4.text(0.02, 0.98, info_text, transform=ax4.transAxes, fontsize=9,
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
         facecolor="lightyellow", alpha=0.8))

plt.show()