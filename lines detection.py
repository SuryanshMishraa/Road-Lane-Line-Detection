import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
img = cv2.imread("lines.png")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to the grayscale image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Detect lines using Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 60, minLineLength=40, maxLineGap=100)

# Draw lines on the original image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

# Convert BGR image to RGB for displaying with matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Display the edges
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(edges, cmap='gray')
plt.title("Edges")
plt.axis("off")

# Display the image with lines
plt.subplot(1, 2, 2)
plt.imshow(img_rgb)
plt.title("Image with Lines")
plt.axis("off")

# Save the image
cv2.imwrite("1.3_lines_with_gap.jpg", img)

# Show the plots
plt.show()