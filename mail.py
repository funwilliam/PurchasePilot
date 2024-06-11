import os
import email
import dotenv
import smtplib
import imaplib

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import decode_header
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart



dotenv.load_dotenv()

# 配置郵件伺服器和用戶憑證
SMTP_SERVER = os.getenv('MAIL_SERVER')
IMAP_SERVER = os.getenv('MAIL_SERVER')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
EMAIL_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
SMTP_PORT = os.getenv('SMTP_PORT')
IMAP_PORT = os.getenv('IMAP_PORT')

print(
    SMTP_SERVER,
    IMAP_SERVER,
    ACCOUNT_ADDRESS,
    EMAIL_PASSWORD,
    SMTP_PORT,
    IMAP_PORT
)

# def test_smtp_connection(to_address = 'William@minmax.com.tw', subject = 'test_2', body = 'hi', attachment_path=None):
#     try:
#         # 創建一個MIMEMultipart對象
#         msg = MIMEMultipart()
#         msg['From'] = ACCOUNT_ADDRESS
#         msg['To'] = to_address
#         msg['Subject'] = subject

#         # 添加郵件正文
#         msg.attach(MIMEText(body, 'plain'))

#         # 如果有附件，添加附件
#         if attachment_path:
#             attachment = open(attachment_path, "rb")
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload((attachment).read())
#             encode_base64(part)
#             part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
#             msg.attach(part)

#         # 設置SSL上下文
#         # context = ssl.create_default_context()

#         # 發送郵件
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             # server.starttls(context=context)  # 啟用TLS
#             server.login(ACCOUNT_ADDRESS, EMAIL_PASSWORD)
#             server.sendmail(ACCOUNT_ADDRESS, to_address, msg.as_string())
#             print("Email sent successfully")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

def test_smtp_connection():
    try:
        # context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # server.starttls(context=context)  # 啟用TLS
            server.login(ACCOUNT_ADDRESS, EMAIL_PASSWORD)
            print("SMTP connection successful")
    except Exception as e:
        print(f"SMTP connection failed: {e}")

def test_imap_connection():
    try:
        with imaplib.IMAP4(IMAP_SERVER, IMAP_PORT) as mail:
            mail.login(ACCOUNT_ADDRESS, EMAIL_PASSWORD)
            mail.select('inbox')
            status, messages = mail.search(None, 'ALL')
            if status == 'OK':
                print("IMAP connection successful")
                mail_ids = messages[0].split()
                for mail_id in mail_ids[-5:]:  # 只讀取最新的5封郵件
                    mail_id = mail_id.decode()  # 解碼mail_id
                    status, msg_data = mail.fetch(mail_id, '(RFC822)')
                    if status != 'OK':
                        print(f"Failed to fetch mail id {mail_id}")
                        continue

                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else 'utf-8')
                            from_ = msg.get("From")
                            print(f"Subject: {subject}")
                            print(f"From: {from_}")

                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))

                                    if "attachment" in content_disposition:
                                        filename = part.get_filename()
                                        if filename:
                                            if isinstance(filename, bytes):
                                                filename = filename.decode(encoding if encoding else 'utf-8')
                                            filepath = os.path.join(".", filename)
                                            with open(filepath, "wb") as f:
                                                f.write(part.get_payload(decode=True))
                                            print(f"Attachment {filename} downloaded")
                                    elif content_type == "text/plain" and "attachment" not in content_disposition:
                                        body = part.get_payload(decode=True).decode()
                                        print(f"Body: {body}")
                            else:
                                content_type = msg.get_content_type()
                                body = msg.get_payload(decode=True).decode()
                                if content_type == "text/plain":
                                    print(f"Body: {body}")
            else:
                print(f"IMAP connection failed: {status} - {messages}")
    except imaplib.IMAP4.error as e:
        print(f"IMAP login failed: {e}")
    except Exception as e:
        print(f"IMAP connection failed: {e}")

if __name__ == "__main__":
    test_smtp_connection()
    # test_imap_connection()
