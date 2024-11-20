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
            ({"perception": {"below": 1}, "detect_something": False}, "none"),
            ({"percetion": {"below": 2}, "detect_something": True}, "alert"),  
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
            elif key == "detect_something":
                if self.is_detecting_something != value:
                    return False