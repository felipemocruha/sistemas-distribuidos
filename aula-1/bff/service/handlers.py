from uuid import uuid4
from flask import Blueprint, request, jsonify

from service.core import (
    CreateTransactionRequest,
    TransactionStatus,
)
from service.pubsub import transaction_client
from service.cache import cache
from service.failures import inject_failures
#from service.metrics import instrument_handler


api = Blueprint(__name__)


@api.route("/transactions", methods=["POST"])
# @instrument_handler
@inject_failures(0.1)
def register_transaction():
    payload = request.get_json()
    txn = CreateTransactionRequest(**payload)

    payload["transaction_id"] = str(uuid4())
    transaction_client.create(txn)
    cache.add_transaction(payload)

    return jsonify({"transaction_id": payload["transaction_id"]}), 201


@api.route("/transactions/<id>/status", methods=["PATCH"])
# @instrument_handler
@inject_failures(0.4)
def update_transaction_status():
    txn_id = request.args.get("id")
    payload = request.get_json()
    status = payload.get("status")

    if not hasattr(TransactionStatus, status):
        return jsonify({'error': f'"{status}" is not a valid status value.'})

    cache.update_transaction_status(txn_id, status)
    return "", 204


@api.route("/transactions", methods=["GET"])
# @instrument_handler
@inject_failures(0.4)
def list_recent_transactions():
    transactions = cache.list_transactions()
    return jsonify(transactions)
