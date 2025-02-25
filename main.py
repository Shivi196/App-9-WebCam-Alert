import os
import cv2
import time
from emailing import send_email
import glob
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

firstFrame = None
status_list = []
count = 1

def clean_folder():
    print("clean function started ")
    images = glob.glob("/Users/misha/PycharmProjects/app9-webcam-alert/images/*.png")
    for image in images:
     os.remove(image)
    print("clean function ended ")

while True:
    status = 0
    check,frame = video.read()

    # preprocessing the video images into grayscale and blurred so that it decreases the matrix no as bgr matrix is way complex to perform the subtract operation on frames to detect new object entered in frame
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurr_frame_gaus = cv2.GaussianBlur(gray_frame,(21,21),0)

    #Subtraction of new frame with the firstframe in the video to get the new object entered in webcam
    if firstFrame is None:
        firstFrame = blurr_frame_gaus

    delta_frame = cv2.absdiff(firstFrame,blurr_frame_gaus)
    # in delta_frame the image in video in quite grey and also bgd with noises or information there, you can put this delta_frame in imshow method and run program to check how image in video looks now
    # now we need to move to second stage where in we need to make my image white and whole bgd as black so it will be black and white in the frame. So we have only white pixels where there is object and black pixels when no object .
    # This is a classification of pixels based on threshold
    # if nos in matrix closer to 0 then it's black and if it's closer to 255 then its white background

    # print(delta_frame)

    # Setting threshold to classify the delta_frame pixels and pixels who is having 67or more threshold will replace it with white pixels i.e 255
    thresh_frame =cv2.threshold(delta_frame,67,255,cv2.THRESH_BINARY)[1]

    # To remove the noise from the image we want to dilate it as below
    dil_frame = cv2.dilate(thresh_frame,None,iterations=2)
    # cv2.imshow("My Video", dil_frame)

    # now in next stage we need to contour our white image as below , contouring is required for nxt step to make underline rectangle on our face
    contours,check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

        if rectangle.any():
            status = 1
        cv2.imwrite(f"/Users/misha/PycharmProjects/app9-webcam-alert/images/{count}.png",frame)  # remember approx. 30 frames generated per second so if video is of 5sec so 150 images will be there in that video
        count = count + 1
        all_images = glob.glob("/Users/misha/PycharmProjects/app9-webcam-alert/images/*.png")
        index = int(len(all_images)/2)
        img_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    # here 1 means object entered into frame and 0 means object left from the frame and then email willl be sent

    if status_list[0] == 1 and status_list[1] == 0:
        # send_email(img_with_object)
        email_thread = Thread(target=send_email,args=(img_with_object,),daemon=True) #we have type comma in args so it take it as tuple not string
        email_thread.start()
        email_thread.join()  # Wait until email is sent before cleaning folder

        clean_thread = Thread(target=clean_folder, daemon=True)
        clean_thread.start()
        # clean_folder()

    print(status_list)

    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)

    if key==ord("q"):
        break

video.release()

clean_folder()
cv2.destroyAllWindows()











# check2,frame2 = video.read()
# time.sleep(1)
#
# check3,frame3 = video.read()



# print(check)
# print(frame3)
# time.sleep(1)

