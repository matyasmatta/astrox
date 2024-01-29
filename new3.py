import cv2
import numpy as np
import time
from threading import Thread

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, resolution=(640,480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True

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

# Initialize video stream
videostream = VideoStream(resolution=(640,480), framerate=30).start()
time.sleep(1)

try:
    while True:
        # Grab frame from video stream
        frame = videostream.read()

        # Find center of mass for light and dark elements
        light_center = find_color_center(frame, light_lower, light_upper)
        dark_center = find_color_center(frame, dark_lower, dark_upper)

        # Draw circles at the found centers
        if light_center is not None:
            cv2.circle(frame, light_center, 10, (0, 255, 0), -1)

        if dark_center is not None:
            cv2.circle(frame, dark_center, 10, (0, 0, 255), -1)

        # Calculate distance if both centers are found
        if light_center is not None and dark_center is not None:
            distance = calculate_distance(light_center, dark_center)
            cv2.putText(frame, f"Distance: {distance:.2f} pixels", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow("Light and Dark Elements Detection", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

finally:
    # Clean up
    cv2.destroyAllWindows()
    videostream.stop()
print("Hello world")