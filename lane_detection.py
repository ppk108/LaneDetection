import cv2
import numpy as np

# Define the region of interest (ROI) for lane detection
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# Define the Hough lines algorithm for detecting lines
def draw_lines(img, lines):
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)

# Define the main function for lane detection
def lane_detection(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Define parameters for Canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    
    # Define ROI for lane detection
    height, width = edges.shape
    roi_vertices = [(0, height), (width/2, height/2), (width, height)]
    roi_edges = region_of_interest(edges, np.array([roi_vertices], np.int32))
    
    # Define parameters for Hough lines detection
    rho = 2
    theta = np.pi/180
    threshold = 50
    min_line_length = 100
    max_line_gap = 100
    lines = cv2.HoughLinesP(roi_edges, rho, theta, threshold, np.array([]), 
                            minLineLength=min_line_length, maxLineGap=max_line_gap)
    
    # Draw lines on original image
    line_image = np.zeros_like(image)
    if lines is not None:
        draw_lines(line_image, lines)
    
    # Combine line image with original image
    lane_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    
    return lane_image

# Test the lane detection function on an image
image = cv2.imread('test_image.jpg')
lane_image = lane_detection(image)
cv2.imshow('Lane detection', lane_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
