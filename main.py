from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List


class RootResponse(BaseModel):
    message: str


class ListEndpointItem(BaseModel):
    path: str
    name: str


app = FastAPI(title="FastAPI Advanced Testing Tutorial", 
              description="📝 This repo demonstrates some of the advanced topics on how to implement testing",
              contact={"url": "https://github.com/mehmetcanfarsak", "Name": "Mehmet Can Farsak"},
              )


@app.get("/", response_model=RootResponse)
async def root():
    return {"message": "Hello World"}


@app.get('/list-endpoints', response_model=List[ListEndpointItem])
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list
