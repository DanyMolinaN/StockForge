const express = require('express');
const router = express.Router();
const productController = require('../controllers/productController');
const { validateProductInput } = require('../middlewares/validationMiddleware');

router.get('/', productController.getProductos);
router.get('/:id', productController.getProductoById);
router.post('/', validateProductInput, productController.createProducto);
router.put('/:id', validateProductInput, productController.updateProducto);
router.delete('/:id', productController.deleteProducto);

module.exports = router;
