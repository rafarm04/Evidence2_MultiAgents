from flask import Flask, request, jsonify
import json
from Agents import SecurityDepartmentModel 

app = Flask(__name__)

# Inicialización del modelo
def init_model():
    parameters = {
        "num_cams": 4,
        "num_dron": 1,
        "objects": 5,
        "grid_size": 10,
        "guards": 1, 
        "steps": 1000,
    }
    model = SecurityDepartmentModel(parameters)
    model.setup()
    return model

# Variable global del modelo
model = init_model()

@app.route('/initialize', methods=['POST'])
def initialize_model():
    global model
    model = init_model()
    return jsonify({"message": "Model initialized successfully."})

@app.route('/step', methods=['POST'])
def step_simulation():
    try:
        model.step()
        grid_state = model.grid
        return jsonify({"grid": grid_state, "message": "Step executed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_state', methods=['GET'])
def get_state():
    try:
        dron_states = [{dron.id: dron.onto_dron.ubication} for dron in model.drons]
        guard_states = [{"Guard": model.guard[0].onto_guard.ubication}]
        object_states = model.objects
        return jsonify({
            "drons": dron_states,
            "guard": guard_states,
            "objects": object_states,
            "grid": model.grid,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_landing', methods=['POST'])
def run_landing():
    try:
        model.run_landing()
        return jsonify({"message": "Landing mode completed."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_checking', methods=['POST'])
def run_checking():
    try:
        model.run_checking()
        object_states = model.objects
        return jsonify({
            "message": "Guard checking mode completed.",
            "objects": object_states
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_model():
    global model
    model = init_model()
    return jsonify({"message": "Model reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
