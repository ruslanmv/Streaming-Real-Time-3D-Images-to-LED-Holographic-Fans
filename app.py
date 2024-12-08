import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests
from PIL import Image
import io
import time

# Define the fan's API endpoint
FAN_API_URL = "http://<fan-ip-address>/upload_frame"  # Replace with your fan's IP address

# Initialize the 3D plot
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

def generate_frame(angle):
    """
    Generate a single frame of a rotating 3D spiral.
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(-1, 1, 100)
    x = np.sin(theta)
    y = np.cos(theta)

    ax.clear()
    ax.plot(x, y, z, color='b')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.view_init(elev=20, azim=angle)

    # Render the frame to a NumPy array
    fig.canvas.draw()
    frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return frame

def send_frame_to_fan(frame):
    """
    Send a single frame to the 3D LED fan.
    """
    buffer = io.BytesIO()
    image = Image.fromarray(frame)
    image.save(buffer, format="PNG")
    buffer.seek(0)

    try:
        response = requests.post(FAN_API_URL, files={'frame': buffer})
        if response.status_code == 200:
            print("Frame sent successfully")
        else:
            print(f"Failed to send frame: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending frame: {e}")

def stream_frames():
    """
    Main loop to generate and stream frames to the fan in real-time.
    """
    angle = 0
    try:
        while True:
            frame = generate_frame(angle)
            send_frame_to_fan(frame)
            angle += 5
            time.sleep(0.033)  # ~30 FPS
    except KeyboardInterrupt:
        print("Streaming stopped by user.")

if __name__ == "__main__":
    print("Starting real-time streaming to the LED fan...")
    stream_frames()
