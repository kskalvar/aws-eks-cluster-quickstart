from flask import Flask
import os
import socket
import fcntl
import struct

app = Flask(__name__)
host = socket.gethostname()

@app.route('/')
def hello():
    Addresses = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
    return '\nMy Address is %s\n\n' % (Addresses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
