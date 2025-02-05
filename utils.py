import cv2  
import numpy as np

def calculate_fill_percentage(processed_image):
    total_pixels = processed_image.size
    filled_pixels = cv2.countNonZero(processed_image)
    
    fill_percentage = (filled_pixels / total_pixels) * 100
    return fill_percentage
