from chalice import Chalice

app = Chalice(app_name='workshop-intro')

@app.lambda_function()
def hello_world(event, context):
    return {'hello': 'world'}


@app.lambda_function()
def hello_name(event, context):
    name = event['name']
    return {'hello': name}