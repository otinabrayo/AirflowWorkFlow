import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test email from Airflow")
msg['Subject'] = "Test Email"
msg['From'] = "otibra00@gmail.com"
msg['To'] = "marionkoki00@gmail.com"

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("otibra00@gmail.com", "qqullnfzzkhukfwd")
        server.sendmail("otibra00@gmail.com", "marionkoki00@gmail.com", msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")