const AWS = require('aws-sdk');

// Conexión a DynamoDB
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.SOLICITUD_PRESTAMO_TABLE;

exports.lambdaHandler = async (event) => {
  try {
    // Validar el cuerpo de la solicitud
    if (!event.body) {
      return {
        statusCode: 400,
        body: {
          error: 'Solicitud inválida',
          details: 'No se encontró el cuerpo de la solicitud',
        },
      };
    }

    const data = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    const { estado } = data;

    // Validar que el estado esté presente y sea válido
    if (!estado || (estado !== 'aceptado' && estado !== 'rechazado')) {
      return {
        statusCode: 400,
        body: {
          error: 'Solicitud inválida',
          details: 'El estado debe ser "aceptado" o "rechazado"',
        },
      };
    }

    // Escanear solicitudes según el estado
    const params = {
      TableName: TABLE_NAME,
      FilterExpression: '#estado = :estado',
      ExpressionAttributeNames: {
        '#estado': 'estado', // Necesario si "estado" es una palabra reservada
      },
      ExpressionAttributeValues: {
        ':estado': estado,
      },
    };

    const response = await dynamodb.scan(params).promise();
    const solicitudes = response.Items || [];

    // Retornar las solicitudes encontradas
    return {
      statusCode: 200,
      body: {
        message: `Solicitudes con estado ${estado} encontradas`,
        estado,
        solicitudes,
      },
    };
  } catch (error) {
    console.error(`Error: ${error.message}`);
    return {
      statusCode: 500,
      body: {
        error: 'Error interno al procesar la solicitud',
        details: error.message,
      },
    };
  }
};