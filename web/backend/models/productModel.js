const products = [];

class ProductModel {
  static async findAll() {
    return [...products];
  }

  static async findById(id) {
    return products.find(p => p.id === Number(id));
  }

  static async create({ name, sku, price, stock }) {
    const newProduct = {
      id: products.length > 0 ? Math.max(...products.map(p => p.id)) + 1 : 1,
      name: name.trim(),
      sku: sku.trim(),
      price: Number(price),
      stock: Number(stock),
      createdAt: new Date().toISOString()
    };

    products.push(newProduct);
    return newProduct;
  }

  static async update(id, { name, sku, price, stock }) {
    const product = products.find(p => p.id === Number(id));
    
    if (!product) {
      return null;
    }

    product.name = name.trim();
    product.sku = sku.trim();
    product.price = Number(price);
    product.stock = Number(stock);
    product.updatedAt = new Date().toISOString();

    return product;
  }

  static async delete(id) {
    const index = products.findIndex(p => p.id === Number(id));
    
    if (index === -1) {
      return null;
    }

    const deletedProduct = products.splice(index, 1);
    return deletedProduct[0];
  }
}

module.exports = ProductModel;
