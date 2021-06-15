import boto3
import requests
from time import sleep
import json

s3_client = boto3.client('s3')
dynamodb = boto3.resource("dynamodb")
product_table = dynamodb.Table("aws-serverless-productdatabase")
cart_table = dynamodb.Table("aws-serverless-shopping-cart-shoppingcart-service-DynamoDBShoppingCartTable-OPG744JU5FRA")

s = requests.Session()
cookies = None

# Test schedule product from S3 Lambda

def test_schedule_product_from_s3(active=True):
    if active == False:
        return True
    response = s3_client.list_buckets()
    bucket_name = next(filter(lambda x: x['Name'][:20] == 'product-input-bucket', response['Buckets']))['Name']
    s3_client.upload_file('../backend/product-mock-service/product1.json', bucket_name, 'product1.json')
    s3_client.upload_file('../backend/product-mock-service/product2.json', bucket_name, 'product2.json')
    s3_client.upload_file('../backend/product-mock-service/product3.json', bucket_name, 'product3.json')
    sleep(5)
    successful = len(product_table.scan()["Items"]) != 0
    print(f"{'✅' if successful else '❌'} – schedule product from s3")
    return successful


# Test get products

def test_get_products(active=True):
    if active == False:
        return True
    response = s.get('https://cj9jtf0zyf.execute-api.us-east-1.amazonaws.com/Prod/product')
    successful = False
    if response.status_code == 200:
        successful = len(json.loads(response.content.decode('UTF-8'))['products']) == 3
        print(f"{'✅' if successful else '❌'} – get products")
    return successful


# Test get products with filter

def test_get_products_with_filter(active=True):
    if active == False:
        return True
    response = s.get('https://cj9jtf0zyf.execute-api.us-east-1.amazonaws.com/Prod/product?c=apparel')
    successful = False
    if response.status_code == 200:
        successful = len(json.loads(response.content.decode('UTF-8'))['products']) == 1
        print(f"{'✅' if successful else '❌'} – get products with filter")
    return successful


# Test get product by id

def test_get_product_by_id(active=True):
    if active == False:
        return True
    response = s.get('https://cj9jtf0zyf.execute-api.us-east-1.amazonaws.com/Prod/product/e-d105-45a5-9b21-ba61995bc6da')
    successful = False
    if response.status_code == 200:
        successful = 'product' in json.loads(response.content.decode('UTF-8'))
        print(f"{'✅' if successful else '❌'} – get product by id")
    return successful

# Test list cart

def test_list_cart(active=True):
    global cookies
    if active == False:
        return True
    successful = False
    response = s.get(
        'https://6mlrh3slw6.execute-api.us-east-1.amazonaws.com/Prod/cart')
    if response.status_code == 200:
        successful = 'products' in json.loads(response.content.decode('UTF-8'))
        print(f"{'✅' if successful else '❌'} – get cart")
    return successful

# Test add to cart

def test_add_to_cart(active=True):
    if active == False:
        return True
    payload = '{"productId":"e-d105-45a5-9b21-ba61995bc6da","quantity":1}'
    response = s.post(
        'https://6mlrh3slw6.execute-api.us-east-1.amazonaws.com/Prod/cart', data=payload, cookies=s.cookies)
    successful = response.status_code == 200
    print(f"{'✅' if successful else '❌'} – add product to cart")
    return successful
#

def test_update_cart(active=True):
    if active == False:
        return True
    payload = '{"productId":"e-d105-45a5-9b21-ba61995bc6da","quantity":"3"}'
    response = s.put(
        'https://6mlrh3slw6.execute-api.us-east-1.amazonaws.com/Prod/cart/e-d105-45a5-9b21-ba61995bc6da', data=payload, cookies=s.cookies)
    successful = response.status_code == 200
    print(f"{'✅' if successful else '❌'} – update cart")
    return successful


test_schedule_product_from_s3() and\
    test_get_products() and\
    test_get_products_with_filter() and\
    test_get_product_by_id() and\
    test_list_cart() and\
    test_add_to_cart() and\
    test_list_cart() and\
    test_update_cart() and\
    print("Test finished")
