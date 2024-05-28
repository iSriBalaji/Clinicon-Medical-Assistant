import cv2
import time
vid=cv2.VideoCapture(0)
check,frame=vid.read()
print(check)
cv2.imshow("Captured",frame)
cv2.waitKey(0)
time.sleep(5)
vid.release()
cv2.destroyAllWindows()
