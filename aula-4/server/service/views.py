import json
from flask import Blueprint, jsonify

from service.db import DB
from service.config import DB_NAME

api = Blueprint("api", __name__)


@api.route("/accounts", methods=["GET"])
def list_accounts():
    database = DB(DB_NAME)
    accounts = database.list_accounts()
    return jsonify(accounts)
