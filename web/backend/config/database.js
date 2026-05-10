// Archivo preparado para futura integración con MySQL o PostgreSQL.
// En esta fase el servicio utiliza almacenamiento en memoria.

const dbConfig = {
  client: 'postgresql',
  connection: {
    host: 'localhost',
    port: 5432,
    user: 'tu_usuario',
    password: 'tu_contraseña',
    database: 'inventario'
  }
};

const connect = async () => {
  // En el futuro aquí se puede inicializar la conexión real a la base de datos.
  return Promise.resolve();
};

module.exports = {
  dbConfig,
  connect
};
