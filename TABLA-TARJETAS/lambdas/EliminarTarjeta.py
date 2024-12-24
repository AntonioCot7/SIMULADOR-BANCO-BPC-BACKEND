import boto3
import json
import os

def lambda_handler(event, context):
    if isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event['body']

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')
    tarjeta_id = body.get('tarjeta_id')

    dynamodb = boto3.resource('dynamodb')
    cuentas_table = dynamodb.Table(os.environ.get('CUENTAS_TABLE'))
    tarjetas_table = dynamodb.Table(os.environ.get('TARJETAS_TABLE'))

    cuenta_response = cuentas_table.get_item(Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id})
    if 'Item' not in cuenta_response:
        return {
            'statusCode': 400,
            'body': 'Error: Cuenta no encontrada para este usuario.'
        }

    tarjeta_response = tarjetas_table.get_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})
    if 'Item' not in tarjeta_response:
        return {
            'statusCode': 404,
            'body': 'Error: Tarjeta no encontrada.'
        }

    tarjetas_table.delete_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})

    return {
        'statusCode': 200,
        'body': f'Tarjeta {tarjeta_id} eliminada exitosamente'
    }
