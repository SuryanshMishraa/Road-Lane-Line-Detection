import cv2
import numpy as np

video = cv2.VideoCapture("road_cv.mp4")

# Set the frame rate of the video (assuming 30 FPS)
fps = video.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps * 4)  # Set delay for 0.25x speed (adjust if needed)

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture("road_cv.mp4")
        continue

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Adjusted HSV range for white lanes
    low_white = np.array([0, 0, 200])
    up_white = np.array([180, 40, 255])
    mask = cv2.inRange(hsv, low_white, up_white)
    
    # Focus on the lower part of the frame where lane markings usually appear
    height, width = mask.shape
    roi_mask = np.zeros_like(mask)
    roi_mask[int(height * 0.6):, :] = mask[int(height * 0.6):, :]
    
    edges = cv2.Canny(roi_mask, 75, 150)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Filter based on line length and position
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if length > 50 and y1 > height * 0.6:  # Minimum length and position filter
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow("frame", frame)
    cv2.imshow("edges", edges)

    key = cv2.waitKey(delay)  # Adjusted delay for slower playback
    if key == 27:  # Escape key to exit
        break

video.release() 
cv2.destroyAllWindows()
