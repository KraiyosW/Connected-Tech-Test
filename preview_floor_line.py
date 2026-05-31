import cv2
import numpy as np

# Read frame
cap = cv2.VideoCapture('entrance.mov')
cap.set(cv2.CAP_PROP_POS_FRAMES, 500)
ret, frame = cap.read()
cap.release()

if ret:
    # Draw floor line
    # Adjust coordinates based on the door threshold
    # From previous ROI: door is around x=250 to 1000, y=100 to 900
    # Let's draw a line across the bottom of the door
    pt1 = (450, 750) # Left side of door frame on the floor
    pt2 = (900, 750) # Right side of door frame on the floor
    
    cv2.line(frame, pt1, pt2, (0, 255, 255), 4)
    cv2.putText(frame, "Floor Counting Line", (pt1[0], pt1[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imwrite('floor_line_preview.jpg', frame)
    print("Saved preview to floor_line_preview.jpg")
else:
    print("Failed to read video")
