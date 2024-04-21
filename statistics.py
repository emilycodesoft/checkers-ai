import matplotlib.pyplot as plt

# Suponiendo que tienes los datos de partidas en dos arrays llamados jugador1 y jugador2
# Ejemplo de datos
jugador1 = [1, 1, 0, 2, 1, 2, 0, 1, 0, 1]  # 1: ganado, 2: perdido, 0: empate
jugador2 = [2, 2, 1, 1, 2, 1, 0, 2, 0, 2]

# Crear una lista para representar los estados de los juegos
estados = ['Ganado', 'Perdido', 'Empatado']

# Crear una lista de colores para representar a cada jugador
colores = ['blue', 'red']

# Crear el gráfico
plt.figure(figsize=(10, 6))

# Iterar sobre los juegos y dibujar la evolución de los resultados
for i in range(len(jugador1) - 1):
    plt.plot([i, i+1], [jugador1[i], jugador1[i+1]], color=colores[0], label='Jugador 1' if i == 0 else None)
    plt.plot([i, i+1], [jugador2[i], jugador2[i+1]], color=colores[1], label='Jugador 2' if i == 0 else None)

# Configurar los ejes y etiquetas
plt.xlabel('Juego')
plt.ylabel('Resultado')
plt.title('Evolución de los resultados de las partidas')
plt.xticks(range(len(jugador1)), range(1, len(jugador1) + 1))
plt.yticks(range(3), estados)
plt.grid(True)
plt.legend()

# Mostrar el gráfico
plt.show()
