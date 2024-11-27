import agentpy as ap
import random
from owlready2 import *
import os 
import time 

# Crear la ontología
onto = get_ontology("file://onto.owl")

with onto:
    class Guard(Thing):
        pass

    class decision(DataProperty, FunctionalProperty):
        domain = [Guard]
        range = [str]

    class Dron(Thing):
        pass

    class ubication(DataProperty, FunctionalProperty):
        domain = [Dron, Guard]
        range = [str]

    class Camera(Thing):
        pass

    class id(DataProperty, FunctionalProperty):
        domain = [Camera, Dron, Guard]
        range = [int]

    class status(DataProperty, FunctionalProperty):
        domain = [Camera, Dron, Guard]
        range = [str]

    class action(DataProperty, FunctionalProperty):
        domain = [Camera, Dron, Guard]
        range = [int]

    class perception(DataProperty, FunctionalProperty):
        domain = [Camera, Dron, Guard]
        range = [int]

onto.save()


class ShareMessages:
    def __init__(self):
        self.perception = None
        self.ubication = None


class cameraAgent(ap.Agent):
    def setup(self):
        self.shared = self.model.shared_resource
        self.onto_camera = onto.Camera(f"Camera_{self.id}")
        self.onto_camera.status = "Normal"
        self.onto_camera.action = 0
        self.perception = 0

    def set_position(self, position):
        self.onto_camera.ubication = f"{position[0]},{position[1]}"

    def get_state(self):
        return {
            "id": self.id,
            "alert": self.onto_camera.status,
            "movements": self.onto_camera.action,
            "ubication": self.onto_camera.ubication,
        }

    def step(self):
        pass  # Las cámaras no se mueven


class DronAgent(ap.Agent):
    def setup(self):
        self.shared = self.model.shared_resource
        self.onto_dron = onto.Dron(f"Dron_{self.id}")
        self.onto_dron.ubication = "0,0"
        self.onto_dron.decision = "Normal"
        self.onto_dron.action = 0
        self.grid_size = self.model.p.grid_size

    def move(self):
        x, y = map(int, self.onto_dron.ubication.split(","))
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and y < self.grid_size - 1:
            y += 1
        elif direction == "down" and y > 0:
            y -= 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < self.grid_size - 1:
            x += 1
        self.onto_dron.ubication = f"{x},{y}"
        return x, y

    def perception_and_act(self):
        if self.shared.perception == 1:
            self.onto_dron.decision = "Alerting"
        else:
            self.onto_dron.decision = "Normal"

    def step(self, perception_json=None):
        x, y = self.move()
        self.perception_and_act()
        return x, y

class GuardAgent(ap.Agent):
    def setup(self):
        self.shared = self.model.shared_resource
        self.onto_guard = onto.Guard(f"Guard_{self.id}")
        self.onto_guard.ubication = "0,1"
        self.onto_guard.decision = "Normal"
        self.onto_guard.action = 0
        self.grid_size = self.model.p.grid_size

    def move(self):
        x, y = map(int, self.onto_guard.ubication.split(","))
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and y < self.grid_size - 1:
            y += 1
        elif direction == "down" and y > 0:
            y -= 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < self.grid_size - 1:
            x += 1
        self.onto_guard.ubication = f"{x},{y}"
        return x, y

    def perception_and_act(self):
        
        if self.shared.perception == 1:
            self.onto_dron.decision = "Alerting"
        else:
            self.onto_dron.decision = "Normal"
    
    def step(self, perception_json = None):
        x, y = self.move()
        self.perception_and_act()
        return x, y

class SecurityDepartmentModel(ap.Model):
    def setup(self):
        self.shared_resource = ShareMessages()
        self.grid_size = self.p.grid_size
        self.grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Inicializar posiciones ocupadas
        self.occupied_positions = set()

        # Crear cámaras en las esquinas
        self.cams = ap.AgentList(self, 4, cameraAgent)
        corner_positions = [
            (0, 0),
            (0, self.grid_size - 1),
            (self.grid_size - 1, 0),
            (self.grid_size - 1, self.grid_size - 1),
        ]
        for cam, position in zip(self.cams, corner_positions):
            cam.set_position(position)
            self.occupied_positions.add(position)

        #create securityGuard

        self.guard = ap.AgentList(self, 1,GuardAgent)
        guard_position = (1,1)
        self.occupied_positions.add(guard_position)


        # Crear drones
        self.drons = ap.AgentList(self, self.p.num_dron, DronAgent)
        for dron in self.drons:
            x, y = self.get_random_position()
            dron.onto_dron.ubication = f"{x},{y}"
            self.occupied_positions.add((x, y))

        # Crear objetos adicionales
        self.objects = {}
        for _ in range(self.p.objects):
            x, y = self.get_random_position()
            is_threatening = random.choice(["amenazador", "inofensivo"])
            self.objects[(x, y)] = {
                "estado": "no visitado",
                "tipo": is_threatening,
                "asegurado": "no"
            }
            self.occupied_positions.add((x, y))


        # Crear el punto de aterrizaje
        self.landing_point = self.get_random_position()
        self.occupied_positions.add(self.landing_point)

    def get_random_position(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.occupied_positions:
                return x, y

    def update_grid(self, dron_positions):
        self.grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for cam in self.cams:
            x, y = map(int, cam.onto_camera.ubication.split(","))
            self.grid[y][x] = "C"

        for x, y in dron_positions:
            self.grid[y][x] = "D"


        for (x, y), state in self.objects.items():
            if state["estado"] == "no visitado":
                self.grid[y][x] = "O"
            elif state["estado"] == "visitado":
                self.grid[y][x] = "V"  # Usar "V" para objetos visitados

        guard_position_x = 0
        guard_position_y = 1
        self.grid[guard_position_x][guard_position_y] ="G"

        # Marcar el punto de aterrizaje
        lx, ly = self.landing_point
        self.grid[ly][lx] = "X"

    def check_object_detection(self, dron_positions):
        for x, y in dron_positions:
            if (x, y) in self.objects and self.objects[(x, y)]["estado"] == "no visitado":
                self.objects[(x, y)]["estado"] = "visitado"
                print(f"Dron detected an object at coordinates: ({x}, {y})")

    def check_landing_point(self, dron_positions):
        for x, y in dron_positions:
            if (x, y) == self.landing_point:
                print(f"Dron reached the landing point at coordinates: ({x}, {y})")
                return True
        return False

    def print_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(" ".join(row) for row in self.grid))
        print("\n" + "-" * (self.grid_size * 2 - 1))

    def step(self):
        dron_positions = []
        for dron in self.drons:
            x, y = dron.step()
            dron_positions.append((x, y))

        self.check_object_detection(dron_positions)
        self.update_grid(dron_positions)
        self.print_grid()
        time.sleep(0.01)

    def run_landing(self):
        print("Switching to landing mode...")
        while True:
            dron_positions = [dron.step() for dron in self.drons]
            self.update_grid(dron_positions)
            self.print_grid()
            if self.check_landing_point(dron_positions):
                print("Simulation finished: Landing point found!")
                break

    def run_checking(self):
        print("Switching to guard checking mode...")
        for (x, y), properties in self.objects.items():
            if properties["tipo"] == "amenazador" and properties["estado"] == "visitado":
                self.objects[(x, y)]["asegurado"] = "si"
                print(f"Objeto malicioso asegurado en la posición ({x}, {y})")

            

# Parámetros de la simulación
parameters = {
    "num_cams": 4,
    "num_dron": 1,
    "objects": 5,
    "grid_size": 10,
    "steps": 1000,
}

# Crear y ejecutar el modelo
model = SecurityDepartmentModel(parameters)
model.run()
model.run_landing()
model.run_checking()