import boto3
import json
import os
from decimal import Decimal

def convert_decimals(obj):
    """
    Recursivamente convierte cualquier tipo Decimal en un tipo numérico que sea serializable por JSON.
    """
    if isinstance(obj, Decimal):
        return float(obj)  # Convertir Decimal a float
    elif isinstance(obj, dict):
        return {key: convert_decimals(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    else:
        return obj

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = event['body']
    cuenta_origen = data['cuenta_origen']
    transaccion_id = data['transaccion_id']
    
    transaccion_table = dynamodb.Table(os.environ['TRANSACTION_TABLE'])
    
    try:
        response = transaccion_table.get_item(
            Key={
                'cuenta_origen': cuenta_origen,
                'transaccion_id': transaccion_id
            }
        )
        
        if 'Item' in response:
            
            item = response['Item']
            item = convert_decimals(item)
            
            return {
                'statusCode': 200,
                'body': response['Item']
            }
        else:
            return {
                'statusCode': 404,
                'body': {'error': 'Transacción no encontrada'}
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': f'Error al obtener la transacción: {str(e)}'}
        }
        
