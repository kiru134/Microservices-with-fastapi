import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
from redis_om import get_redis_connection,HashModel
app = FastAPI()
import requests
from fastapi.background import BackgroundTasks

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:3002',
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

redis = get_redis_connection(
 host = 'redis-17922.c305.ap-south-1-1.ec2.cloud.redislabs.com',
 port= 17922,
 password = "NmXiC0Y6afd66vCf2Wv0hjj48ny3lhiW",
decode_responses=True
)

class ProductOrder(HashModel):
    product_id:str
    quantity:int
    class Meta:
        database=redis

class Order(HashModel):
    product_id:str
    price:float
    fee:float
    total:float
    quantity:int
    status:str
    class Meta:
        database = redis


@app.post('/orders')
def create(productorder:ProductOrder,background_tasks:BackgroundTasks):
    req =  requests.get(f'http://localhost:8000/product/{productorder.product_id}')
    product= req.json()
    fee = product['price']*0.2

    order=Order(
        product_id=productorder.product_id,
        price = product['price'],
        fee=fee,
        total=product['price']+fee,
        quantity=productorder.quantity,
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_complete(order))
    return order


@app.get('/orders/{pk}')
def get(pk:str):
   return format(pk) 


@app.get('/orders')
def get_all_orders():
    return [format(pk) for pk in Order.all_pks()] 
def format(pk: str):
  order = Order.get(pk)
  return {
    'id': order.pk,
    'product_id': order.product_id,
    'fee': order.fee,
    'total': order.total,
    'quantity': order.quantity,
    'status': order.status
  }

def order_complete(order:Order):
    time.sleep(5)
    order.status='completed'
    order.save()
    # pushing the ordercompleted status to redis stream
    redis.xadd(name="order-completed",fields=order.dict())

