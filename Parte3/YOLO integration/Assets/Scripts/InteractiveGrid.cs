using UnityEngine;

public class InteractiveGrid : MonoBehaviour
{
    public int rows = 10;
    public int columns = 10;
    public float cellSize = 1.0f;

    void OnDrawGizmos()
    {
        Gizmos.color = Color.black;

        // Obten la posición del plano
        Vector3 origin = transform.position;

        // Ajusta el punto de inicio para centrar el grid
        origin.x -= (columns * cellSize) / 2;
        origin.z -= (rows * cellSize) / 2;

        // Dibuja las líneas del grid
        for (int x = 0; x <= columns; x++)
        {
            Gizmos.DrawLine(
                origin + new Vector3(x * cellSize, 0, 0),
                origin + new Vector3(x * cellSize, 0, rows * cellSize)
            );
        }

        for (int y = 0; y <= rows; y++)
        {
            Gizmos.DrawLine(
                origin + new Vector3(0, 0, y * cellSize),
                origin + new Vector3(columns * cellSize, 0, y * cellSize)
            );
        }
    }
}
