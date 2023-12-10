from __future__ import annotations

from enum import Enum

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message":"hello world"}


@app.post("/", description='this is post method ok?')
async def post():
    return {"message": "post request sent"}



@app.put("/{id}", description='this is put')
async def put(id:str):
    return {"post request put with id :": id}


class FoodEnum(str, Enum):
    fruits= "fruits"
    vegetables= "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.fruits:
        return {"foodname is:": food_name}
    elif food_name == FoodEnum.vegetables:
        return {"foodname is veg:": food_name}
    else:
        return {"foodname is dairy:": food_name}


@app.get("/items/{item_id}")
def get_items(item_id:int, q: str | None = None, short:bool = False):
    response = {"message":item_id}
    if q:
        response.update({"QQQ": q})
    if not short:
        response.update({"short":"is false"})
    return response


class Item(BaseModel):
    name: str
    price: float
    description: str | None=None
    tax: float | None=None


@app.post('/items')
def create_item(item:Item):
    item_dict = item.model_dump()
    if item.tax and item.price:
        total = item.price + (item.price * item.tax / 100)
        item_dict.update({'total':total})
    return item_dict



@app.put('/update_items')
def up(item:Item, q : str | None=None, id:int |None=None):
    result = {"item_id":id, **item.model_dump()}

    if q:
        result.update({'q':q})
    return result

@app.get('/items')
def get_items(q: str | None=None):
    dic = {'name':'berkan'}
    if q:
        dic.update({'surname':q })
    return dic

@app.get('/items_query')
# def items_query(q: str | None=Query('sdfd', min_length=2, max_length=10, alias='this is the placeholder')):
def items_query(q: float | None=Query(...,lte=10, gt=2,  alias='this is the placeholder')):
    dic = {'name':'berkan'}
    if q:
        dic.update({'surname':q })
    return dic
