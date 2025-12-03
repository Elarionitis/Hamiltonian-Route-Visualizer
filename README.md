# Dirac Delivery: Hamiltonian Route Visualizer 🚚

An interactive **Streamlit** app that models a delivery network as a graph and explores when a **Hamiltonian cycle** (a full delivery loop visiting each location exactly once) exists.

The app uses:

- **Dirac’s Theorem** to check if a Hamiltonian cycle is *guaranteed* from degree conditions.
- A **brute-force Hamiltonian cycle search** (for small graphs) to actually find such a cycle.
- A **nearest–neighbour heuristic route** as a realistic alternative when no Hamiltonian cycle exists.

> Built for educational purposes to connect **graph theory** with a **delivery route planning** scenario.

---

## ✨ Features

- Randomly generates delivery locations in a 2D plane.
- Connects locations with edges if they are within a chosen **distance threshold** (road radius).
- Shows:
  - Node **degrees** for all locations.
  - Whether **Dirac’s condition** is satisfied.
  - Whether a **Hamiltonian cycle** actually exists (and displays it).
  - A **greedy nearest-neighbour route** as a heuristic “real-world” route.
- Side-by-side:
  - **Text summary** (routes, distances, degrees).
  - **Graph visualization** with clear legend and highlighted routes.

---

## 🧠 Math Background (Short)

- A **Hamiltonian cycle** is a cycle that visits every vertex exactly once and returns to the start.
- **Dirac’s Theorem**:  
  For a simple graph with \( n \ge 3 \) vertices, if **every vertex has degree at least \( n/2 \)**, then the graph is guaranteed to have a Hamiltonian cycle.
- In this app:
  - We check Dirac’s condition on the generated graph.
  - We also *explicitly* try to find a Hamiltonian cycle using permutations (only feasible for small \( n \)).
  - When no cycle is found, we still build a plausible delivery route using the **nearest-neighbour heuristic**.

---

## 🛠 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) – UI & app framework
- [NetworkX](https://networkx.org/) – graph representation
- [Matplotlib](https://matplotlib.org/) – plotting & visualization

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
2.Create a virtual environment(optional but recommended):

   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   #venv\Scripts\activate        # Windows

3.Install dependencies:

   pip install streamlit networkx matplotlib

4.Running the app(Assuming file is named as app.py)

   streamlit run app.py

🔎 How to Use

Use the sidebar controls to explore different graphs:

- Number of delivery locations (n)
 - Choose between 4 and 10 nodes.

- Connection distance (road threshold)
 - Controls how “dense” the graph is. Larger values → more edges → more likely to satisfy Dirac’s condition.

- Random seed
 - Changes the layout while keeping it reproducible.

##Main Panel

- Summary panel (left)

 - Shows Dirac’s condition: ✅ / ❌
 - Displays node degrees.
 - If a Hamiltonian cycle exists, shows:
   - The route (e.g. A → B → C → … → A)
   - The total distance of the cycle.

 - Always shows the heuristic (nearest-neighbour) route and its total distance.

- Graph panel (right)

 - Nodes = delivery locations.
 - Blue edges = roads in the graph.
 - Grey dotted lines = pairs that are too far to be connected.
 - Red edges = Hamiltonian cycle (when found).
 - Orange dashed edges = heuristic route (when no Hamiltonian cycle is found).

⚠️ Limitations

- The Hamiltonian search is brute-force using permutations, so it’s only practical for small graphs (here limited to at most 9–10 nodes).

- The nearest-neighbour heuristic doesn’t always give the optimal route; it’s meant to simulate a simple real-world strategy.

🔮 Possible Extensions

- Add more heuristics (2-opt, Christofides, etc.) for better TSP approximations.
- Compare Dirac’s condition with Ore’s Theorem or other Hamiltonicity criteria.
- Allow users to manually place nodes instead of random generation.
- Export routes as CSV / JSON.

👨‍💻 Authors
Suhan Ramani

Developed as a visualization project to connect Dirac’s Theorem and Hamiltonian cycles with practical delivery routing.
