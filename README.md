https://chalice-workshop.readthedocs.io/en/latest/media-query/00-intro-chalice.html

## Part 0: Introduction to AWS Lambda and Chalice¶
This section will provide an introduction on how to use AWS Chalice and provide instructions on how to go about building your very first Chalice application running on AWS Lambda. Steps include:

- Create a virtualenv and install Chalice
- Create a new Chalice application
- Hello world Lambda function
- Lambda function using event parameter
- Delete the Chalice application

## Create a virtualenv and install Chalice¶
To start using Chalice, you will need a new virtualenv with Chalice installed.

### Instructions
Make sure you have Python 3 installed. See the env-setup page for instructions on how to install Python.

Create a new virtualenv called chalice-env by running the following command:

```python
python3 -m venv /tmp/chalice-env
```

Activate your newly created virtualenv:
```python
source /tmp/chalice-env/bin/activate
```

Install chalice using pip:
```python
pip install chalice
```

### Verification
To check that chalice was installed, run:

```python
chalice --version

chalice 1.6.0, python 3.7.3, darwin 15.6.0

mine:
chalice 1.15.1, python 3.8.10, linux 5.4.0-52-generic
```

The version of chalice must be version 1.6.0 or higher and the version of Python should be 3.7.

## Create a new Chalice application
With chalice now installed, it is time to create your first Chalice application.

### Instructions
Run the chalice new-project command to create a project called workshop-intro:
```python
chalice new-project workshop-intro
```
### Verification
A new workshop-intro directory should have been created on your behalf. Inside of the workshop-intro directory, you should have two files: an app.py file and a requirements.txt file:

```python
ls workshop-intro

app.py           requirements.txt

mine
drwxr-xr-x  3 root root 4096 Jul 13 20:36 ./
drwxr-xr-x 22 root root 4096 Jul 13 20:36 ../
drwxr-xr-x  2 root root 4096 Jul 13 20:36 .chalice/
-rw-r--r--  1 root root   37 Jul 13 20:36 .gitignore
-rw-r--r--  1 root root  739 Jul 13 20:36 app.py
-rw-r--r--  1 root root    0 Jul 13 20:36 requirements.txt
```

## Hello world Lambda function
Let’s create our first Lambda function and deploy it using Chalice.

### Instructions
1. Change directories to your newly created workshop-intro directory:

```python
cd workshop-intro
```
2. Open the app.py file and delete all lines of code underneath the line: app = Chalice(app_name='workshop-intro'). Your app.py file should only consist of the following lines:

```python
from chalice import Chalice

app = Chalice(app_name='workshop-intro')
```
3. Add a new function hello_world decorated by app.lambda_function() that returns {"hello": "world"}. Your app.py file should now consist of the following lines:

```python
from chalice import Chalice

app = Chalice(app_name='workshop-intro')

@app.lambda_function()
def hello_world(event, context):
    return {'hello': 'world'}
```
4. Run chalice deploy to deploy your Chalice application to AWS Lambda:

```python
chalice deploy

Creating deployment package.
Creating IAM role: workshop-intro-dev
Creating lambda function: workshop-intro-dev-hello_world
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:708090526287:function:workshop-intro-dev-hello_world
```
### Verification
Run the chalice invoke command to invoke your newly deployed hello_world Lambda function:

```python
$ chalice invoke -n hello_world
{"hello": "world"}
```
## Lambda function using event parameter
Lambda functions accept two parameters: an event and a context parameter. The event parameter is used to provide data to the Lambda function. It is typically a dictionary, but may be a list, string, integer, float, or None. The context parameter provides information about the runtime to the Lambda function. This step will create a Lambda function that will use data from event passed to it to affect its return value.

### Instructions
1. Create an additional Lambda function hello_name using the app.lambda_function() decorator. The function should retrieve the value of the name key in the event parameter and return {'hello': name}:

```python
@app.lambda_function()
def hello_name(event, context):
    name = event['name']
    return {'hello': name}
```

Your app.py file should now consist of the following lines:

```python
from chalice import Chalice

app = Chalice(app_name='workshop-intro')

@app.lambda_function()
def hello_world(event, context):
    return {'hello': 'world'}


@app.lambda_function()
def hello_name(event, context):
    name = event['name']
    return {'hello': name}
```
2. Run chalice deploy to deploy your Chalice application with the new Lambda function:

```python
chalice deploy

Creating deployment package.
Updating policy for IAM role: workshop-intro-dev
Updating lambda function: workshop-intro-dev-hello_world
Creating lambda function: workshop-intro-dev-hello_name
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:708090526287:function:workshop-intro-dev-hello_world
  - Lambda ARN: arn:aws:lambda:us-east-1:708090526287:function:workshop-intro-dev-hello_name
```

### Verification
1. Run chalice invoke to invoke the hello_name Lambda function with {"name": "Kyle"} as the event payload:

```python
$ echo '{"name": "Kyle"}' | chalice invoke -n hello_name
{"hello": "Kyle"}
```

2. It is also possible for your Lambda function to encounter runtime errors. Passing in an empty event payload when invoking the hello_name will result in the Lambda Function returning a Traceback:

```python
chalice invoke -n hello_name
Traceback (most recent call last):
  File "/var/task/chalice/app.py", line 901, in __call__
    return self.func(event, context)
  File "/var/task/app.py", line 12, in hello_name
    name = event['name']
KeyError: 'name'
Error: Unhandled exception in Lambda function, details above.
```

## Delete the Chalice application
Now with an understanding of the basics of AWS Lambda and Chalice, let’s clean up this introduction application by deleting it remotely.

### Instructions
1. Run chalice delete to delete the deployed Lambda functions running this application:

```python
$ chalice delete
Deleting function: arn:aws:lambda:us-east-1:708090526287:function:workshop-intro-dev-hello_name
Deleting function: arn:aws:lambda:us-east-1:708090526287:function:workshop-intro-dev-hello_world
Deleting IAM role: workshop-intro-dev```

### Validation
Try running chalice invoke on the previously deployed Lambda functions:

```python
$ chalice invoke -n hello_world
Could not find invokable resource with name: hello_world

$ chalice invoke -n hello_name
Could not find invokable resource with name: hello_name
```

You should no longer be able to invoke both Lambda functions as they have been deleted.
