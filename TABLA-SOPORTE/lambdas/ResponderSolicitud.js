const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

module.exports.lambda_handler = async (event) => {
    try {
        // Verificar si el cuerpo ya es un objeto, si no, realizar el parseo
        const data = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
        const { usuario_id, ticket_id, response: response_text } = data;

        // Obtener el ítem actual de DynamoDB
        const params = {
            TableName: process.env.SOPORTE_TABLE,
            Key: {
                usuario_id: usuario_id,
                ticket_id: ticket_id
            }
        };

        const response = await dynamodb.get(params).promise();

        // Verificar si la solicitud ya fue respondida
        if (response.Item && response.Item.estado === 'respondido') {
            return {
                statusCode: 400,
                body: {
                    message: 'La solicitud ya fue respondida.'
                }
            };
        }

        // Preparar la actualización con la respuesta y la fecha actual
        const fecha_respuesta = new Date().toISOString();
        const updateParams = {
            TableName: process.env.SOPORTE_TABLE,
            Key: {
                usuario_id: usuario_id,
                ticket_id: ticket_id
            },
            UpdateExpression: 'SET #resp = :response_text, estado = :estado, fecha_respuesta = :fecha',
            ExpressionAttributeNames: {
                '#resp': 'response'  // Alias para el atributo 'response'
            },
            ExpressionAttributeValues: {
                ':response_text': response_text,
                ':estado': 'respondido',
                ':fecha': fecha_respuesta
            }
        };

        await dynamodb.update(updateParams).promise();

        // Retornar la respuesta confirmando la actualización
        return {
            statusCode: 200,
            body: {
                usuario_id: usuario_id,
                ticket_id: ticket_id,
                response: response_text,
                estado: 'respondido',
                fecha_respuesta: fecha_respuesta
            }
        };
    } catch (e) {
        console.error(`Error: ${e.message}`);
        return {
            statusCode: 500,
            body: {
                message: `Error interno del servidor: ${e.message}`
            }
        };
    }
};
