import os
import pytest

from sanic_mailing import Mail, Message
from sanic import Sanic

CONTENT = "file test content"


@pytest.mark.usefixtures("app")
class TestConnection:

    async def test_connection(self, app: Sanic):
        message = Message(
            subject="test subject",
            recipients=["sabuhi.shukurov@gmail.com"],
            body="test",
            subtype="plain",
        )
    
        fm = Mail(app)
    
        await fm.send_message(message)
    
        assert message.body == "test"
        assert message.subtype == "plain"
        assert not message.template_body
        assert not message.html
    
    async def test_send_mail_method(self, app: Sanic):
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_mail(subject="test subject", message="test", recipients=["sabuhi.shukurov@gmail.com"])
    
            assert len(outbox) == 1
            mail = outbox[0]
            assert mail["To"] == "sabuhi.shukurov@gmail.com"
            assert mail["Subject"] == "test subject"
    
    async def test_send_mass_mail_method(self, app: "Sanic"):
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            datatuple = (
                ("test-subject-1", "message-body-1", ["sabuhi.shukurov@gmail.com"]),
                ("test-subject-2", "message-body-2", ["sabuhi.shukurov@gmail.com"]),
                ("test-subject-3", "message-body-3", ["sabuhi.shukurov@gmail.com"])
            )
            await fm.send_mass_mail(datatuple)
    
            assert len(outbox) == 3
            mail1, mail2, mail3 = tuple(outbox)
            assert mail1["To"] == "sabuhi.shukurov@gmail.com"
            assert mail1["Subject"] == "test-subject-1"
    
            assert mail2["To"] == "sabuhi.shukurov@gmail.com"
            assert mail2["Subject"] == "test-subject-2"
    
            assert mail3["To"] == "sabuhi.shukurov@gmail.com"
            assert mail3["Subject"] == "test-subject-3"
    
    
    async def test_html_message(self, app: "Sanic"):
        sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
        subject = "testing"
        to = "to@example.com"
        msg = Message(subject=subject, recipients=[to], html="html test")
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg)
    
            assert len(outbox) == 1
            mail = outbox[0]
            assert mail["To"] == to
            assert mail["From"] == sender
            assert mail["Subject"] == subject
            assert not msg.subtype
        assert msg.html == "html test"
    
    
    async def test_attachement_message(self, app: "Sanic"):
        directory = os.getcwd()
        attachement = directory + "/files/attachement.txt"
    
        with open(attachement, "w") as file:
            file.write(CONTENT)
    
        subject = "testing"
        to = "to@example.com"
        msg = Message(
            subject=subject,
            recipients=[to],
            html="html test",
            subtype="html",
            attachments=[attachement],
        )
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg)
            mail = outbox[0]
    
            assert len(outbox) == 1
            assert mail._payload[1].get_content_maintype() == "application"
            assert (
                mail._payload[1].__dict__.get("_headers")[0][1]
                == "application/octet-stream"
            )
    
    
    async def test_attachement_message_with_headers(self, app: "Sanic"):
        directory = os.getcwd()
        attachement = directory + "/files/attachement.txt"
    
        with open(attachement, "w") as file:
            file.write(CONTENT)
    
        subject = "testing"
        to = "to@example.com"
        msg = Message(
            subject=subject,
            recipients=[to],
            html="html test",
            subtype="html",
            attachments=[
                {
                    "file": attachement,
                    "headers": {"Content-ID": "test ID"},
                    "mime_type": "image",
                    "mime_subtype": "png",
                }
            ],
        )
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg)
    
            assert len(outbox) == 1
            mail = outbox[0]
            assert mail._payload[1].get_content_maintype() == msg.attachments[0][1].get(
                "mime_type"
            )
            assert mail._payload[1].get_content_subtype() == msg.attachments[0][1].get(
                "mime_subtype"
            )
    
            assert mail._payload[1].__dict__.get("_headers")[0][1] == "image/png"
            assert mail._payload[1].__dict__.get("_headers")[4][1] == msg.attachments[0][
                1
            ].get("headers").get("Content-ID")
    
    
    async def test_jinja_message_list(self, app: "Sanic"):
        sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
        subject = "testing"
        to = "to@example.com"
        persons = [
            {"name": "Andrej"},
        ]
        msg = Message(subject=subject, recipients=[to], template_body=persons)
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg, template_name="email.html")
    
            assert len(outbox) == 1
            mail = outbox[0]
            assert mail["To"] == to
            assert mail["From"] == sender
            assert mail["Subject"] == subject
        assert msg.subtype == "html"
        #assert msg.template_body == ("\n    \n    \n        Andrej\n    \n\n")
    
    
    async def test_jinja_message_dict(self, app: "Sanic"):
        sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
        subject = "testing"
        to = "to@example.com"
        person = {"name": "Andrej"}
    
        msg = Message(subject=subject, recipients=[to], template_params=person)
        fm = Mail(app)
    
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg, template_name="email_dict.html")
    
            assert len(outbox) == 1
            mail = outbox[0]
            assert mail["To"] == to
            assert mail["From"] == sender
            assert mail["Subject"] == subject
        assert msg.subtype == "html"
        assert msg.template_body == ("\n   Andrej\n")
    
    
    async def test_send_msg(self, app: "Sanic"):
        msg = Message(subject="testing", recipients=["to@example.com"], body="html test")
    
        sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
        fm = Mail(app)
        fm.config.SUPPRESS_SEND = 1
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg)
    
            assert len(outbox) == 1
            assert outbox[0]["subject"] == "testing"
            assert outbox[0]["from"] == sender
            assert outbox[0]["To"] == "to@example.com"
    
    
    async def test_send_msg_with_subtype(self, app: "Sanic"):
        msg = Message(
            subject="testing",
            recipients=["to@example.com"],
            body="<p html test </p>",
            subtype="html",
        )
    
        sender = f"{app.config['MAIL_FROM_NAME']} <{app.config['MAIL_FROM']}>"
        fm = Mail(app)
        fm.config.SUPPRESS_SEND = 1
        with fm.record_messages() as outbox:
            await fm.send_message(message=msg)
    
            assert len(outbox) == 1
            assert outbox[0]["subject"] == "testing"
            assert outbox[0]["from"] == sender
            assert outbox[0]["To"] == "to@example.com"
        assert msg.body == "<p html test </p>"
        assert msg.subtype == "html"
    
    
    async def test_jinja_message_with_html(self, app: "Sanic"):
        persons = [
            {"name": "Andrej"},
        ]
    
        msg = Message(
            subject="testing",
            recipients=["to@example.com"],
            template_body=persons,
            html="test html",
        )
        fm = Mail(app)
    
        with pytest.raises(ValueError):
            await fm.send_message(message=msg, template_name="email.html")
    
        #assert msg.template_body == ("\n    \n    \n        Andrej\n    \n\n")
    
        assert not msg.body
