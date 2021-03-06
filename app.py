from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort
from resources.user import Index, Download, Modelbin, Detail, QRcode, Prize, codeDetail, monthCode, ItemDetail, Tranditionalcode, Manual
from db import dbInit
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
# api.decorators=[cors.crossdomain(origin='*')]

api.add_resource(Index, "/")
api.add_resource(Download, "/Download")
api.add_resource(Modelbin, "/model.weights.bin")
api.add_resource(Tranditionalcode, "/Tranditionalcode")
api.add_resource(Manual, "/manual")
api.add_resource(Detail, "/Detail")
api.add_resource(QRcode, "/QRcode")
api.add_resource(Prize, "/prizenum")
api.add_resource(monthCode, "/monthCode")
api.add_resource(codeDetail, "/codeDetail")
api.add_resource(ItemDetail, "/ItemDetail")


if __name__ == "__main__":
    dbInit()
    app.run(port=8081)
