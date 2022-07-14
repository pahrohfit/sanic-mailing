"""
# ✉️ Sanic-Mailing

Sanic-Mailing adds SMTP mail sending to your Sanic applications

Sanic_Mail is dead now. This is the time to migrate a fully asynchronous 
based mailer library to send emails while using a Sanic based application. 
Now Sanic 2.0 supports the asynchronous view function then who is stopping you to use Sanic-Mailing ?

The key features are:

-  Most of the Apis are very familiar with `Sanic-Mail` module.
-  sending emails with either with Sanic or using asyncio module 
-  sending files either from form-data or files from server
-  Using Jinja2 HTML Templates
-  email utils (utility allows you to check temporary email addresses, you can block any email or domain)
-  email utils has two available classes ```DefaultChecker``` and  ```WhoIsXmlApi```
-  Unittests using Mail

More information on [Getting-Started](https://marktennyson.github.io/sanic-mailing/getting-started)

# 🔗 Important Links 

#### ❤️ [Github](https://github.com/marktennyson/sanic-mailing)    
#### 📄 [Documentation](https://marktennyson.github.io/sanic-mailing)    
#### 🐍 [PYPI](https://pypi.org/project/sanic-mailing)    

# 🔨 Installation ###

```bash
 pip install sanic-mailing
```
or install from source code
```bash
git clone https://github.com/marktennyson/sanic-mailing.git && cd sanic-mailing
python -m pip install .
```

# 🦮 Guide


```python

from sanic import Sanic, json
from sanic_mailing import Mail, Message


app = Sanic(__name__)

app.config['MAIL_USERNAME'] = "YourUserName"
app.config['MAIL_PASSWORD'] = "strong_password"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "your mail server"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['USE_CREDENTIALS'] = True
app.config['VALIDATE_CERTS'] = True
app.config['MAIL_DEFAULT_SENDER'] = "youremailid@doaminname.com"

mail = Mail(app)

html = "<p>Thanks for using Sanic-Mailing</p> "

@app.post("/email")
async def simple_send():

    message = Message(
        subject="Sanic-Mailing module",
        recipients=["recipients@email-domain.com"],  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    await mail.send_message(message)
    return json(status_code=200, content={"message": "email has been sent"})     
```

# 🪜 List of Examples

For more examples of using sanic-mailing please check [example](https://marktennyson.github.io/sanic-mailing/example/) section

# 📝 LICENSE

[MIT](LICENSE)
"""


from . import utils
from .config import ConnectionConfig
from .mail import Mail
from .schemas import Message as Message
from .schemas import MultipartSubtypeEnum as MultipartSubtypeEnum


__author__ = "aniketsarkar@yahoo.com"


__all__ = ["Mail", "ConnectionConfig", "Message", "utils", "MultipartSubtypeEnum"]
