import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

while True:

    check,frame = video.read()
    cv2.imshow("My Video",frame)

    key = cv2.waitKey(1)

    if key==ord("q"):
        break

video.release()


# check2,frame2 = video.read()
# time.sleep(1)
#
# check3,frame3 = video.read()



# print(check)
# print(frame3)
# time.sleep(1)

