# app/backend/api/pos_routes.py

from flask import Blueprint, request, jsonify
from app.backend.services.pos_service import POSService

def create_pos_blueprint(pos_service: POSService) -> Blueprint:
    """
    Fábrica del Blueprint. Recibe el servicio inyectado para garantizar
    la Inversión de Dependencias (Desacoplamiento).
    """
    # Prefijo unificado para todas las rutas de este módulo
    pos_bp = Blueprint("pos_api", __name__, url_prefix="/api/pos")

    @pos_bp.route("/search", methods=["GET"])
    def search():
        query = request.args.get("q", "")
        if not query:
            return jsonify([]), 200
            
        products = pos_service.search_products(query)
        
        # Mapeo de la Entidad de Dominio a un DTO (Diccionario JSON)
        results = [
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "price": p.price,
                "stock": p.stock,
                "category": p.category
            }
            for p in products
        ]
        return jsonify(results), 200

    @pos_bp.route("/checkout", methods=["POST"])
    def checkout():
        payload = request.get_json()
        
        # Validaciones de la capa de entrega (HTTP)
        if not payload or "items" not in payload or not isinstance(payload["items"], list):
            return jsonify({"error": "Payload inválido o carrito vacío"}), 400
            
        try:
            # 1. Limpiamos cualquier estado residual en memoria del servicio
            pos_service.clear_cart()
            
            # 2. Reconstruimos el carrito desde el JSON recibido de Node.js/Frontend
            for item in payload["items"]:
                pos_service.add_to_cart(item["producto_id"], item["cantidad"])
                
            # 3. Extraemos metadatos y delegamos la regla de negocio
            metodo_pago = payload.get("metodo_pago", "Efectivo")
            usuario_id = payload.get("usuario_id", 1)
            
            venta = pos_service.confirm_sale(usuario_id=usuario_id, metodo_pago=metodo_pago)
            
            # 4. Retornamos la respuesta estandarizada
            return jsonify({
                "success": True,
                "venta": {
                    "numero_venta": venta.numero_venta,
                    "total": venta.total,
                    "fecha": venta.fecha,
                    "metodo_pago": venta.metodo_pago
                }
            }), 201
            
        except ValueError as e:
            # Capturamos excepciones de negocio (ej. stock insuficiente lanzado por POSService)
            pos_service.clear_cart() 
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            # Error genérico para no exponer trazas de base de datos al cliente
            pos_service.clear_cart()
            return jsonify({"error": "Error interno procesando la transacción"}), 500

    return pos_bp