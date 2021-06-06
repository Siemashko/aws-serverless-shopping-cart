import json
import jsonpickle
import os

from aws_lambda_powertools import Logger, Tracer
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("aws-serverless-productdatabase")


HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN"),
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

def change_list_from_decimal(l):
    for i, e in enumerate(l):
        if isinstance(e, Decimal):
            l[i] = change_num_from_decimal(e)
        if isinstance(e, dict):
            l[i] = change_dict_from_decimal(e)
        if isinstance(e, list):
            l[i] = change_list_from_decimal(e)
    return l

def change_num_from_decimal(val):
    if val % 1 == 0:
        val = int(val)
    else:
        val = float(val)
    return val

def change_dict_from_decimal(dictionary):
    for k in dictionary.keys():
        e = dictionary[k]
        if isinstance(e, Decimal):
            dictionary[k] = change_num_from_decimal(e)
        if isinstance(e, dict):
            dictionary[k] = change_dict_from_decimal(e)
        if isinstance(e, list):
            dictionary[k] = change_list_from_decimal(e)
    return dictionary


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    Return list of all products.
    """

    serialized = jsonpickle.encode(event)
    logger.debug(json.dumps(json.loads(serialized), indent=2))
    if 'queryStringParameters' not in event or event['queryStringParameters'] is None or len(event['queryStringParameters']) == 0:
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"products": [change_dict_from_decimal(e) for e in table.scan()["Items"]]})
        }
    else:
        categories = event['queryStringParameters']['c'].split(",") if 'c' in event['queryStringParameters'] else None
        price_low = event['queryStringParameters']['pl'] if 'pl' in event['queryStringParameters'] else None
        price_high = event['queryStringParameters']['ph'] if 'ph' in event['queryStringParameters'] else None
    logger.debug("Fetching product list")
    filter_expr = None
    if categories is not None and len(categories) > 0:
        filter_expr = Attr("category").is_in(categories)

    if price_low is not None:
        filter_expr = filter_expr & Attr("price").gte(int(price_low)) if filter_expr is not None else Attr("price").gte(int(price_low))

    if price_high is not None:
        filter_expr = filter_expr & Attr("price").lte(int(price_high)) if filter_expr is not None else Attr("price").lte(int(price_high))

    logger.debug(f"categories: {categories}, price low: {price_low}, price high: {price_high}, filter_expr: {filter_expr}")

    scan_kwargs = {
        "FilterExpression": filter_expr
    }

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"products": [change_dict_from_decimal(e) for e in table.scan(**scan_kwargs)["Items"]]})
    }
