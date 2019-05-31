from flask import Flask, request, render_template
from flask_restful import Api
from flask_restful import Resource
from resources.user import Index, Detail, QRcode, Prize, codeDetail, monthCode
from db import dbInit


app = Flask(__name__)
api = Api(app)

api.add_resource(Index, "/")
api.add_resource(Detail, "/Detail")
api.add_resource(QRcode, "/QRcode")
api.add_resource(Prize, "/prizenum")
api.add_resource(monthCode, "/monthCode")
api.add_resource(codeDetail, "/codeDetail")


if __name__ == "__main__":
    dbInit()
    app.run()
