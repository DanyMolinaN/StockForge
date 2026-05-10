const form = document.getElementById('product-form');
const formTitle = document.getElementById('form-title');
const productList = document.getElementById('product-list');
const submissionMessage = document.getElementById('submission-message');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const productIdInput = document.getElementById('product-id');

const fields = {
  name: document.getElementById('name'),
  sku: document.getElementById('sku'),
  price: document.getElementById('price'),
  stock: document.getElementById('stock')
};

const errors = {
  name: document.getElementById('error-name'),
  sku: document.getElementById('error-sku'),
  price: document.getElementById('error-price'),
  stock: document.getElementById('error-stock')
};

const apiUrl = '/productos';

let isEditMode = false;

const clearForm = () => {
  form.reset();
  productIdInput.value = '';
  isEditMode = false;
  formTitle.textContent = 'Registro de Nuevo Producto';
  submitBtn.textContent = 'Guardar producto';
  cancelBtn.style.display = 'none';
  Object.values(errors).forEach((errorElement) => {
    errorElement.textContent = '';
  });
  Object.values(fields).forEach((field) => {
    field.classList.remove('input-error');
  });
  submissionMessage.textContent = '';
};

const renderMessages = (validationErrors) => {
  Object.entries(errors).forEach(([key, element]) => {
    element.textContent = validationErrors[key] || '';
    fields[key].classList.toggle('input-error', Boolean(validationErrors[key]));
  });
};

const renderProducts = (products) => {
  if (!products.length) {
    productList.innerHTML = `
      <tr>
        <td colspan="5" class="empty-state">No hay productos registrados.</td>
      </tr>
    `;
    return;
  }

  productList.innerHTML = products
    .map(
      (product) => `
        <tr>
          <td>${product.name}</td>
          <td>${product.sku}</td>
          <td>$${product.price.toFixed(2)}</td>
          <td>${product.stock}</td>
          <td>
            <div class="action-buttons">
              <button type="button" class="btn btn-edit" data-edit="${product.id}">Editar</button>
              <button type="button" class="btn btn-danger" data-delete="${product.id}">Eliminar</button>
            </div>
          </td>
        </tr>
      `
    )
    .join('');

  // Agregar event listeners para los botones de editar
  document.querySelectorAll('[data-edit]').forEach((btn) => {
    btn.addEventListener('click', () => handleEdit(Number(btn.dataset.edit)));
  });

  // Agregar event listeners para los botones de eliminar
  document.querySelectorAll('[data-delete]').forEach((btn) => {
    btn.addEventListener('click', () => handleDelete(Number(btn.dataset.delete)));
  });
};

const fetchProducts = async () => {
  try {
    const response = await fetch(apiUrl);
    const result = await response.json();

    if (result.success) {
      renderProducts(result.data);
      return;
    }

    console.error('Error al obtener productos', result.message);
  } catch (error) {
    console.error('Error de red al obtener productos', error);
  }
};

const getFormData = () => ({
  name: fields.name.value.trim(),
  sku: fields.sku.value.trim(),
  price: fields.price.value.trim(),
  stock: fields.stock.value.trim()
});

const validateField = (key, value) => {
  const fieldErrors = {};

  if (!value) {
    fieldErrors[key] = {
      name: 'El nombre del producto es obligatorio.',
      sku: 'El SKU es obligatorio y no permite espacios vacíos.',
      price: 'El precio es obligatorio.',
      stock: 'El stock inicial es obligatorio.'
    }[key];
    return fieldErrors;
  }

  if (key === 'sku' && /\s/.test(value)) {
    fieldErrors.sku = 'El SKU no puede contener espacios.';
    return fieldErrors;
  }

  if (key === 'price') {
    const priceValue = Number(value);
    if (Number.isNaN(priceValue) || priceValue <= 0) {
      fieldErrors.price = 'El precio debe ser un número mayor a cero.';
    }
  }

  if (key === 'stock') {
    const stockValue = Number(value);
    if (!Number.isInteger(stockValue) || stockValue < 0) {
      fieldErrors.stock = 'El stock debe ser un número entero positivo.';
    }
  }

  return fieldErrors;
};

const validateAllFields = () => {
  const formData = getFormData();
  const validationErrors = {};

  Object.entries(formData).forEach(([key, value]) => {
    const fieldError = validateField(key, value);
    Object.assign(validationErrors, fieldError);
  });

  renderMessages(validationErrors);
  return Object.keys(validationErrors).length === 0;
};

const handleEdit = async (id) => {
  try {
    const response = await fetch(`${apiUrl}/${id}`);
    const result = await response.json();

    if (!response.ok || !result.data) {
      submissionMessage.textContent = 'No se pudo cargar el producto.';
      submissionMessage.style.color = '#ef4444';
      return;
    }

    const product = result.data;
    fields.name.value = product.name;
    fields.sku.value = product.sku;
    fields.price.value = product.price;
    fields.stock.value = product.stock;
    productIdInput.value = id;

    isEditMode = true;
    formTitle.textContent = 'Editar Producto';
    submitBtn.textContent = 'Actualizar producto';
    cancelBtn.style.display = 'inline-block';

    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (error) {
    submissionMessage.textContent = 'Error al cargar el producto.';
    submissionMessage.style.color = '#ef4444';
    console.error(error);
  }
};

const handleDelete = async (id) => {
  if (!confirm('¿Estás seguro de que deseas eliminar este producto?')) {
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/${id}`, {
      method: 'DELETE'
    });

    const result = await response.json();

    if (!response.ok) {
      submissionMessage.textContent = result.message || 'No se pudo eliminar el producto.';
      submissionMessage.style.color = '#ef4444';
      return;
    }

    submissionMessage.textContent = result.message;
    submissionMessage.style.color = 'var(--success)';
    fetchProducts();

    // Limpiar si estaba en modo edición y borramos ese producto
    if (isEditMode && Number(productIdInput.value) === id) {
      clearForm();
    }
  } catch (error) {
    submissionMessage.textContent = 'Error al eliminar el producto.';
    submissionMessage.style.color = '#ef4444';
    console.error(error);
  }
};

const handleFormSubmit = async (event) => {
  event.preventDefault();
  submissionMessage.textContent = '';

  if (!validateAllFields()) {
    submissionMessage.textContent = '';
    return;
  }

  const payload = {
    name: fields.name.value,
    sku: fields.sku.value,
    price: Number(fields.price.value),
    stock: Number(fields.stock.value)
  };

  const method = isEditMode ? 'PUT' : 'POST';
  const url = isEditMode ? `${apiUrl}/${productIdInput.value}` : apiUrl;
  const statusCode = isEditMode ? 200 : 201;

  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      renderMessages(result.errors || {});
      submissionMessage.textContent = result.message || 'Error al procesar el producto.';
      submissionMessage.style.color = '#ef4444';
      return;
    }

    submissionMessage.textContent = result.message;
    submissionMessage.style.color = 'var(--success)';
    clearForm();
    fetchProducts();
  } catch (error) {
    submissionMessage.textContent = 'Ocurrió un error en la comunicación con el servidor.';
    submissionMessage.style.color = '#ef4444';
    console.error(error);
  }
};

// Event listeners para validación en tiempo real
Object.entries(fields).forEach(([key, input]) => {
  input.addEventListener('input', () => {
    const fieldError = validateField(key, input.value.trim());
    renderMessages(fieldError);
  });
});

form.addEventListener('submit', handleFormSubmit);

cancelBtn.addEventListener('click', () => {
  clearForm();
});

window.addEventListener('load', () => {
  fetchProducts();
});
