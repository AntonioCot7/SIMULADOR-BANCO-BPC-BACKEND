const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();  // Usar DocumentClient para operaciones sencillas

module.exports.lambda_handler = async (event) => {
    try {
        // Verifica si event.body es una cadena
        let data;
        if (typeof event.body === 'string') {
            data = JSON.parse(event.body);  // Solo parsear si es una cadena JSON
        } else {
            data = event.body;  // Si ya es un objeto, usalo tal cual
        }

        const usuario_id = data.usuario_id;
        const ticket_id = data.ticket_id;
        
        // Obtener la solicitud por usuario_id y ticket_id
        const params = {
            TableName: process.env.SOPORTE_TABLE,  // Usar la variable de entorno para la tabla
            Key: {
                usuario_id: usuario_id,
                ticket_id: ticket_id
            }
        };
        
        const response = await dynamodb.get(params).promise();  // Hacer la llamada a DynamoDB
        
        if (response.Item) {
            return {
                statusCode: 200,
                body: response.Item  // Devolver el objeto directamente
            };
        } else {
            return {
                statusCode: 404,
                body: { message: 'Solicitud no encontrada' }  // Devolver el objeto de error como JSON
            };
        }
    } catch (e) {
        console.error(`Error: ${e.message}`);
        return {
            statusCode: 500,
            body: { message: `Error interno del servidor: ${e.message}` }  // Devolver el objeto de error como JSON
        };
    }
};
