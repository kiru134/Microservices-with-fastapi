from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
from redis_om import get_redis_connection,HashModel
app = FastAPI()


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

class Product(HashModel):
  name: str
  price: float
  quantity: int
  class Meta:
    database = redis

@app.post('/product')
def create(product:Product):
    return product.save()

@app.get('/product/{pk}')
def get(pk:str):
   return Product.get(pk)

@app.get('/products')
def allproducts():
#    return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
   product=Product.get(pk)
   return {
      'id':product.pk,
      'name':product.name,
      'price':product.price,
      'quantity':product.quantity
   }

@app.delete('/product/{pk}')
def deleteitem(pk:str):
   return Product.delete(pk)
   