import numpy as np
import matplotlib.pyplot as plt


def fractional_difference(y, alpha, dt):
    """
    Calcula a diferença fracionária usando o método de diferenças finitas fracionárias.


    Parâmetros:
    - y: Lista contendo os valores da série temporal.
    - alpha: Ordem fracionária para a derivada.
    - dt: Incremento de tempo.


    Retorna:
    - Valor fracionário calculado.
    """
    if len(y) >= 2:
        # Se houver pelo menos dois elementos em y, calcula a diferença fracionária.
        return (1 - alpha) * y[-1] + alpha * y[-2]
    else:
        # Se houver menos de dois elementos, retorna o último elemento.
        return y[-1]


# Parâmetros do modelo Lotka-Volterra
alpha = 0.1   # Taxa de crescimento das presas na ausência de predadores
beta = 0.02   # Taxa de predação (interação entre presas e predadores)
gamma = 0.1   # Taxa de diminuição dos predadores na ausência de presas
delta = 0.01  # Taxa de crescimento dos predadores em função das presas
q = 0.5       # Ordem fracionária para a derivada (pode ser ajustada conforme necessário)


# Condições iniciais
R0 = 40  # População inicial de coelhos (presas)
F0 = 9   # População inicial de raposas (predadores)


# Configuração do tempo
t_max = 200  # Tempo máximo de simulação
dt = 0.1     # Incremento de tempo (passo)
time_points = np.arange(0, t_max, dt)  # Lista de pontos temporais


# Inicialização das populações
R = np.zeros(len(time_points))  # Lista para armazenar a população de coelhos
F = np.zeros(len(time_points))  # Lista para armazenar a população de raposas
R[0] = R0  # População inicial de coelhos
F[0] = F0  # População inicial de raposas


# Método de diferenças finitas fracionárias para resolver EDFs
for i in range(1, len(time_points)):
    # Equações Lotka-Volterra discretizadas com derivadas fracionárias
    dRdt = alpha * R[i-1] - beta * R[i-1] * F[i-1] + delta * fractional_difference(R[:i], q, dt)
    dFdt = -gamma * F[i-1] + delta * R[i-1] * F[i-1] + delta * fractional_difference(F[:i], q, dt)


    # Atualização das populações usando o método de diferenças finitas fracionárias
    R[i] = R[i-1] + dt * dRdt
    F[i] = F[i-1] + dt * dFdt


# Criação de campos vetoriais
R_vec = np.linspace(min(R), max(R), 20)
F_vec = np.linspace(min(F), max(F), 20)
R_grid, F_grid = np.meshgrid(R_vec, F_vec)


dRdt_grid = alpha * R_grid - beta * R_grid * F_grid
dFdt_grid = -gamma * F_grid + delta * R_grid * F_grid


# Normalizando os vetores para melhor visualização
magnitude = np.sqrt(dRdt_grid**2 + dFdt_grid**2)
dRdt_grid /= magnitude
dFdt_grid /= magnitude


# Plotagem do gráfico bidimensional com campos vetoriais
plt.figure(figsize=(12, 6))


# Plotagem do campo vetorial
plt.quiver(R_grid, F_grid, dRdt_grid, dFdt_grid, scale=40, color='pink')


# Plotagem da evolução temporal de Coelhos e Raposas
plt.plot(R, F, label='Dinâmica Populacional', color='blue')
plt.title('Modelo Lotka-Volterra: Sistema Dinâmico Bidimensional com Campos Vetoriais')
plt.xlabel('População de Coelhos')
plt.ylabel('População de Raposas')
plt.legend()
plt.grid(True)
plt.show()