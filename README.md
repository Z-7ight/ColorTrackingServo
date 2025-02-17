# 📌 **ColorTrackingServo**

*A Raspberry Pi-based object tracking system using OpenCV, HSV color filtering, and servo motors.*

**一个基于 Raspberry Pi 和 OpenCV 的目标跟踪系统，通过 HSV 颜色过滤识别目标，并使用舵机调整摄像头方向进行跟踪。**

---

## 📖 **Features | 功能**
✅ Real-time object tracking using color detection.  
✅ Smooth servo movement to reduce jitter using filtering techniques.  
✅ Raspberry Pi + OpenCV-based implementation.  
✅ Supports PiCamera and standard USB cameras.  

✅ **基于颜色检测的实时目标跟踪**  
✅ **平滑舵机控制，减少抖动**  
✅ **Raspberry Pi + OpenCV 实现**  
✅ **支持 PiCamera 及普通 USB 摄像头**

---

## 🔧 **Hardware Requirements | 硬件需求**
- Raspberry Pi (Recommended: Raspberry Pi 4B)  
- PiCamera (or USB webcam)  
- 2x SG90 Mini Servos  
- Adafruit 1967 Mini Pan-Tilt Bracket  
- GPIO wiring for servo control  

- **树莓派（推荐 Raspberry Pi 4B）**  
- **PiCamera（或 USB 摄像头）**  
- **2 个 SG90 迷你舵机**  
- **Adafruit 1967 迷你云台支架**  
- **用于舵机控制的 GPIO 连接**

---

## 🚀 **Installation & Setup | 安装与配置**
### 1️⃣ **Clone the repository | 克隆仓库**
```bash
git clone https://github.com/yourusername/ColorTrackingServo.git
cd ColorTrackingServo
```

### 2️⃣ **Install dependencies | 安装依赖**
```bash
pip install -r requirements.txt
```
**Dependencies (依赖项)**:
- `opencv-python`
- `numpy`
- `RPi.GPIO`
- `picamera2`

### 3️⃣ **Run the script | 运行程序**
```bash
python ColorTrackingServo.py
```
The script will start tracking the target based on the defined HSV color range.  
**该程序会根据设定的 HSV 颜色范围开始追踪目标。**

---

## 🎯 **Usage Guide | 使用指南**
1️⃣ **Place an object of the target color in front of the camera.**  
2️⃣ **Press SPACE to enable servo tracking.**  
3️⃣ **The servos will move the camera to keep the target centered.**  
4️⃣ **Press 'q' to quit the program.**  

1️⃣ **将目标颜色的物体放置在摄像头前。**  
2️⃣ **按下空格键启用舵机跟踪。**  
3️⃣ **舵机将自动调整摄像头角度，使目标保持在中心。**  
4️⃣ **按 'q' 退出程序。**

---

## 🛠 **Customization | 自定义设置**
**Modify the HSV range in `ColorTrackingServo.py` to track different colors. OR you can use space button (whenever) to automatically detect the color.**  
在 `ColorTrackingServo.py` 文件中修改 HSV 颜色范围或者按空格来自动确认颜色，以跟踪不同的目标：
```python
lower_hsv = np.array([0, 100, 100], dtype=np.uint8)  # Adjust for target color
upper_hsv = np.array([10, 255, 255], dtype=np.uint8)
```

**Adjust the servo motion smoothing parameters to reduce jitter.**  
调整舵机平滑参数以减少抖动：
```python
alpha = 0.25  # Exponential Moving Average smoothing factor
```

---

## 🏆 License | 许可协议
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。
