import json

from fizz_buzz import FizzBuzz


def generate(event, context):
    """FizzBuzz generate Lambda function
    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API
        context LambdaContext -- Lambda Context runtime methods and attributes
    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """
    try:
        number = 0

        if 'queryStringParameters' in event:
            number = int(event['queryStringParameters']['number'])

        body = json.dumps({
            'value': FizzBuzz.generate(number)
        })

        print("Application execute with params:" + str(number))
        return __create_response(200, body)
    except Exception as err:
        err_msg = 'Application error occurred:' + str(err.args)
        print(err_msg)
        body = json.dumps({
            'message': err_msg
        })
        return __create_response(500, body)


def iterate(event, context):
    """FizzBuzz iterate Lambda function
    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API
        context LambdaContext -- Lambda Context runtime methods and attributes
    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """
    try:
        params = json.loads(event['body'])
        count = 0

        if 'count' in params:
            count = int(params['count'])

        body = json.dumps({
            'values': FizzBuzz.iterate(count)
        })

        print("Application execute with params:" + str(params))
        return __create_response(200, body)
    except Exception as err:
        err_msg = 'Application error occurred:' + str(err.args)
        print(err_msg)
        body = json.dumps({
            'message': err_msg
        })
        return __create_response(500, body)


def __create_response(status_code, data):
    return {
        "statusCode": status_code,
        "body": data,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    }
