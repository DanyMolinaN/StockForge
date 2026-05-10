const validateProductInput = (req, res, next) => {
  const { name, sku, price, stock } = req.body;
  const errors = {};

  if (!name || !name.toString().trim()) {
    errors.name = 'El nombre del producto es obligatorio.';
  }

  if (!sku || !sku.toString().trim()) {
    errors.sku = 'El SKU es obligatorio y no permite espacios vacíos.';
  } else if (/\s/.test(sku)) {
    errors.sku = 'El SKU no puede contener espacios.';
  }

  if (price === undefined || price === null || price.toString().trim() === '') {
    errors.price = 'El precio es obligatorio.';
  } else {
    const priceValue = Number(price);
    if (Number.isNaN(priceValue) || priceValue <= 0) {
      errors.price = 'El precio debe ser un número mayor a cero.';
    }
  }

  if (stock === undefined || stock === null || stock.toString().trim() === '') {
    errors.stock = 'El stock inicial es obligatorio.';
  } else {
    const stockValue = Number(stock);
    if (!Number.isInteger(stockValue) || stockValue < 0) {
      errors.stock = 'El stock debe ser un número entero positivo.';
    }
  }

  if (Object.keys(errors).length > 0) {
    return res.status(400).json({
      success: false,
      message: 'Validación de producto fallida.',
      errors
    });
  }

  req.body = {
    name: name.toString().trim(),
    sku: sku.toString().trim(),
    price: Number(price),
    stock: Number(stock)
  };

  next();
};

module.exports = {
  validateProductInput
};
