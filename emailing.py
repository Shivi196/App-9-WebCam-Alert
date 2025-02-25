import smtplib
import imghdr #imported to check what is the type of image like png,jpg or wht although this is obsolete lib now alternative lib you can use in Pillow library
from email.message import EmailMessage


SENDER = "sharmabruno310@gmail.com"
PASSWORD = "hxfr tumk gern jcaz" #this pswd we create by goin to gmail and manage your google a/c and creating pswd in App passwords after enabling 2 step verification. This pswd will give python to access our gmail and send emails
RECEIVER = "sharmabruno310@gmail.com"

def send_email(image_path):
    print("Send email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New Customer showed up!!"
    email_message.set_content("Hey we just saw a new customer!!")

    with open(image_path,"rb") as binary_file:
       content =  binary_file.read()
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))

    gmail = smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER,email_message.as_string())
    gmail.quit()
    print("Send email function ended")

if __name__ == "__main__":
    send_email(image_path="/Users/misha/PycharmProjects/app9-webcam-alert/images/29.png")
    # print("Email was sent!!")