import agentpy as ap
import json
import random
from owlready2 import *

# here we are goin to create the ontology
onto = get_ontology("file://onto.owl")

with onto:
    class Dron(Thing): #here we declare the class Agent
        pass

    class Position(Thing):#this class is going to be used to get the position of the drone
        pass

    class Object(Thing):
        pass

    class Direction(Thing):#this class is going to be used to get the direction of the drone
        pass

    class Action(Thing):#this class is going to be used to get the action of the drone
        pass

    class has_position(ObjectProperty):#this class is going to be used to get the position of the drone
        domain = [Dron] #domain: the class that is going to be used
        range = [Position] #range: the class that is going to be used

    class has_perception(ObjectProperty): #this class is going to be used to get the perception of the drone
        domain = [Dron]
        range = [Object]

    class detect_something(objectProperty): #this class is going to be used to get the detection of the drone
        domain = [Dron]
        range = [Position]

    class can_perform(ObjectProperty):#this class is going to be used to get the action of the drone
        domain = [Dron]
        range = [Action]

    class Forward(Direction):
        pass

    class Backward(Direction):
        pass

    class Left(Direction):
        pass

    class Right(Direction):
        pass

    class Move(Action):
        pass

    class Alert(Action):
        pass

    class Wait(Action):
        pass

# Save the ontology
    onto.save()

#in this class  we declare tue class drone which we are going to work with
class Drone(ap.Agent): 
    def setup(self): 
        self.onto_robot = onto.Robot() #thsi property
        self.onto_robot.has_position() = [onto.Position()] #here we declare the method has_position of the propertie onto_robot
        self.movements = 0 #movements of the drone
        self.perception_data = {} #here we are going to get the perception data
        self.is_detecting_something = False #here the drone detect something
        self.rules = [
            ({"perception": {"below": 1}, "detect_suspicious": False}, "continue"),
            ({"percetion": {"below": 2}, "detect_suspicious": True}, "alert"),

        ]

    def get_state(self): #here we are going to get the state of the drone
        return {
            "id" : self.onto_robot.id, 
            "is_detecting_something": self.is_detecting_something,
            "movements": self.movements
        }
    #here we are going to get the perception of the drone
    def update_state(self, perception_json, stored_state=None): #here we are going to update the state of the drone
        print("Updating state with perception: {perception_json}")
        perception = json.loads(perception_json)
        self.onto_robot.id = perception["id"]
        self.perception_data = perception["position"]
        if stored_state:
            # Restore the state
            self.movements = stored_state["movements"]
        print("State updated: Robot id: {self.onto_robot.id}, alrt: {self.is_detecting_something}, movements: {self.movements}")
    
    def check_rule(self, rule):
        for key,value in rule.items():
            if key == "perception":
                for direction, expected in value.items():
                    if self.perception_data.get(direction) != expected:
                        return False
            elif key == "detect_suspicious":
                if self.is_detecting_something != value:
                    return False
        
    
    def get_suspicious_direction(self):
        return [direction for direction, value in self.perception_data.items() if value == 1]

    def get_free_directions(self):
        return [direction for direction, value in self.perception_data.items() if value == 0]
    
    def get_guard_direction(self):
        return [direction for direction, value in self.perception_data.items() if value == 2]
    
    def perceive_and_act(self):
        print(f"PErceiving and acting... There is suspicious activity {self.is_detecting_something}")

        if self.is_detecting_something:
            suspicious_direction = self.get_suspicious_direction()
            if suspicious_direction: 
                chosen_direction = random.choice(suspicious_direction)
                print(f"Alerting in direction {chosen_direction}")
                return f"alert {chosen_direction}"
            
            else: 
                free_directions = self.get_free_directions()
                if free_directions: 
                    choosen_direction = random.choice(free_directions)
                    print(f"Moving in direction  {choosen_direction} with an alert")
                    return f"move {choosen_direction}"
                else: 
                    print("no free space to move")
                    return "wait"
        
        else: 
            alert_direction = self.get_suspicious_direction()
            if alert_direction:
                chosen_direction = random.choice(alert_direction)
                print(f"Alerting in direction {chosen_direction}")
                return f"alert {chosen_direction}"
            else:
                free_directions = self.get_free_directions()
                if free_directions:
                    choosen_direction = random.choice(free_directions)
                    print(f"Moving in direction {choosen_direction}")
                    return f"move {choosen_direction}"
                else:
                    print("No free space to move")
                    return "wait"
                
    def act(self, action):
        print(f"Perform action: {action}")
        if action.startswith("move"):
            self.movements += 1
        elif action.startswith("alert"):
            self.is_detecting_something = True
        return action 

    def reason(self):
        print("reasoning...")
        action = self.perceive_and_act()
        return json.dumps({"action": action})
        
    def step(self, perception_json, stored_state = None):
        print(f"Step with perception: {perception_json}")
        self.update_state(perception_json,stored_state)
        action = self.perceive_and_act()
        return self.act(action)
    
class GridModel(ap.Model):
    def setup(self):
        self.num_drons = 1
        self.num_suspicions_onbjects = 3
        self.grid_size = self.p.grid_size
        self.current_step = 0
        
        self.grid = ap.Grid(self, (self.grid_size, self.grid_size), track_empty = True)

        self.drons = ap.AgentList(self, self.num_drons, Drone)
        for i, dron in enumerate(self.drons):
            dron.onto_robot.id = i
        self.grid.add_agents(self.drons, random = True, empty = True)

        self.objects = ap.AgentList(self, self.num_objects, ap.Agent)
        self.suspicious_objects = ap.AgentList(self, self.num_suspicious_objects, ap.Agent)
        self.grid.add_drons(self.objects, random = True, empty = True)

        self.data = {
            'steps_to_completion': None,
            'detection': {dron.onto_robot.id: 0 for dron in self.drons}
        }
    
    def get_perception(self, dron): 
        x, y = self.grid.positions[dron]
        directions = {'F': (0, 1), 'B': (0, -1), 'L': (-1, 0), 'R': (1, 0)}        

        perception = {} #perception of the drone
        for direction, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy #new position

            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                cell_content =  self.grid.agents[new_x, new_y] #get the content of the cell
                if not cell_content: 
                    perception[direction] = 0
                elif any(isinstance(agent, Drone) for agent in cell_content): 
                    perception[direction] = 2
                elif len(cell_content) == 1:
                    perception[direction] = 1
                else: 
                    perception[direction] = 3
            else: 
                perception[direction] = 2
        
        return json.dumps({
            "id": dron.onto_robot.id,
            "position": perception
        })

    def update_enviroment(self, dron, action):
        current_position = self.grid.positions[dron]

        if action.startswith("alert_"):
            direction = action.split("")[1]
            if direction == "random":
                direction = random.choice(["F", "B", "L", "R"])
            dx, dy = {"F": (0, 1), "B": (0, -1), "L": (-1, 0), "R": (1, 0)}[direction]
            new_position = (current_position[0] + dx, current_position[1] + dy)

            if (0 <= new_position[0] < self.grid_size and 0 <= new_position[1] < self.grid_size and len(self.grid[new_position]) == 0):
                self.grid.move_to(dron,new_position)
                self.data["dron_movements"][dron.onto_robot.id] += 1

            elif action.startswith("alert_"):
                direction = action.split("_")[1]
                if direction == "random":
                    direction = random.choice(['F','B','L','R'])
                
                dx, dy = {'F': (0, 1), 'B': (0, -1), 'L': (-1, 0), 'R': (1, 0)}[direction]
                new_position = (current_position[0] + dx, current_position + dy)
            
                if (0 <= new_position[0] < self.grid_size and 
                    0 <= new_position[1] < self.grid_size and 
                    len(self.grid.agents[new_position]) == 0):
                    self.grid.move_to(dron, new_position)
                    self.data['detection'][dron.onto_robot.id] += 1

            elif action.startswith("alert_"):
                direction = action.split("_")[1]
                dx, dy = {'F': (0, 1), 'B': (0, -1), 'L': (-1, 0), 'R': (1, 0)}[direction]
                alert_pos = (current_position[0] + dx, current_position[1] + dy)

                if (0 <= alert_pos[0] < self.grid_size and 
                    0 <= alert_pos[1] < self.grid_size):
                    objects_at_pos = [agent for agent in self.grid.agents[grab_pos] if agent in self.objects]
                    if objects_at_pos:
                        alert_suspicious = objects_at_pos[0]
                        self.grid.remove_agents(alert_suspicious)
                        dron.onto_robot.is_holding = [onto.Object()]


    def step(self):
            self.current_step += 1

            for dron in self.robots:
                perception_json = self.get_perception(dron)
                action = dron.step(perception_json)
                self.update_environment(dron, action)

            if self.check_end_condition():
                self.stop()
            self.current_step += 1

            for dron in self.robots:
                perception_json = self.get_perception(dron)
                action = dron.step(perception_json)
                self.update_environment(dron, action)

            if self.check_end_condition():
                self.stop()
                
    def check_end_condition(self):
        all_stacks_valid = all(1 <= stack_size <= 5 for stack_size in self.stacks.values())
        all_objects_stacked = sum(self.stacks.values()) == self.num_objects
        all_robots_believe_finished = all(not robot.onto_robot.is_holding for robot in self.robots)
        return all_stacks_valid and all_objects_stacked and all_robots_believe_finished

    def end(self):
        self.data['steps_to_completion'] = self.current_step
        print(f"Simulation ended after {self.data['steps_to_completion']} steps")
        print("Robot movements:")
        for robot_id, movements in self.data['robot_movements'].items():
            print(f"Robot {robot_id}: {movements} movements")

    def run_model(parameters):
        model = GridModel(parameters)
        results = model.run()
        return model, results

    if __name__ == "__main__":
        parameters = {
            'num_objects': 20,
            'grid_size': 10
        }
        model, results = run_model(parameters)

