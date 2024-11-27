using System.Collections.Generic;
using UnityEngine;

public class OntologyManager : MonoBehaviour
{
    public Dictionary<string, object> Ontology = new Dictionary<string, object>();

    void Start()
    {
        // Simular las clases de la ontología como estructuras de datos
        Ontology["Guard"] = new List<Guard>();
        Ontology["Dron"] = new List<Dron>();
        Ontology["Camera"] = new List<Camera>();
        Ontology["LandingPoint"] = new Vector2(Random.Range(0, 10), Random.Range(0, 10));
        Ontology["Objects"] = new List<GameObject>();
    }
}

public class Guard
{
    public string Ubication { get; set; }
    public string Decision { get; set; }
}

public class Dron
{
    public string Ubication { get; set; }
    public string Decision { get; set; }
}

public class Camera
{
    public string Ubication { get; set; }
    public string Status { get; set; }
}

public class LandingPoint
{
    public Vector2 Position { get; set; }
}

public class Object
{
    public GameObject GameObject { get; set; }
}
