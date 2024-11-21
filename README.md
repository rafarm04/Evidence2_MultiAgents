```markdown
# Integrated Autonomous Surveillance System

## Introduction

In modern security operations, ensuring safety within large and complex environments poses significant challenges. Traditional surveillance methods often fall short in covering expansive areas like warehouses, factories, and agricultural zones effectively. This project presents an innovative solution by developing an integrated autonomous surveillance system that combines the capabilities of autonomous drones, fixed cameras, and advanced computer vision algorithms.

Our system leverages multi-agent collaboration within a simulated environment to detect and respond to potential threats efficiently. By simulating agents such as drones, cameras, and security personnel, we aim to enhance surveillance operations' precision, reliability, and scalability.

## Project Overview

The project is divided into two main parts:

### Part 1: Agent Simulation and Backend Development

#### Description

This part focuses on creating the backend simulation of agents using Python. We utilize agent-based modeling to define the behaviors and interactions of different agents within a grid-based environment. The agents include:

- **Drone Agents**: Autonomous drones that patrol the environment, detect objects, and respond to potential threats.
- **Camera Agents**: Fixed cameras positioned strategically to monitor specific areas and detect objects within their line of sight.
- **Guard Agents**: Security personnel who respond to threats by moving towards and securing suspicious objects.
- **Objects**: Items within the environment classified as "threatening" or "harmless."

#### Implementation Details

- **Languages and Tools**: Python, AgentPy, Owlready2, Flask.
- **Key Scripts**:
  - `agent.py`: Defines the base classes for agents and sets up the ontology using Owlready2.
  - `DronAgent.py`: Implements the `Drone` class, defining the drone's perception, decision-making, and actions.
  - `robotAgent.py`: Contains the `RobotAgent` class for object manipulation tasks like grabbing and dropping.
  - `server.py`: Sets up a Flask server to facilitate communication between the agents and an external interface (e.g., Unity).

### Part 2: Unity Visualization and Frontend Development

#### Description

The second part involves creating a visual simulation of the environment using Unity. This allows for a graphical representation of the agents and their interactions within the grid, enhancing understanding and demonstration of the system's capabilities.

#### Implementation Details

- **Languages and Tools**: C#, Unity Engine.
- **Key Scripts**:
  - `ontologyManager.cs`: Simulates the ontology within Unity, managing agents and their properties.
  - `securitySimulation.cs`: Controls the simulation, including agent initialization and behavior within the Unity environment.

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Unity 2020.3 or higher
- Required Python libraries:
  - `agentpy`
  - `owlready2`
  - `flask`
  - `random`
  - `json`
- Unity packages:
  - Standard assets for 3D objects and environment

### Setting Up the Python Backend (Part 1)

1. **Clone the Repository**

   ```bash
   git clone https://github.com/GermanDelRioGuzman/Evidence2_MultiAgents_Drone.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd Evidence2_MultiAgents_Drone/Part1_Backend
   ```

3. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

4. **Install Required Python Libraries**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Simulation**

   - To run the agent simulation and start the Flask server:

     ```bash
     python server.py
     ```

### Setting Up the Unity Frontend (Part 2)

1. **Open Unity and Load the Project**

   - Launch Unity Hub.
   - Click on "Add" and select the `Part2_Frontend` directory from the cloned repository.

2. **Ensure All Assets Are Loaded**

   - Once the project is opened, ensure that all assets and scripts are properly imported.
   - Check for any missing packages or assets and resolve any warnings or errors.

3. **Run the Simulation**

   - In the Unity Editor, open the main scene (e.g., `MainScene.unity`).
   - Click on the "Play" button to start the simulation.

## How to Run the Simulation

1. **Start the Python Backend**

   - Ensure the Flask server is running by executing `python server.py`.
   - The server handles agent logic and communicates with the Unity frontend.

2. **Run the Unity Frontend**

   - With the backend server running, press "Play" in the Unity Editor.
   - The Unity simulation will visualize the agents and their interactions.

3. **Interact with the Simulation**

   - Observe the drones, cameras, and guards as they operate within the environment.
   - The agents will perform actions based on the logic defined in the Python backend.

## Project Structure

```
Evidence2_MultiAgents_Drone/
├── Part1_Backend/
│   ├── agent.py
│   ├── DronAgent.py
│   ├── robotAgent.py
│   ├── server.py
│   ├── onto.owl
│   ├── requirements.txt
│   └── README.md
├── Part2_Frontend/
│   ├── Assets/
│   │   ├── Scripts/
│   │   │   ├── ontologyManager.cs
│   │   │   └── securitySimulation.cs
│   │   └── Scenes/
│   │       └── MainScene.unity
│   └── ProjectSettings/
├── README.md
└── LICENSE (if applicable)
```

- **Part1_Backend**: Contains all Python scripts and resources for the agent simulation and backend logic.
- **Part2_Frontend**: Contains the Unity project files for the visual simulation.

## Technologies Used

- **Python**: For backend simulation and agent logic.
- **AgentPy**: A Python library for agent-based modeling.
- **Owlready2**: A module for ontology-oriented programming in Python.
- **Flask**: A micro web framework for Python to facilitate communication between backend and frontend.
- **Unity Engine**: For creating the visual simulation of the environment and agents.
- **C#**: Scripting language used in Unity for frontend development.

## Team Members

- **Rafael Romo Muñoz (A01643137)** – Drone Navigation Specialist
- **German Avelino Del Rio Guzman (A01641976)** – Computer Vision Specialist
- **José María Soto Valenzuela (A01254831)** – Inter-Agent Communication Developer
- **César Alán Silva Ramos (A01252916)** – Security Personnel Control Developer
- **Dilan Eduardo Ocampo Hernandez (A01634254)** – Graphical Interface Developer

## Acknowledgments

We would like to thank our professors:

- Iván Axel Dounce Nava
- Obed Nehemías Muñoz Reynoso
- Carlos Johnnatan Sandoval Arrayga

For their guidance and support throughout this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For any questions or contributions, please contact the project maintainers via the GitHub repository.

```