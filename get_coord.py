import cv2
import os

curPath = os.getcwd()

# C:\Users\User\Desktop\labelTool\dataset\images
path = os.path.join(curPath, 'dataset', 'images')
# ['18_2_2023_09_13_00_00.jpg', ...]
imgs = os.listdir(path)

img = cv2.imread(os.path.join(path, imgs[11]))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "(%d,%d)" % (x, y)
        print(x, y)
        print(f'BGR : {img[y, x]}')
        print(f'HSV : {hsv[y, x]}')
        print()
        cv2.circle(img, (x, y), 2, (0, 0, 255))
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
        cv2.imshow("image", img)

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
while(True):
    cv2.imshow("image", img)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()