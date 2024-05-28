import smtplib
MY_EMAIL = "sribalajimuruganandam@gmail.com" #From this mail id, the alerts will be sent
MY_PASSWORD = "ilMSt0m!" #Enter the email id's password
with smtplib.SMTP("smtp.gmail.com",587, timeout=120) as connection:
    print("Hellooo")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
                            from_addr=MY_EMAIL,
                            to_addrs=["srisvit@gmail.com"], #for multiple receipients, add another email id after a comma in the list
                            msg="hELLO EMAIL PYTHON AUTOMATION"
                        )
