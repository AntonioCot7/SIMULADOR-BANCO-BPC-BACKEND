const AWS = require('aws-sdk');

// Conexión con DynamoDB
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.SOLICITUD_PRESTAMO_TABLE;

exports.lambdaHandler = async (event) => {
  try {
    // Parsear el cuerpo de la solicitud
    if (!event.body) {
      return {
        statusCode: 400,
        body: {
          error: 'Solicitud inválida',
          details: 'El cuerpo de la solicitud no está presente',
        },
      };
    }

    const data = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    const { usuario_id } = data;

    if (!usuario_id) {
      return {
        statusCode: 400,
        body: {
          error: 'Solicitud inválida',
          details: 'El campo usuario_id es obligatorio',
        },
      };
    }

    // Consulta a DynamoDB para obtener solicitudes por usuario_id
    const params = {
      TableName: TABLE_NAME,
      KeyConditionExpression: 'usuario_id = :usuario_id',
      ExpressionAttributeValues: {
        ':usuario_id': usuario_id,
      },
    };

    const response = await dynamodb.query(params).promise();

    // Convertir el resultado a un formato JSON serializable
    const items = response.Items || [];

    return {
      statusCode: 200,
      body: {
        items, // Los resultados ya están en formato adecuado para la respuesta
      },
    };
  } catch (error) {
    console.error('Error al listar las solicitudes de préstamo:', error);
    return {
      statusCode: 500,
      body: {
        error: 'Error al listar las solicitudes de préstamo',
        details: error.message,
      },
    };
  }
};
