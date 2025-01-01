# Ecosystem Simulation

## Overview
This project simulates a complex ecosystem where different animal species (rabbits, foxes, and pigs) interact in a dynamically changing environment. The simulation incorporates advanced algorithms including A* pathfinding, game theory for predator-prey interactions, and genetic inheritance.

## Features
- Multiple animal species with unique behaviors:
  - Rabbits (Herbivores)
  - Foxes (Carnivores)
  - Pigs (Omnivores)
- Dynamic environment with seasonal changes affecting:
  - Food availability
  - Animal behavior
  - Breeding patterns
- Genetic inheritance system
- Real-time population statistics
- Interactive visual display
- Real-time population graphs

## Prerequisites
- Python 3.x
- Required packages:
  ```
  pip install pygame numpy matplotlib
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecosystem-simulation.git
   cd ecosystem-simulation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation
To start the simulation:
```bash
python ecosystem.py
```

### Controls
- Click the Pause/Unpause button at the bottom of the window to control the simulation
- Close either window to end the simulation

## Implementation Details

### World Generation
- Uses Perlin noise for natural-looking terrain generation
- Includes various terrain types:
  - Water bodies
  - Grassland
  - Berry bushes

### Animal Behavior Systems
- A* Pathfinding: Animals use A* algorithm for navigation
- Game Theory: Predator-prey interactions based on game theory principles
- Genetic Algorithm: Handles trait inheritance between generations

### Seasonal System
Four seasons affect the ecosystem:

- Winter: Reduced food, increased hunger/thirst rates
- Spring: Increased breeding rates, abundant food
- Summer: High thirst rates
- Fall: Peak food availability

## Technical Structure
The project is organized into several key modules:

### Animals
- Base animal class with common behaviors
- Specialized classes for each species:
  - Herbivores (Rabbits)
  - Carnivores (Foxes)
  - Omnivores (Pigs)

### Algorithms
- A* pathfinding for movement
- Game theory for predator-prey decisions
- Genetic algorithms for inheritance
- CSP (Constraint Satisfaction Problem) solver

### World
- Dynamic terrain management
- Season system
- Resource distribution

## Contributing
Contributions are welcome! Please feel free to submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Pygame for graphics rendering
- NumPy for mathematical operations
- Matplotlib for real-time plotting