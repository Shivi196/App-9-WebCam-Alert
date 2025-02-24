import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

firstFrame = None

while True:

    check,frame = video.read()

    # preprocessing the video images into grayscale and blurred so that it decreases the matrix no as bgr matrix is way complex to perform the subtract operation on frames to detect new object entered in frame
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurr_frame_gaus = cv2.GaussianBlur(gray_frame,(21,21),0)

    #Subtraction of new frame with the firstframe in the video to get the new object entered in webcam
    if firstFrame is None:
        firstFrame = blurr_frame_gaus

    delta_frame = cv2.absdiff(firstFrame,blurr_frame_gaus)
    # in delta_frame the image in video in quite grey and also bgd with noises or information there, you can put this delta_frame in imshow method and run program to check how image in vidoe looks now
    # now we need to move to second stage where in we need to make my image white and whole bgd as black so it will be black and white in the frame. So we have only white pixels where there is object and black pixels when no object .
    # This is a classification of pixels based on threshold
    # if nos in matrix closer to 0 then it's black and if it's closer to 255 then its white background

    # print(delta_frame)
    # Setting threshold to classify the delta_frame pixels and pixels who is having 67or more threshold will replace it with white pixels i.e 255
    thresh_frame =cv2.threshold(delta_frame,67,255,cv2.THRESH_BINARY)[1]
    # To remove the noise from the image we want to dilate it as below
    dil_frame = cv2.dilate(thresh_frame,None,iterations=2)
    cv2.imshow("My Video", dil_frame)
    # now in next stage we need to contour our white image as below , contouring is required for nxt step to make underline rectangle on our face
    contours,check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.imshow("Video",frame)
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

