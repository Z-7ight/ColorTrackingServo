import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
from picamera2 import Picamera2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

panServo = 18
tiltServo = 16

panAngle = 90
tiltAngle = 160
alpha = 0.25
smoothedPanAngle = panAngle
smoothedTiltAngle = tiltAngle

# Function to set servo angle
def setServoAngle(servo, angle):
    GPIO.setup(servo, GPIO.OUT)
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18.0 + 3.0
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()

# Frame dimensions
frame_w = 320
frame_h = 240
center_x = frame_w // 2
center_y = frame_h // 2

# Boundary margin
margin = 50
LEFT_BOUND = center_x - margin
RIGHT_BOUND = center_x + margin
UPPER_BOUND = center_y - margin
LOWER_BOUND = center_y + margin

# Flag to enable/disable servo tracking
servo_enabled = False

# Function to move servo based on object position
def mapObjectPosition(x, y):
    global panAngle, tiltAngle, smoothedPanAngle, smoothedTiltAngle

    # Horizontal control
    if x < LEFT_BOUND:
        panAngle = min(panAngle + 10, 150)
    elif x > RIGHT_BOUND:
        panAngle = max(panAngle - 10, 30)

    # Vertical control
    if y < UPPER_BOUND:
        tiltAngle = max(tiltAngle - 10, 90)
    elif y > LOWER_BOUND:
        tiltAngle = min(tiltAngle + 10, 180)
    
    # smoothed_angle = alpha * new_angle + (1 - alpha) * old_smoothed_angle
    smoothedPanAngle = alpha * panAngle + (1 - alpha) * smoothedPanAngle
    smoothedTiltAngle = alpha * tiltAngle + (1 - alpha) * smoothedTiltAngle
    
    setServoAngle(panServo, smoothedPanAngle)
    setServoAngle(tiltServo, smoothedTiltAngle)
    
# Initialize servo angles
setServoAngle(panServo, panAngle)
setServoAngle(tiltServo, tiltAngle)

# HSV tolerances
hue_range = 10
sat_range = 40
val_range = 40

lower_hsv = np.array([0, 100, 100], dtype=np.uint8)
upper_hsv = np.array([10, 255, 255], dtype=np.uint8)

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (frame_w, frame_h)})
picam2.configure(config)
picam2.start()

# ROI dimensions
roi_w = 260
roi_h = 190
roi_x = center_x - roi_w // 2
roi_y = center_y - roi_h // 2

while True:
    frame = picam2.capture_array()
    # Convert from RGB to BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Draw one bounding rectangle instead of four lines
    cv2.rectangle(
        frame,
        (LEFT_BOUND, UPPER_BOUND),
        (RIGHT_BOUND, LOWER_BOUND),
        (255, 0, 0),
        1
    )

    # Extract ROI and convert to HSV
    roi_frame = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    hsv_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # Center sampling region
    height, width = hsv_frame.shape[:2]
    size = 30
    cx1 = width // 2 - size // 2
    cy1 = height // 2 - size // 2
    cx2 = cx1 + size
    cy2 = cy1 + size
    cv2.rectangle(roi_frame, (cx1, cy1), (cx2, cy2), (0, 255, 255), 2)

    # Threshold mask
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # Morphological operations
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # Draw bounding rectangle on the main frame
        cv2.rectangle(
            frame,
            (x + roi_x, y + roi_y),
            (x + roi_x + w, y + roi_y + h),
            (0, 255, 0),
            2
        )

        # Object center in white
        target_x = x + w // 2
        target_y = y + h // 2
        cv2.circle(frame, (target_x + roi_x, target_y + roi_y), 3, (255, 255, 255), -1)

        # Move servos if enabled
        if servo_enabled:
            mapObjectPosition(target_x + roi_x, target_y + roi_y)

    # Display frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        # Enable servo after pressing space
        servo_enabled = True

        # Recompute HSV range based on center of ROI
        roi_center = hsv_frame[cy1:cy2, cx1:cx2]
        mean_hsv = cv2.mean(roi_center)[:3]
        h_mean, s_mean, v_mean = mean_hsv

        lower_h = max(h_mean - hue_range, 0)
        upper_h = min(h_mean + hue_range, 180)
        lower_s = max(s_mean - sat_range, 0)
        upper_s = min(s_mean + sat_range, 255)
        lower_v = max(v_mean - val_range, 0)
        upper_v = min(v_mean + val_range, 255)

        lower_hsv = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
        upper_hsv = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)
        print("New HSV range:", lower_hsv, upper_hsv)

# Reset servos and cleanup
setServoAngle(panServo, 90)
setServoAngle(tiltServo, 160)
GPIO.cleanup()
cv2.destroyAllWindows()
