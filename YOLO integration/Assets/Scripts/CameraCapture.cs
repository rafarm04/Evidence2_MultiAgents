using UnityEngine;
using System.Collections;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

public class CameraCapture : MonoBehaviour
{
    public Camera droneCamera;  // Reference to the camera
    public string serverUrl = "http://127.0.0.1:5000/get_detection";  // YOLO server URL
    private RenderTexture renderTexture;

    void Start()
    {
        // Create a render texture for the camera
        renderTexture = new RenderTexture(256, 256, 24);  // Adjust resolution as needed
        droneCamera.targetTexture = renderTexture;
    }

    public byte[] GetImageBytes()
    {
        // Capture from the RenderTexture
        RenderTexture.active = renderTexture;
        Texture2D texture = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.RGB24, false);
        texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
        texture.Apply();
        RenderTexture.active = null;

        // Convert to PNG byte array
        byte[] imageBytes = texture.EncodeToPNG();
        Destroy(texture);

        return imageBytes;
    }

    IEnumerator CaptureAndSend()
    {
        while (true)
        {
            yield return new WaitForEndOfFrame();

            byte[] imageBytes = GetImageBytes();
            Task.Run(() => SendToServer(imageBytes));  // Run async method in a non-blocking way
        }
    }

    private async Task SendToServer(byte[] imageBytes)
    {
        using (HttpClient client = new HttpClient())
        {
            var content = new ByteArrayContent(imageBytes);
            content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("image/png");

            try
            {
                HttpResponseMessage response = await client.PostAsync(serverUrl, content);
                string responseText = await response.Content.ReadAsStringAsync();
                Debug.Log("Response: " + responseText);
            }
            catch (System.Exception e)
            {
                Debug.LogError("Error sending image: " + e.Message);
            }
        }
    }

    public void StartSendingImages()
    {
        StartCoroutine(CaptureAndSend());
    }

    public void StopSendingImages()
    {
        StopAllCoroutines();
    }
}
