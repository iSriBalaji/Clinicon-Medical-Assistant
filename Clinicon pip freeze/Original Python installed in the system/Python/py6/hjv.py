import smptlib
s=smtplib.SMTP("smtp.gmail.com", 465)
s.ehlo()
s.starttls()
s.login("c.medineers@gmail.com", "sih2019_medi")
