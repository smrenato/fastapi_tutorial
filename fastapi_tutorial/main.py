from fastapi import FastAPI

app = FastAPI()


@app.get('/test/{item_id}')
def items(items_id: int):
    items_list = ['coca_cola', 'refirgerante', 'coco', 'sabonete']
    return {'item chosed': items_list[items_id]}
