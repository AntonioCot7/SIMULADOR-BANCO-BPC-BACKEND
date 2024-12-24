import boto3
from boto3.dynamodb.conditions import Key
import os

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('USUARIOS_TABLE'))

    usuario_id = event.get('usuario_id')
    try:
        if usuario_id:
            response = table.query(
                KeyConditionExpression=Key('usuario_id').eq(usuario_id)
            )
            items = response.get('Items', [])
        else:
            response = table.scan()
            items = response.get('Items', [])

            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))

        return {
            'statusCode': 200,
            'body': items if items else "No hay usuarios registrados."
        }

    except Exception as e:
        print(f"Error al listar usuarios: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error interno del servidor: {str(e)}"
        }
