# Streaming Real-Time 3D Images to LED Holographic Fans (Missyou and GIWOX)**

This tutorial provides a step-by-step guide to stream real-time 3D images to LED holographic fans, specifically **Missyou** and **GIWOX** models. The pipeline includes setting up the Python environment, generating real-time 3D images, configuring the LED fan software, and integrating Python code for dynamic streaming.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Pipeline Overview](#pipeline-overview)
3. [Step 1: Set Up the Python Environment](#step-1-set-up-the-python-environment)
4. [Step 2: Install the LED Fan Software](#step-2-install-the-led-fan-software)
5. [Step 3: Generate a Simple 3D Model in Python](#step-3-generate-a-simple-3d-model-in-python)
6. [Step 4: Stream Real-Time Frames to the LED Fan](#step-4-stream-real-time-frames-to-the-led-fan)
7. [Full Python Code](#full-python-code)
8. [Testing and Debugging](#testing-and-debugging)
9. [Conclusion](#conclusion)

---

## **Prerequisites**

Before you start, ensure you have:
- A **Missyou** or **GIWOX** 3D LED holographic fan.
- Access to the fan's official software (downloadable from the manufacturer's website or included on a USB drive).
- A computer with Python installed.
- Wi-Fi or USB connectivity between your computer and the fan.

---

## **Pipeline Overview**

### **1. Python Environment**
We will set up a Python environment with the necessary libraries for 3D rendering and image processing.

### **2. Fan Configuration**
- Install the fan's software and configure it to accept external inputs (videos or images).
- Test connectivity with your fan using Wi-Fi or USB.

### **3. Real-Time 3D Rendering**
Generate real-time 3D images using Python. We will use `matplotlib` for visualization and `Pillow` for image conversion.

### **4. Streaming to the Fan**
Send generated frames to the fan in real-time using its API or manual upload.

---

## **Step 1: Set Up the Python Environment**

1. **Install Python (>= 3.8)**
   - Download and install Python from [python.org](https://www.python.org/).

2. **Create a Virtual Environment**
   ```bash
   python -m venv hologram_env
   source hologram_env/bin/activate  # On Windows: hologram_env\Scripts\activate
   ```

3. **Install Required Libraries**
   ```bash
   pip install matplotlib numpy pillow requests
   ```

---

## **Step 2: Install the LED Fan Software**

1. **Download and Install the Software**
   - For **Missyou** and **GIWOX**, install the official software from their website or included USB. This software allows content upload and basic configuration.

2. **Connect the Fan**
   - Use Wi-Fi:
     - Connect your computer to the fan’s Wi-Fi network.
     - Access the fan's control panel via its IP address (e.g., `192.168.x.x`) in a browser.
   - Use USB:
     - Connect the fan via a USB cable.
     - Ensure it is recognized by the fan's software.

3. **Test Content Upload**
   - Use the software to upload a static video or image to confirm connectivity.

---

## **Step 3: Generate a Simple 3D Model in Python**

We will create a 3D rotating spiral using `matplotlib`.

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Initialize the 3D plot
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

def generate_frame(angle):
    """Generate a single frame of a rotating 3D spiral."""
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
```

---

## **Step 4: Stream Real-Time Frames to the LED Fan**

We use the fan’s API for real-time frame uploads.

### **Python Code for Streaming**
```python
import requests
import time
from PIL import Image
import io

FAN_API_URL = "http://<fan-ip-address>/upload_frame"

def send_frame_to_fan(frame):
    """Send a single frame to the 3D LED fan."""
    buffer = io.BytesIO()
    image = Image.fromarray(frame)
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = requests.post(FAN_API_URL, files={'frame': buffer})
    if response.status_code == 200:
        print("Frame sent successfully")
    else:
        print(f"Failed to send frame: {response.status_code}")

# Real-time streaming loop
angle = 0
try:
    while True:
        frame = generate_frame(angle)
        send_frame_to_fan(frame)
        angle += 5
        time.sleep(0.033)  # ~30 FPS
except KeyboardInterrupt:
    print("Streaming stopped.")
```

---

## **Full Python Code**

Here’s the complete script combining frame generation and real-time streaming:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests
import time
from PIL import Image
import io

FAN_API_URL = "http://<fan-ip-address>/upload_frame"

# Initialize the 3D plot
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

def generate_frame(angle):
    """Generate a single frame of a rotating 3D spiral."""
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
    """Send a single frame to the 3D LED fan."""
    buffer = io.BytesIO()
    image = Image.fromarray(frame)
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = requests.post(FAN_API_URL, files={'frame': buffer})
    if response.status_code == 200:
        print("Frame sent successfully")
    else:
        print(f"Failed to send frame: {response.status_code}")

# Real-time streaming loop
angle = 0
try:
    while True:
        frame = generate_frame(angle)
        send_frame_to_fan(frame)
        angle += 5
        time.sleep(0.033)  # ~30 FPS
except KeyboardInterrupt:
    print("Streaming stopped.")
```

---

## **Testing and Debugging**

1. **Run the Python Script**
   - Ensure the fan is connected and accessible via the specified IP.
   - Run the script and check for successful frame uploads.

2. **Debug Connection Issues**
   - Ensure the fan's API endpoint (`FAN_API_URL`) is correct.
   - Test connectivity by uploading a static image using `curl` or Postman.

---

## **Conclusion**

This tutorial demonstrates how to generate real-time 3D animations in Python and stream them to LED holographic fans. With some customization, you can use this setup to create interactive and dynamic displays for advertising, events, or educational purposes.