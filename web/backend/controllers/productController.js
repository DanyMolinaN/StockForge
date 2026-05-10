const ProductModel = require('../models/productModel');

const getProductos = async (req, res, next) => {
  try {
    const products = await ProductModel.findAll();
    res.json({
      success: true,
      data: products
    });
  } catch (error) {
    next(error);
  }
};

const getProductoById = async (req, res, next) => {
  try {
    const { id } = req.params;
    const product = await ProductModel.findById(id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Producto no encontrado'
      });
    }

    res.json({
      success: true,
      data: product
    });
  } catch (error) {
    next(error);
  }
};

const createProducto = async (req, res, next) => {
  try {
    const payload = req.body;
    const product = await ProductModel.create(payload);

    res.status(201).json({
      success: true,
      message: 'Producto registrado correctamente',
      data: product
    });
  } catch (error) {
    next(error);
  }
};

const updateProducto = async (req, res, next) => {
  try {
    const { id } = req.params;
    const payload = req.body;

    const product = await ProductModel.update(id, payload);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Producto no encontrado'
      });
    }

    res.json({
      success: true,
      message: 'Producto actualizado correctamente',
      data: product
    });
  } catch (error) {
    next(error);
  }
};

const deleteProducto = async (req, res, next) => {
  try {
    const { id } = req.params;

    const product = await ProductModel.delete(id);

    if (!product) {
      return res.status(404).json({
        success: false,
        message: 'Producto no encontrado'
      });
    }

    res.json({
      success: true,
      message: 'Producto eliminado correctamente',
      data: product
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getProductos,
  getProductoById,
  createProducto,
  updateProducto,
  deleteProducto
};
