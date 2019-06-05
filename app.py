from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort
from resources.user import Index, Detail, QRcode, Prize, codeDetail, monthCode, ItemDetail, Tranditionalcode
from db import dbInit
# from flask_cors import CORS
from flask_restful.utils import cors

app = Flask(__name__)
# cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
api.decorators=[cors.crossdomain(origin='*')]

api.add_resource(Index, "/")
api.add_resource(Tranditionalcode, "/Tranditionalcode")
api.add_resource(Detail, "/Detail")
api.add_resource(QRcode, "/QRcode")
api.add_resource(Prize, "/prizenum")
api.add_resource(monthCode, "/monthCode")
api.add_resource(codeDetail, "/codeDetail")
api.add_resource(ItemDetail, "/ItemDetail")


if __name__ == "__main__":
    dbInit()
    app.run()
