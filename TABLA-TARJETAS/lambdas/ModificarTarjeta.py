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
    tarjeta_datos = body.get('tarjeta_datos', {})

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

    update_expression = "set "
    expression_attribute_values = {}
    for key, value in tarjeta_datos.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value
    update_expression = update_expression.rstrip(", ")

    tarjetas_table.update_item(
        Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': f'Tarjeta {tarjeta_id} modificada exitosamente'
    }
