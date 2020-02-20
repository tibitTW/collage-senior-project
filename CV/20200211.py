import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('src/g.jpg')
plt.imshow(img)

t1, t2 = 250, 430
edges = cv.Canny(img, t1, t2)

cnts, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
print(len(cnts))
for pic, contour in enumerate(cnts):
    area = cv.contourArea(contour)
    x, y, w, h = cv.boundingRect(contour)
    print(f'({x}, {y})', f'{w} x {h}, size', area)
    if y > 100: img = cv.drawContours(img, contour, -1, (153, 51, 204), 2)

cv.imwrite('oput_0211.jpg', img)

plt.subplot(141), plt.imshow(edges), plt.title('Edges')
plt.subplot(142), plt.imshow(img), plt.title('Image')
plt.show()