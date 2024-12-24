import boto3
import json
import os

def lambda_handler(event, context):
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')

    if not usuario_id or not cuenta_id:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Faltan usuario_id o cuenta_id.'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE_CUENTA'))

    try:
        response = table.get_item(
            Key={
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': f'La cuenta con ID {cuenta_id} para el usuario {usuario_id} no existe.'
            }

        return {
            'statusCode': 200,
            'body': response['Item']
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al buscar la cuenta: {str(e)}'
        }
