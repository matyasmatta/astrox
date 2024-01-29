import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import numpy as np

# Initialize PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to find the center of mass of a color range in the image
def find_color_center(image, lower, upper):
    mask = cv2.inRange(image, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
    
    return None

# Define color ranges for light and dark elements
light_lower = np.array([200, 200, 200], dtype="uint8")
light_upper = np.array([255, 255, 255], dtype="uint8")

dark_lower = np.array([0, 0, 0], dtype="uint8")
dark_upper = np.array([50, 50, 50], dtype="uint8")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    image = frame.array

    # Find center of mass for light and dark elements
    light_center = find_color_center(image, light_lower, light_upper)
    dark_center = find_color_center(image, dark_lower, dark_upper)

    # Draw circles at the found centers
    if light_center is not None:
        cv2.circle(image, light_center, 10, (0, 255, 0), -1)

    if dark_center is not None:
        cv2.circle(image, dark_center, 10, (0, 0, 255), -1)

    # Calculate distance if both centers are found
    if light_center is not None and dark_center is not None:
        distance = calculate_distance(light_center, dark_center)
        cv2.putText(image, f"Distance: {distance:.2f} pixels", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Light and Dark Elements Detection", image)

    # Clear the stream for the next frame
    rawCapture.truncate(0)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
