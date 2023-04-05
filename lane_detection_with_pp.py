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
def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

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
    
    # Filter out unwanted lines
    left_lines, right_lines = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue # ignore vertical lines
        slope = (y2 - y1) / (x2 - x1)
        if abs(slope) < 0.5:
            continue # ignore lines that are not steep enough
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)
    
    # Average the remaining lines
    left_line = np.average(left_lines, axis=0)
    right_line = np.average(right_lines, axis=0)
    
    # Draw the lanes on the image
    line_image = np.zeros_like(image)
    if left_line is not None:
        draw_lines(line_image, [left_line], color=[255, 0, 0], thickness=10)
    if right_line is not None:
        draw_lines(line_image, [right_line], color=[255, 0, 0], thickness=10)
    
    # Combine the lane image with the original image
    lane_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    
    return lane_image

# Test the lane detection function on an image
image = cv2.imread('test_image.jpg')
lane_image = lane_detection(image)
cv2.imshow('Lane detection', lane_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
