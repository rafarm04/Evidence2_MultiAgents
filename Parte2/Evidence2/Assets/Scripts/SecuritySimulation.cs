using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SecuritySimulation : MonoBehaviour
{
    public int gridSize = 10; // Tamaño de la cuadrícula
    public int numberOfObjects = 5; // Número de objetos configurables
    public int droneSteps = 10; // Cantidad de pasos iniciales que debe dar el dron
    public float stepInterval = 0.2f; // Intervalo entre pasos en segundos
    public GameObject dronPrefab;
    public GameObject guardPrefab;
    public GameObject cameraPrefab;
    public GameObject landingPointPrefab;
    public GameObject objectPrefab;

    private List<GameObject> drons = new List<GameObject>();
    private List<GameObject> guards = new List<GameObject>();
    private List<GameObject> cameras = new List<GameObject>();
    private List<GameObject> objects = new List<GameObject>();
    private Dictionary<GameObject, string> objectStates = new Dictionary<GameObject, string>(); // Estados de los objetos
    private Dictionary<GameObject, string> objectThreats = new Dictionary<GameObject, string>(); // Amenaza o inofensivo
    private HashSet<Vector3> occupiedPositions = new HashSet<Vector3>();
    private Vector3 landingPoint;

    void Start()
    {
        InitializeGrid();
        InitializeAgents();
        InitializeObjects();
        MarkObjectsInCameraView(); // Marcar objetos visibles por cámaras
        StartCoroutine(RunSimulation());
    }

    void InitializeGrid()
    {
        // Generar un punto de aterrizaje aleatorio
        landingPoint = new Vector3(Random.Range(0, gridSize), 0, Random.Range(0, gridSize));
        Debug.Log($"Landing Point: {landingPoint}");
        occupiedPositions.Add(landingPoint);

        // Visualizar el punto de aterrizaje
        Instantiate(landingPointPrefab, landingPoint, Quaternion.identity);
    }

    void InitializeAgents()
    {
        // Inicializar cámaras en las esquinas
        cameras.Add(Instantiate(cameraPrefab, new Vector3(0, 0, 0), Quaternion.identity));
        cameras.Add(Instantiate(cameraPrefab, new Vector3(0, 0, gridSize - 1), Quaternion.identity));
        cameras.Add(Instantiate(cameraPrefab, new Vector3(gridSize - 1, 0, 0), Quaternion.identity));
        cameras.Add(Instantiate(cameraPrefab, new Vector3(gridSize - 1, 0, gridSize - 1), Quaternion.identity));

        foreach (GameObject camera in cameras)
        {
            occupiedPositions.Add(camera.transform.position);
        }

        // Inicializar un guardia
        GameObject guard = Instantiate(guardPrefab, new Vector3(1, 0, 1), Quaternion.identity);
        guards.Add(guard);
        occupiedPositions.Add(guard.transform.position);

        // Inicializar drones
        GameObject dron = Instantiate(dronPrefab, new Vector3(5, 0, 5), Quaternion.identity);
        drons.Add(dron);
        occupiedPositions.Add(new Vector3(5, 0, 5));
    }

    void InitializeObjects()
    {
        for (int i = 0; i < numberOfObjects; i++)
        {
            Vector3 randomPosition = GetRandomUnoccupiedPosition();
            randomPosition.y = 0; // Asegurar que y=0
            GameObject obj = Instantiate(objectPrefab, randomPosition, Quaternion.identity);
            objects.Add(obj);

            // Asignar estado inicial
            objectStates[obj] = "no visitado";

            // Asignar amenaza o inofensivo de forma aleatoria
            objectThreats[obj] = Random.Range(0, 2) == 0 ? "amenaza" : "inofensivo";

            occupiedPositions.Add(randomPosition);
            Debug.Log($"Object {i + 1} placed at {randomPosition} with state: {objectStates[obj]}, type: {objectThreats[obj]}");
        }
    }

    Vector3 GetRandomUnoccupiedPosition()
    {
        while (true)
        {
            int x = Random.Range(0, gridSize);
            int z = Random.Range(0, gridSize);
            Vector3 position = new Vector3(x, 0, z);

            if (!occupiedPositions.Contains(position))
            {
                return position;
            }
        }
    }

    IEnumerator RunSimulation()
    {
        // Ejecutar los pasos iniciales de los drones
        for (int step = 0; step < droneSteps; step++)
        {
            foreach (GameObject dron in drons)
            {
                MoveAgent(dron);
                CheckObjectCollision(dron);
            }

            yield return new WaitForSeconds(stepInterval); // Usar el intervalo de paso configurado
        }

        Debug.Log("Initial steps completed. Starting landing search...");

        // Continuar buscando el punto de aterrizaje
        foreach (GameObject dron in drons)
        {
            yield return StartCoroutine(SearchLandingPoint(dron));
        }

        Debug.Log("Drones completed their mission. Starting guard patrol...");

        // Comenzar patrullaje del guardia
        foreach (GameObject guard in guards)
        {
            yield return StartCoroutine(GuardPatrol(guard));
        }

        Debug.Log("Guard completed the patrol.");
    }

    IEnumerator SearchLandingPoint(GameObject dron)
    {
        while (true)
        {
            MoveAgent(dron);

            // Verificar si el dron ha alcanzado el punto de aterrizaje
            if (CheckLandingPoint(dron))
            {
                Debug.Log($"Dron reached the landing point at {dron.transform.position}. Stopping movement.");
                yield break; // Finalizar la corrutina al encontrar el punto de aterrizaje
            }

            yield return new WaitForSeconds(stepInterval); // Pausa entre movimientos
        }
    }

    IEnumerator GuardPatrol(GameObject guard)
    {
        foreach (GameObject obj in objects)
        {
            Debug.Log($"Guard moving towards object at {obj.transform.position}");

            // Mover al guardia hacia el objeto
            while (Vector3.Distance(guard.transform.position, obj.transform.position) > 2.0f)
            {
                MoveTowards(guard, obj.transform.position);
                yield return new WaitForSeconds(stepInterval);

                // Depuración: Posición actual del guardia y distancia al objeto
                Debug.Log($"Guard position: {guard.transform.position}, Distance to object: {Vector3.Distance(guard.transform.position, obj.transform.position)}");
            }

            // Al llegar al objeto, verificar el tipo y reportar
            Debug.Log($"Objeto detectado en posición: {obj.transform.position}");

            if (objectThreats[obj] == "amenaza")
            {
                Debug.Log($"Amenaza detectada en coordenadas: {obj.transform.position}");
            }
            else
            {
                Debug.Log($"Objeto inofensivo en coordenadas: {obj.transform.position}");
            }
        }
    }

    void MarkObjectsInCameraView()
    {
        foreach (GameObject camera in cameras)
        {
            Vector3 cameraPosition = camera.transform.position;

            foreach (GameObject obj in objects)
            {
                Vector3 objectPosition = obj.transform.position;

                // Comparar si el objeto está en la misma fila (z) o columna (x) que la cámara
                if (Mathf.Approximately(cameraPosition.x, objectPosition.x) || Mathf.Approximately(cameraPosition.z, objectPosition.z))
                {
                    // Marcar el objeto como visitado
                    objectStates[obj] = "visitado";
                    Debug.Log($"Objeto en {objectPosition} marcado como visitado por cámara en {cameraPosition}");
                }
            }
        }
    }




    void MoveTowards(GameObject agent, Vector3 targetPosition)
    {
        Vector3 direction = (targetPosition - agent.transform.position).normalized;
        Vector3 newPosition = agent.transform.position + direction;

        // Ajustar la posición y asegurar que y=0
        newPosition.x = Mathf.Clamp(newPosition.x, 0, gridSize - 1);
        newPosition.z = Mathf.Clamp(newPosition.z, 0, gridSize - 1);
        newPosition.y = 0;

        if (!IsPositionOccupied(newPosition))
        {
            occupiedPositions.Remove(agent.transform.position);
            occupiedPositions.Add(newPosition);
            agent.transform.position = newPosition;
        }
    }

    bool CheckLandingPoint(GameObject dron)
    {
        // Asegurarse de que la altura sea consistente
        Vector3 dronPosition = dron.transform.position;
        dronPosition.y = 0; // Normalizar altura
        Vector3 landingPosition = landingPoint;
        landingPosition.y = 0; // Normalizar altura

        // Verificar si el dron está cerca del punto de aterrizaje
        return Vector3.Distance(dronPosition, landingPosition) <= 1.0f; // Aumentar rango si es necesario
    }

    bool IsPositionOccupied(Vector3 position)
    {
        return occupiedPositions.Contains(position);
    }

    void MoveAgent(GameObject agent)
    {
        Vector3 position = agent.transform.position;
        Vector3 newPosition = position;

        int direction = Random.Range(0, 4);
        switch (direction)
        {
            case 0: newPosition += Vector3.forward; break;
            case 1: newPosition += Vector3.back; break;
            case 2: newPosition += Vector3.left; break;
            case 3: newPosition += Vector3.right; break;
        }

        newPosition.x = Mathf.Clamp(newPosition.x, 0, gridSize - 1);
        newPosition.z = Mathf.Clamp(newPosition.z, 0, gridSize - 1);
        newPosition.y = 0; // Asegurar que y=0

        if (!IsPositionOccupied(newPosition))
        {
            occupiedPositions.Remove(position);
            occupiedPositions.Add(newPosition);
            agent.transform.position = newPosition;
            Debug.Log($"Moved {agent.name} to {newPosition}");
        }
    }

    void CheckObjectCollision(GameObject dron)
    {
        Vector3 dronPosition = dron.transform.position;
        dronPosition.y = 0; // Asegurar que y=0

        foreach (GameObject obj in objects)
        {
            Vector3 objPosition = obj.transform.position;
            objPosition.y = 0; // Asegurar que y=0

            if (Vector3.Distance(dronPosition, objPosition) <= 1.0f) // Aumentar rango de detección
            {
                if (objectStates[obj] == "no visitado")
                {
                    objectStates[obj] = "visitado"; // Cambiar el estado del objeto
                    Debug.Log($"Dron visited object at {obj.transform.position}. New state: {objectStates[obj]}, type: {objectThreats[obj]}");
                }
            }
        }
    }
}
