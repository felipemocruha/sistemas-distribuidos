from uuid import uuid4
import logging
from time import time

from flask import Blueprint, request, jsonify
from pydantic.error_wrappers import ValidationError

from service.core import (
    CreateTransactionRequest,
    TransactionStatus,
)
from service.pubsub import transaction_client
from service.cache import cache
from service.failures import inject_failures
from service.config import FAILURE_RATE


api = Blueprint("api", __name__)
logger = logging.getLogger()


@api.route("/transactions", methods=["POST"])
@inject_failures(FAILURE_RATE)
def register_transaction():
    payload = request.get_json() or {}

    try:
        txn = CreateTransactionRequest(
            **payload,
            transaction_id=str(uuid4()),
            event_timestamp=int(time()),
            status=TransactionStatus.pending,
        ).dict()

    except ValidationError:
        return jsonify({"error": "Invalid request payload"}), 400

    try:
        transaction_client.create(txn)
        cache.add_transaction(txn)

    except Exception as err:
       logger.error(f'failed to create transaction: {str(err)}')
       return jsonify({'error': 'Internal Server Error'}), 500

    return jsonify({"transaction_id": txn["transaction_id"]}), 201


@api.route("/transactions/<txn_id>/status", methods=["PATCH"])
@inject_failures(FAILURE_RATE)
def update_transaction_status(txn_id):
    payload = request.get_json() or {}
    status = payload.get("status")

    if not hasattr(TransactionStatus, status):
        return (
            jsonify({"error": f'"{status}" is not a valid status value.'}),
            400,
        )

    cache.update_transaction(txn_id, status)
    return "", 204


@api.route("/transactions", methods=["GET"])
@inject_failures(FAILURE_RATE)
def list_recent_transactions():
    try:
        transactions = cache.list_transactions()
        return jsonify({"transactions": transactions})

    except Exception as err:
       logger.error(f'failed to list transactions: {str(err)}')
       return jsonify({'error': 'Internal Server Error'}), 500
