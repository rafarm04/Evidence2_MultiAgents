using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class YoloDetection : MonoBehaviour
{
    public CameraCapture cameraCapture; // Reference to the CameraCapture script
    public string yoloServerUrl = "http://127.0.0.1:5000/get_detection";  // YOLO server URL

    void Start()
    {
        if (cameraCapture == null)
        {
            Debug.LogError("CameraCapture script is not assigned in the Inspector!");
            return;
        }

        // Start periodically sending images to the YOLO server
        InvokeRepeating(nameof(SendImageToYoloServer), 2f, 1f);
    }

    void SendImageToYoloServer()
    {
        if (cameraCapture == null)
        {
            Debug.LogError("CameraCapture script reference is missing!");
            return;
        }

        byte[] imageBytes = cameraCapture.GetImageBytes();
        if (imageBytes == null || imageBytes.Length == 0)
        {
            Debug.LogError("Failed to retrieve valid image bytes from CameraCapture.");
            return;
        }

        StartCoroutine(PostImage(imageBytes));
    }

    IEnumerator PostImage(byte[] imageBytes)
{
    // Create a form to send the image as "multipart/form-data"
    WWWForm form = new WWWForm();
    form.AddBinaryData("image", imageBytes, "photo.png", "image/png");

    UnityWebRequest request = UnityWebRequest.Post(yoloServerUrl, form);

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        Debug.Log("YOLO Detection Results: " + request.downloadHandler.text);
        ProcessDetectionResults(request.downloadHandler.text);
    }
    else
    {
        Debug.LogError($"Failed to send image: {request.error}");
        Debug.LogError($"Response Code: {request.responseCode}");
        Debug.LogError($"Response: {request.downloadHandler.text}");
    }
}


    void ProcessDetectionResults(string jsonResponse)
    {
        if (string.IsNullOrEmpty(jsonResponse))
        {
            Debug.LogWarning("Received empty or null response from YOLO server.");
            return;
        }

        // Parse and process detection results
        Debug.Log("Detection Results JSON: " + jsonResponse);
        // Further processing can be added here, e.g., highlighting detected objects.
    }
}
