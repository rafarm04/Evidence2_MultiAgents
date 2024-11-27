from flask import Flask, request, jsonify
import json
from Agents import SecurityDepartmentModel, onto

# Crear la aplicación Flask
app = Flask(__name__)

# Inicializar el modelo
def init_model():
    parameters = {
        "num_cams": 4,
        "num_dron": 1,
        "objects": 5,
        "grid_size": 10,
        "steps": 1000,
    }
    model = SecurityDepartmentModel(parameters)
    model.setup()
    return model

# Cargar modelo al iniciar la aplicación
model = init_model()

@app.route('/state', methods=['GET'])
def get_state():
    """
    Devuelve el estado actual del modelo, incluidos drones, guardias, cámaras y objetos.
    """
    try:
        state = {
            "drones": [dron.onto_dron.ubication for dron in model.drons],
            "cameras": [cam.get_state() for cam in model.cams],
            "guard": [guard.onto_guard.ubication for guard in model.guard],
            "objects": model.objects,
            "grid": model.grid
        }
        return jsonify(state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dron/<int:dron_id>/action', methods=['POST'])
def dron_action(dron_id):
    """
    Permite a Unity enviar datos de percepción a un dron y devuelve su acción resultante.
    """
    try:
        data = request.json
        perception = data.get('perception')

        # Obtener el dron correspondiente
        dron = next((d for d in model.drons if d.id == dron_id), None)
        if not dron:
            return jsonify({"error": "Dron not found"}), 404

        # Enviar percepción al dron y obtener su acción
        action = dron.step(perception_json=json.dumps({"id": dron_id, "position": perception}))
        return jsonify({"action": action, "ubication": dron.onto_dron.ubication})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update', methods=['POST'])
def update_environment():
    """
    Actualiza el entorno en base a las acciones realizadas por Unity.
    """
    try:
        data = request.json  # Suponiendo que se envía una lista de acciones
        if not isinstance(data, list):
            return jsonify({"error": "Invalid input format. Expected a list of actions."}), 400

        for dron_action in data:
            dron_id = dron_action['id']
            action = dron_action['action']

            dron = next((d for d in model.drons if d.id == dron_id), None)
            if not dron:
                continue

            # Actualizar el entorno con la acción del dron
            model.update_grid([(int(dron.onto_dron.ubication.split(',')[0]), 
                                int(dron.onto_dron.ubication.split(',')[1]))])
        return jsonify({"message": "Environment updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_simulation():
    """
    Reinicia la simulación.
    """
    try:
        global model
        model = init_model()
        return jsonify({"message": "Simulation reset successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
