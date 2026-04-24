import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER


class EmailSender:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.user = EMAIL_USER
        self.password = EMAIL_PASS
        self.receiver = EMAIL_RECEIVER

    def _connect(self) -> smtplib.SMTP_SSL:
        server = smtplib.SMTP_SSL(self.host, self.port)
        server.login(self.user, self.password)
        return server

    def _build_message(self, subject: str, body: str, attachment: Path = None) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.user
        msg["To"] = self.receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        if attachment and attachment.exists():
            with open(attachment, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment.name}")
                msg.attach(part)

        return msg

    def send(self, subject: str, body: str, attachment_path: str = None) -> bool:
        try:
            attachment = Path(attachment_path) if attachment_path else None
            msg = self._build_message(subject, body, attachment)
            with self._connect() as server:
                server.sendmail(self.user, self.receiver, msg.as_string())
            print(f"[email] sent — {subject}")
            return True
        except Exception as e:
            print(f"[email] failed — {e}")
            return False

    def send_report(self, csv_path: str, source: str, deal_count: int) -> bool:
        subject = f"Price Monitor Report — {deal_count} deal(s) found"
        body = f"""
        <h2>Competitor Monitor Report</h2>
        <p>Source: <strong>{source}</strong></p>
        <p>Deals found below threshold: <strong>{deal_count}</strong></p>
        <p>Full data attached as CSV.</p>
        <br/>
        <small>Powered by competitor-price-monitor</small>
        """
        return self.send(subject, body, csv_path)
