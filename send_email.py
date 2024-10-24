import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from utils_consts import to_addresses,subject,body
from remove_csv_and_xlsx_files import *
from datetime import datetime


load_dotenv()


def send_email(to_addresses, subject, body):
    # Set up the email server and login credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    #email_address = 'tariq.khasawneh@devoteam.com'
    email_address = "omarkamalabuassaf1@gmail.com"
    email_password = os.getenv('EMAIL_PASSWORD')


    # Create the email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = ", ".join(to_addresses)  
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))
    today_date = datetime.today().strftime('%Y-%m-%d')
    # Attach the CSV file
    filename = f'tenders_{today_date}_filtered.xlsx'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(filename)}')

    msg.attach(part)
    attachment.close()

    # Connect to Gmail server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, to_addresses, text)

    server.quit()

    print('Email sent successfully!')
    remove_csv_and_xlsx_files()
    
if __name__ == '__main__':
    send_email(to_addresses, subject, body)




# import aiosmtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# import os
# from dotenv import load_dotenv
# from remove_csv_and_xlsx_files import remove_csv_and_xlsx_files

# load_dotenv()

# def send_email(to_addresses, subject, body, attachment_filename=None):
#     # Set up the email server and login credentials
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     email_address = "omarkamalabuassaf1@gmail.com"
#     email_password = os.getenv('EMAIL_PASSWORD')

#     # Create the email
#     msg = MIMEMultipart()
#     msg['From'] = email_address
#     msg['To'] = ", ".join(to_addresses)
#     msg['Subject'] = subject

#     # Attach the body of the email
#     msg.attach(MIMEText(body, 'plain'))

#     # Attach the CSV file if it exists
#     if attachment_filename and os.path.exists(attachment_filename):
#         try:
#             with open(attachment_filename, 'rb') as attachment:
#                 part = MIMEBase('application', 'octet-stream')
#                 part.set_payload(attachment.read())
#                 encoders.encode_base64(part)
#                 part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_filename)}')
#                 msg.attach(part)
#         except Exception as e:
#             print(f"Error attaching file: {e}")

#     # Connect to Gmail server and send the email asynchronously
#     try:
#         await aiosmtplib.send(
#             message=msg,
#             hostname=smtp_server,
#             port=smtp_port,
#             username=email_address,
#             password=email_password,
#             start_tls=True
#         )
#         print('Email sent successfully!')
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#     finally:
#         remove_csv_and_xlsx_files()