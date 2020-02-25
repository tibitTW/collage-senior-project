import cv2 as cv

video = cv.VideoCapture('src/test1.mp4')

f_count = 0
while video.isOpened():
    ret, frame = video.read()
    if not ret: break
    cv.imwrite(f'./test/frame_{f_count:02d}.jpg', frame)
    f_count += 1
    cv.imshow('frame', frame)
    
    if cv.waitKey(1) == ord('q'): break

video.release()
cv.destroyAllWindows()