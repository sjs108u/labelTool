import cv2
import os
import numpy as np

def is_in_poly(point, poly):
    # https://blog.csdn.net/leviopku/article/details/111224539
    px, py = point
    is_in = False

    for i, corner in enumerate(poly):
        next_i = (i + 1) % len(poly)
        x1, y1 = corner
        x2, y2 = poly[next_i]

        if (x1 == px and y1 == py) or (x2 == px and y2 == py):
            is_in = True
            break

        if min(y1, y2) < py <= max(y1, y2):
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:
                is_in = True
                break
            elif x > px:
                is_in = not is_in
    return is_in

curPath = os.getcwd()

# C:\Users\User\Desktop\labelTool\dataset\images
path = os.path.join(curPath, 'dataset', 'images')
# ['18_2_2023_09_13_00_00.jpg', ...]
imgs = os.listdir(path)

img = cv2.imread(os.path.join(path, imgs[36])) #23 good, #11 bad
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 30, 255])

frame = img
cv2.imshow('Capture', frame)
mask = cv2.inRange(hsv, lower_white, upper_white)
# cv2.imshow('Mask', mask)

poly_mask = np.zeros(img.shape[:2], np.uint8)
for x in range(305, 645):
    for y in range(95, 1190):
        if mask[x][y] == 255 and is_in_poly([x, y], [[315, 319], [644, 98], [595, 1188], [308, 962]]):
            poly_mask[x][y] = 255

mask = cv2.bitwise_and(mask, poly_mask)

res = cv2.bitwise_and(frame, frame, mask=mask)
# cv2.imshow('Result', res)

mask_gbr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
mask_gbr[mask==255] = (0, 0, 255)
cv2.imshow('Mask', mask_gbr)
final_img = cv2.addWeighted(frame, 0.7, mask_gbr, 1, 0)
cv2.line(final_img, (319, 315), (98, 644), (0, 0, 255), 2)
cv2.line(final_img, (98, 644), (1188, 595), (0, 0, 255), 2)
cv2.line(final_img, (1188, 595), (962, 308), (0, 0, 255), 2)
cv2.line(final_img, (962, 308), (319, 315), (0, 0, 255), 2)
cv2.imshow('final', final_img)

cv2.waitKey(0)
cv2.destroyAllWindows()