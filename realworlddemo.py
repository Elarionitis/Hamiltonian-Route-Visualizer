import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
from itertools import permutations
import matplotlib.lines as mlines

st.set_page_config(page_title="Delivery Route Planner - Dirac’s Theorem", layout="wide")

st.title("🚚 Delivery Route Planner using Dirac’s Theorem")
st.markdown("""
This interactive demo models a **delivery network**, where each node represents a delivery location.  
It demonstrates how **Dirac’s Theorem** guarantees a **Hamiltonian Cycle** (a full delivery loop)  
when the network is well-connected, and compares it with a **real-world route heuristic**.
""")

st.sidebar.header("🔧 Configuration")
n = st.sidebar.slider("Number of delivery locations", 4, 10, 6)
radius = st.sidebar.slider("Connection distance (road threshold)", 0.1, 0.6, 0.3)
seed = st.sidebar.number_input("Random Seed (city layout)", value=42, step=1)
random.seed(seed)

coords = [(random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)) for _ in range(n)]
G = nx.Graph()
labels = [chr(65 + i) for i in range(n)]
for i, p in enumerate(coords):
    G.add_node(labels[i], pos=p)

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

for i in range(n):
    for j in range(i + 1, n):
        if distance(coords[i], coords[j]) <= radius:
            G.add_edge(labels[i], labels[j], weight=round(distance(coords[i], coords[j]), 2))

degrees = dict(G.degree())
dirac_ok = all(deg >= n / 2 for deg in degrees.values())

def find_hamiltonian(graph):
    nodes = list(graph.nodes)
    if len(nodes) > 9:
        return None
    for perm in permutations(nodes):
        if all(graph.has_edge(perm[i], perm[i + 1]) for i in range(len(nodes) - 1)) and graph.has_edge(perm[-1], perm[0]):
            return perm + (perm[0],)
    return None

ham_cycle = find_hamiltonian(G)

def nearest_neighbor(graph, start):
    nodes = list(graph.nodes)
    unvisited = set(nodes)
    unvisited.remove(start)
    route = [start]
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda x: distance(G.nodes[current]['pos'], G.nodes[x]['pos']))
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    route.append(start)
    return route

heuristic_route = nearest_neighbor(G, labels[0])

def total_distance(route):
    d = 0
    for i in range(len(route) - 1):
        p1, p2 = G.nodes[route[i]]['pos'], G.nodes[route[i + 1]]['pos']
        d += distance(p1, p2)
    return round(d, 3)

col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.subheader("📋 Summary")
    st.write(f"**Delivery locations:** {n}")
    st.write(f"**Dirac’s Condition:** {'✅ Satisfied' if dirac_ok else '❌ Not satisfied'}")
    st.write(f"**Degrees:** {degrees}")

    if ham_cycle:
        st.success(f"✅ Hamiltonian Route Found: {' → '.join(ham_cycle)}")
        st.write(f"**Total Distance:** {total_distance(ham_cycle)}")
    else:
        st.warning("⚠️ No Hamiltonian cycle found — the network isn't dense enough.")
    
    st.markdown("---")
    st.write("**Heuristic (Greedy) Route:**")
    st.info(" → ".join(heuristic_route))
    st.write(f"**Total Distance:** {total_distance(heuristic_route)}")

with col2:
    st.subheader("🗺️ Delivery Network Visualization")

    pos = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor("#eaf2ff")

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            dist = distance(coords[i], coords[j])
            color = "#B0BEC5"
            style = ':' if dist > radius else '-'
            ax.plot([x1, x2], [y1, y2], color=color, linestyle=style, linewidth=1)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="#1976D2", edgecolors="white")
    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color="#42A5F5", width=2)

    if ham_cycle:
        edges = list(zip(ham_cycle, ham_cycle[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=3)
        st.success("✅ Hamiltonian Cycle Detected — Full Delivery Loop Found!")
    else:
        edges = list(zip(heuristic_route, heuristic_route[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="orange", width=3, style="--")
        st.warning("⚠️ Dirac condition not met — showing heuristic route instead.")

    blue_line = mlines.Line2D([], [], color="#42A5F5", linewidth=2, label="Connected roads")
    gray_dotted = mlines.Line2D([], [], color="#B0BEC5", linestyle=':', linewidth=1, label="Too far to connect")
    red_line = mlines.Line2D([], [], color="red", linewidth=3, label="Hamiltonian cycle (perfect route)")
    orange_dashed = mlines.Line2D([], [], color="orange", linewidth=3, linestyle="--", label="Heuristic (real-world route)")

    legend = ax.legend(
        handles=[blue_line, gray_dotted, red_line, orange_dashed],
        loc='upper left',
        bbox_to_anchor=(0.02, 0.98),
        frameon=True,
        fancybox=True,
        framealpha=0.9,
        facecolor='white',
        edgecolor='gray',
        fontsize=9,
        title="Legend"
    )
    legend.get_title().set_fontweight('bold')

    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

st.caption("Made by Diya Limbani,Suhan Ramani,Krish Patel")
