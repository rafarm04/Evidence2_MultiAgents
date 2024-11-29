

# Integrated Autonomous Surveillance System

## Documentation

You can find the detailed project documentation, including the system design, agent behaviors, implementation details, and analysis in our comprehensive report: [Project Documentation PDF](https://drive.google.com/file/d/1zUVnwrRo6COHelZAfjxzTd7yQOmV8PGF/view?usp=sharing)

The documentation covers:

- **Introduction**: An overview of the project's objectives and the challenges addressed.
- **Team Composition**: Roles and contributions of each team member.
- **Formal Proposal**: Detailed problem description, agents involved, environment setup, and success metrics.
- **Work Plan and Acquired Learning**: Project timeline, responsibilities, and insights gained during development.
- **Evidence**: Code excerpts and explanations of key components.
- **Conclusion**: Reflections on the project's outcomes and future considerations.

## Demonstration Video

Watch a video demonstration of the current functionality of our system: [Project Demo Video](https://drive.google.com/file/d/1dVTSWxUu3o26loMIPVybDsQRUuWz5jA1/view?usp=sharing)

The video showcases:

- The simulation environment with drones, cameras, and guards.
- Agents performing their tasks within the grid.
- Interactions between agents and objects.
- The system's response to potential threats.

## Introduction

Ensuring safety and security in large and complex environments like warehouses, factories, and agricultural areas is a significant challenge. Traditional surveillance methods often struggle to cover these vast spaces effectively. To tackle this issue, we have developed an innovative surveillance system that combines autonomous drones, strategically placed fixed cameras, and advanced computer vision techniques.

Our system relies on different agents working together seamlessly. Autonomous drones patrol the area, conducting inspections and responding to potential threats. Fixed cameras provide continuous monitoring of specific zones, enhancing the overall coverage. Security personnel are involved for critical decision-making and can intervene when necessary.

These agents operate within a virtual environment, coordinating with each other to detect and respond to potential issues in real-time. The system is designed to maintain a balance between automated processes and human oversight, allowing for efficient surveillance while still enabling human operators to take control when needed. By integrating these technologies and fostering collaboration among the agents, we aim to improve the effectiveness and reliability of security operations in complex settings.

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
├── Parte1/
│   ├── __pycache__/
│   ├── .gitignore
│   ├── Agents.py
│   ├── DronAgent.py
│   ├── RobotAgent.py
│   ├── server.py
│   ├── onto.owl
│   ├── requirements.txt
│   └── README.md
├── Parte2/
│   ├── Evidence2/
│   │   ├── .vscode/
│   │   ├── Assets/
│   │   │   ├── Prefabs/
│   │   │   ├── Scenes/
│   │   │   └── Scripts/
│   │   │       ├── OntologyManager.cs
│   │   │       ├── SecuritySimulation.cs
│   │   │       └── ThreeBox/
│   │   ├── Unity Technologies/
│   │   ├── NativeFunctionality.unity
│   │   ├── Prefabs.meta
│   │   ├── Scenes.meta
│   │   ├── Scripts.meta
│   │   ├── ServerFunctionality.unity
│   │   ├── ThreeBox.meta
│   │   └── Unity Technologies.meta
│   ├── Library/
│   ├── Logs/
│   ├── Packages/
│   ├── ProjectSettings/
│   ├── UserSettings/
│   ├── Assembly-CSharp.csproj
│   ├── Evidence2.sln
│   └── mono_crash.mem.19914.1.blob
├── yolov8m.pt
└── README.md
```

- **Documentation**: Contains the project documentation PDF.
- **Video**: Contains the demonstration video.
- **Part1_Backend**: Contains all Python scripts and resources for the agent simulation and backend logic.
- **Part2_Frontend**: Contains the Unity project files for the visual simulation.

## Technologies Used

- **Python**: For backend simulation and agent logic.
- **AgentPy**: A Python library for agent-based modeling.
- **Owlready2**: A module for ontology-oriented programming in Python.
- **Flask**: A micro web framework for Python to facilitate communication between backend and frontend.
- **Unity Engine**: For creating the visual simulation of the environment and agents.
- **C#**: Scripting language used in Unity for frontend development.

### YOLO Object Detection

**YOLO (You Only Look Once)** is a real-time object detection algorithm that divides an input image into a grid and predicts bounding boxes, class labels, and confidence scores in a single pass through a neural network. Each grid cell detects multiple bounding boxes and assigns class probabilities, while confidence scores indicate how likely the detected object is and how accurate the bounding box is. YOLO processes the entire image at once, making it fast and efficient for real-time applications. After detection, a post-processing step called Non-Maximum Suppression (NMS) filters out redundant boxes, keeping the most confident predictions. This enables YOLO to quickly and accurately detect and classify objects in images.

#### How the Server Functions with Unity

- **Unity Captures the Image**:
  - A camera in Unity (e.g., drone camera, fixed camera) captures an image.
  - The script (`CameraCapture.cs`) converts the image into a PNG byte array.
  
- **Unity Sends the Image to the Server**:
  - Unity (`YoloDetection.cs`) uses an HTTP POST request to send the captured image to the Flask server.
  - The image is sent as part of a `multipart/form-data` request, ensuring compatibility with the Flask server.
  
- **Server Processes the Image**:
  - The Flask server receives the image and decodes it using OpenCV.
  - The YOLO model processes the image, identifying objects and their bounding boxes.
  
- **Server Responds to Unity**:
  - The Flask server formats the detection results as JSON and sends them back to Unity.
  - The JSON includes details like detected object classes and bounding box coordinates.
  
- **Unity Processes the Results**:
  - Unity parses the JSON response and uses it to implement game logic, such as highlighting detected objects or triggering actions based on specific detections.

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
