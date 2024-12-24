import boto3
import uuid
from datetime import datetime, timedelta
import os
import json

def lambda_handler(event, context):
    if 'body' in event:
        if isinstance(event['body'], str):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'body': {
                        'message': 'Solicitud inválida. Formato JSON incorrecto.'
                    }
                }
        else:
            body = event['body']
    else:
        body = event

    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return {
            'statusCode': 400,
            'body': {
                'message': 'Faltan los campos requeridos: email y/o password.'
            }
        }

    dynamodb = boto3.resource('dynamodb')
    usuarios_table = dynamodb.Table(os.environ.get('USUARIOS_TABLE'))

    try:
        response = usuarios_table.query(
            IndexName=os.environ.get('GSI_EMAIL'),
            KeyConditionExpression="email = :email_val",
            ExpressionAttributeValues={":email_val": email}
        )
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 403,
                'body': {
                    'message': 'Usuario no existe.'
                }
            }

        user = items[0]

        if password != user.get('password'):
            return {
                'statusCode': 403,
                'body': {
                    'message': 'Contraseña incorrecta.'
                }
            }

        usuario_id = user.get('usuario_id')
        if not usuario_id:
            return {
                'statusCode': 500,
                'body': {
                    'message': 'Error interno: usuario_id no encontrado en el registro.'
                }
            }

        token = str(uuid.uuid4())
        expires = (datetime.now() + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')

        tokens_table = dynamodb.Table(os.environ.get('TOKENS_TABLE'))
        tokens_table.put_item(
            Item={
                'token': token,
                'expires': expires,
                'usuario_id': usuario_id
            }
        )

        return {
            'statusCode': 200,
            'body': {
                'message': 'Inicio de sesión exitoso.',
                'token': token,
                'expires': expires,
                'usuario_id': usuario_id
            }
        }

    except Exception as e:
        print(f"Error en el inicio de sesión: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'message': 'Error interno del servidor.',
                'error': str(e)
            }
        }
