import sympy as sp
from sympy import symbols, pi, Piecewise, fourier_series
import matplotlib.pyplot as plt
import numpy as np

# Definir la variable simbólica
t = symbols('t')

# Definir la función original con T = 10 (período de -5 a 5)
# f(t) = {0, -5 < t < 0; 1, 0 < t < 5}
ft = Piecewise((0, (t > -5) & (t < 0)), 
               (1, (t > 0) & (t < 5)))

# Calcular la serie de Fourier con período 10
s = fourier_series(ft, (t, -5, 5))
s_truncated = s.truncate(6)  # Usar 6 términos para mejor aproximación

# Crear valores para graficar
t_vals = np.linspace(-15, 15, 2000)  # Graficamos 3 períodos

# Función original periódica
def original_function(t_val):
    # Normalizar al período [-5, 5]
    t_normalized = ((t_val + 5) % 10) - 5
    
    result = np.zeros_like(t_val)
    
    # Para -5 < t < 0: f(t) = 0
    mask1 = (t_normalized > -5) & (t_normalized < 0)
    result[mask1] = 0
    
    # Para 0 < t < 5: f(t) = 1
    mask2 = (t_normalized > 0) & (t_normalized < 5)
    result[mask2] = 1
    
    # En t = 0, t = ±5 (discontinuidades), valor promedio = 0.5
    mask_disc = np.abs(t_normalized % 5) < 0.01
    result[mask_disc] = 0.5
    
    return result

# Convertir la serie de Fourier a función numérica
s_func = sp.lambdify(t, s_truncated, 'numpy')

# Crear la serie matemática formateada CORREGIDA
# Los argumentos deben ser πt/5, 3πt/5, etc. según el período T=10
serie_matematica_linea1 = r'$\frac{2\sin\left(\frac{\pi t}{5}\right)}{\pi} + \frac{2\sin\left(\frac{3\pi t}{5}\right)}{3\pi} + \frac{2\sin\left(\frac{5\pi t}{5}\right)}{5\pi} + \frac{2\sin\left(\frac{7\pi t}{5}\right)}{7\pi} + \frac{2\sin\left(\frac{9\pi t}{5}\right)}{9\pi} + \frac{2\sin\left(\frac{11\pi t}{5}\right)}{11\pi} + \frac{1}{2}$'

serie_completa_matematica = (
    r'$f(t) = \frac{1}{2} + \frac{2}{\pi}\left[\sin\left(\frac{\pi t}{5}\right) + \frac{1}{3}\sin\left(\frac{3\pi t}{5}\right) + \frac{1}{5}\sin\left(\frac{5\pi t}{5}\right) + '
    r'\frac{1}{7}\sin\left(\frac{7\pi t}{5}\right) + \frac{1}{9}\sin\left(\frac{9\pi t}{5}\right) + \frac{1}{11}\sin\left(\frac{11\pi t}{5}\right) + \cdots\right]$'
)

# Crear la gráfica con espacio adicional para la serie
fig = plt.figure(figsize=(16, 14))

# Crear un layout con espacio para mostrar la serie
gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 2, 2], hspace=0.5, wspace=0.3)

# Título principal
ax_title = fig.add_subplot(gs[0, :])
ax_title.text(0.5, 0.7, 'SERIE DE FOURIER - FUNCIÓN ESCALÓN', 
            ha='center', va='center', fontsize=18, fontweight='bold',
            transform=ax_title.transAxes)
ax_title.text(0.5, 0.3, 'f(t) = 0 para -5 < t < 0;  f(t) = 1 para 0 < t < 5', 
            ha='center', va='center', fontsize=14,
            transform=ax_title.transAxes)
ax_title.axis('off')

# Mostrar la serie de Fourier con formato matemático
ax_serie = fig.add_subplot(gs[1, :])
ax_serie.text(0.5, 0.8, 'Serie de Fourier (primeros términos):', 
            ha='center', va='center', fontsize=14, fontweight='bold',
            transform=ax_serie.transAxes)

# Primera línea con los primeros 6 términos más la constante
ax_serie.text(0.5, 0.5, serie_matematica_linea1, 
            ha='center', va='center', fontsize=11, 
            transform=ax_serie.transAxes, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

# Serie completa con notación matemática
ax_serie.text(0.5, 0.1, serie_completa_matematica, 
            ha='center', va='center', fontsize=10, 
            transform=ax_serie.transAxes)
ax_serie.axis('off')

# Función original
ax1 = fig.add_subplot(gs[2, 0])
ax1.plot(t_vals, original_function(t_vals), 'b-', linewidth=2, label='Función original')
ax1.set_title('Función Original f(t) - Escalón', fontsize=12, fontweight='bold')
ax1.set_xlabel('t')
ax1.set_ylabel('f(t)')
ax1.grid(True)
ax1.legend()
ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
# Marcar los límites del período
for i in range(-3, 4):
    ax1.axvline(x=i*5, color='r', linestyle='--', alpha=0.5)

# Serie de Fourier
ax2 = fig.add_subplot(gs[2, 1])
ax2.plot(t_vals, original_function(t_vals), 'b--', alpha=0.7, linewidth=1, label='Función original')
ax2.plot(t_vals, s_func(t_vals), 'r-', linewidth=2, label='Serie de Fourier (6 términos)')
ax2.set_title('Aproximación con Serie de Fourier', fontsize=12, fontweight='bold')
ax2.set_xlabel('t')
ax2.set_ylabel('f(t)')
ax2.grid(True)
ax2.legend()
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Zoom en un período
ax3 = fig.add_subplot(gs[3, 0])
t_period = np.linspace(-5, 5, 1000)
ax3.plot(t_period, original_function(t_period), 'b-', linewidth=3, label='Función original')
ax3.plot(t_period, s_func(t_period), 'r--', linewidth=2, label='Serie de Fourier')
ax3.set_title('Un Período: [-5, 5]', fontsize=12, fontweight='bold')
ax3.set_xlabel('t')
ax3.set_ylabel('f(t)')
ax3.grid(True)
ax3.legend()
ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax3.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Espectro de amplitud
ax4 = fig.add_subplot(gs[3, 1])
n_harmonics = 10
frequencies = []
amplitudes = []

# Para función escalón: bn = 2/(n*pi) para n impar, 0 para n par
# a0 = 1/2 (componente DC)
frequencies.append(0)
amplitudes.append(0.5)

for n in range(1, n_harmonics + 1):
    freq = n / 10  # frecuencia fundamental = 1/T = 1/10
    frequencies.append(freq)
    
    if n % 2 == 1:  # n impar
        amp = 2 / (n * np.pi)
        amplitudes.append(amp)
    else:  # n par
        amplitudes.append(0)

ax4.stem(frequencies, amplitudes, linefmt='b-', markerfmt='bo', basefmt='k-')
ax4.set_title('Espectro de Amplitud', fontsize=12, fontweight='bold')
ax4.set_xlabel('Frecuencia (Hz)')
ax4.set_ylabel('Amplitud')
ax4.grid(True)
ax4.set_xlim(-0.1, 1.1)

# Añadir información de características
info_text = (
    "Características:\n"
    "• Componente DC: a₀ = 1/2\n"
    "• Coeficientes: bₙ = 2/(nπ) para n impar\n"
    "• Período: T = 10"
)

ax4.text(0.02, 0.98, info_text, transform=ax4.transAxes, fontsize=9,
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
         facecolor="lightyellow", alpha=0.8))

# Solo mostrar la imagen, sin guardar
plt.show()