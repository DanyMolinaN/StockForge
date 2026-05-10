const path = require('path');
const express = require('express');
const cors = require('cors');
const productosRouter = require('./routes/productos');
const { errorHandler } = require('./middlewares/errorHandler');

const app = express();
const port = process.env.PORT || 3000;
const frontendPath = path.join(__dirname, '..', 'frontend');

app.use(cors());
app.use(express.json());
app.use(express.static(frontendPath));

app.use('/productos', productosRouter);

// Dejar la ruta raíz para servir el frontend en una sola aplicación.
app.get('*', (req, res) => {
  res.sendFile(path.join(frontendPath, 'index.html'));
});

app.use(errorHandler);

app.listen(port, () => {
  console.log(`Servidor iniciado en http://localhost:${port}`);
});
