import cv2  # Image processing
import time  # Delay
import imutils  # Resize images

# Initialize camera
cam = cv2.VideoCapture(0)
time.sleep(0)
firstFrame = None
area = 500
frameUpdateInterval = 100  # Update the reference frame every 100 frames
frameCount = 0

while True:
    ret, img = cam.read()  # Read frame from camera
    if not ret:
        break

    text = "Normal"
    img = imutils.resize(img, width=600)  # Resize the frame
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)  # Smooth the image

    # Update the reference frame every frameUpdateInterval frames
    if firstFrame is None or frameCount % frameUpdateInterval == 0:
        firstFrame = gaussianImg
        frameCount = 0

    frameCount += 1

    # Compute the absolute difference between the current frame and the reference frame
    imgDiff = cv2.absdiff(firstFrame, gaussianImg)

    # Apply thresholding to get the binary image
    threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
    threshImg = cv2.dilate(threshImg, None, iterations=2)

    # Find contours
    cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        # Ignore small contours
        if cv2.contourArea(c) < area:
            continue

        # Draw bounding box around detected object
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Moving Object detected"

    # Display status
    cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("cameraFeed", img)

    # Exit on pressing 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
