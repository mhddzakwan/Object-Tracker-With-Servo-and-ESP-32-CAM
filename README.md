# Object Tracking with 2 Servo and ESP 32 CAM
I made a project where the camera (ESP32 cam) will follow the movement of an object using the help of 2 pan (Horizontal) and tilt (Vertical) servos. For example, when the object moves to the left, the camera will move to the left. For more information, you can watch my video : 
https://www.youtube.com/watch?v=2TU9Fy5hJ-A

Here is step by step to make this project:
1. Wiring Project

![Alt text](img/wiring.png)

Tips:
- Use 2 different battery sources. Each 5V. The first battery is for the ESP 32 cam, the second battery is for other electronics.

2. Upload Code to WEMOS
Upload arduino.txt to your WEMOS

3. Upload Code to ESP 32 CAM

![Alt text](img/ESP 32 CAM.png)

Plug your ESP 32 cam then sellect the board. User example code from the ESP 32 CAM

4. Run Python Code in your computer
Before arduino color tracking camera.py. make sure you read this:

change this code with your IP from ESP 32 cam
```c
ip_cam_url = "http://192.168.220.211:81/stream"  # Sesuaikan dengan IP ESP32-CAM
```

You can change the object color with this code:
```c
color = "#581845"
```

I add this code because i got some delay with esp 32 cam and my bluetooth communication, so i make some delay to my code:

```c
current_time = time.time()
    if current_time - last_sent >= 0.4:  # 400 ms = 0.4 detik
        ser.write(('a' + str(int(Xposition)) + 'b' + str(int(Yposition))).encode())
        last_sent = current_time
```

After all, you can run the code, then change value in the upper right corner to > 300, if not, the servo will not move.


