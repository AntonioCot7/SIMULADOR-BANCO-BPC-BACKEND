import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = event['body']
    cuenta_origen = data['cuenta_origen']
    transaccion_id = data['transaccion_id']
    
    transaccion_table = dynamodb.Table(os.environ.get('TRANSACTION_TABLE'))
    
    try:
        transaccion_table.delete_item(
            Key={
                'cuenta_origen': cuenta_origen,
                'transaccion_id': transaccion_id
            }
        )
        
        return {
            'statusCode': 200,
            'body': {'message': f'Transacción {transaccion_id} eliminada con éxito'}
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Error al eliminar la transacción: {str(e)}'}
        }