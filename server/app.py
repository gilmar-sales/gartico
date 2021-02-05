from flask import Flask

app = Flask(__name__)

#Secret Key
app.secret_key = "ferias"