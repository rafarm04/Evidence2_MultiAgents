import agentpy as ap
import json
import random
from owlready2 import *

# here we are goin to create the ontology
onto = get_ontology("file://onto.owl")

with onto:
    class Agent(Thing): #here we declare the class Agent
        pass

    class Position(Thing):#this class is going to be used to get the position of the drone
        pass

    class Direction(Thing):#this class is going to be used to get the direction of the drone
        pass

    class Action(Thing):#this class is going to be used to get the action of the drone
        pass

    class has_position(ObjectProperty):#this class is going to be used to get the position of the drone
        domain = [Agent] #domain: the class that is going to be used
        range = [Position] #range: the class that is going to be used

    class has_perception(ObjectProperty): #this class is going to be used to get the perception of the drone
        domain = [Agent]
        range = [Direction]

    class detect_something(objectProperty): #this class is going to be used to get the detection of the drone
        domain = [Agent]
        range = [Direction]

    class can_perform(ObjectProperty):#this class is going to be used to get the action of the drone
        domain = [Agent]
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
    