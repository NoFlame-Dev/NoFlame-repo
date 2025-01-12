import cv2
import requests
import time

def capture_image(filename="image.jpeg"):
    # Initialize webcam
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return False

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read from webcam.")
        cap.release()
        return False

    # Save the image to file
    cv2.imwrite(filename, frame)
    cap.release()
    return True

def post_image(filename, url="http://localhost:5000/upload_image"):
    try:
        with open(filename, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            print(f"Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during HTTP POST: {e}")

def main():
    filename = "image.jpeg"
    url = "http://localhost:5000/upload_image"

    while True:
        print("Capturing image...")
        if capture_image(filename):
            print(f"Image saved as {filename}. Sending to {url}...")
            post_image(filename, url)
        else:
            print("Skipping this cycle due to capture error.")

        print("Waiting for 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    main()
