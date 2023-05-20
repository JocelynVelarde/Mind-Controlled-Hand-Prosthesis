import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Definir tres vectores de ejemplo
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
v3 = np.array([7, 8, 9])

# Definir los valores de p para la desigualdad de Minkowski
p_values = [1, 2, 3]

# Crear un grafo vacío
G = nx.Graph()

# Agregar los nodos al grafo
G.add_node('v1')
G.add_node('v2')
G.add_node('v3')

# Calcular la distancia Minkowski para cada par de vectores
for i in range(len(p_values)):
    for j in range(i+1, len(p_values)):
        p = p_values[i]
        q = p_values[j]
        d12 = np.power(np.sum(np.power(np.abs(v1 - v2), p)), 1/p)
        d13 = np.power(np.sum(np.power(np.abs(v1 - v3), p)), 1/p)
        d23 = np.power(np.sum(np.power(np.abs(v2 - v3), p)), 1/p)
        # Agregar las aristas al grafo
        G.add_edge('v1', 'v2', weight=d12, p=p)
        G.add_edge('v1', 'v3', weight=d13, p=p)
        G.add_edge('v2', 'v3', weight=d23, p=p)

# Dibujar el grafo
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='b', node_size=500)
nx.draw_networkx_edges(G, pos, edge_color='k', width=1)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
plt.axis('off')
plt.title('Distancias Minkowski entre tres vectores en un espacio de 3 dimensiones')
plt.show()
