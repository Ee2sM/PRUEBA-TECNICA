from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

VALID_TOKENS = "api_user@example.com"

class SaleOrderAPIController(http.Controller):

    @http.route('/api/sale_order/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        try:
            # Validar token Bearer
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return {"error": "Encabezado Authorization con Bearer token requerido"}

            token = auth_header.split("Bearer ")[-1]
            if token not in VALID_TOKENS:
                return {"error": "Token inválido"}

            data = kwargs  # <- aquí usamos directamente los kwargs

            partner_id = data.get('partner_id')
            order_lines_data = data.get('order_lines', [])

            _logger.info("*********************PARTNER ID********************")
            _logger.info(partner_id)
            _logger.info("*********************ORDER LINES DATA**************")
            _logger.info(order_lines_data)
            if not partner_id or not order_lines_data:
                return {"error": "Faltan datos obligatorios: partner_id y order_lines"}

            order_lines = []
            for line in order_lines_data:
                product_id = line.get('product_id')
                quantity = line.get('quantity', 1)
                price_unit = line.get('price_unit', 0.0)

                if not product_id:
                    return {"error": "Cada línea debe tener product_id"}

                order_lines.append((0, 0, {
                    'product_id': product_id,
                    'product_uom_qty': quantity,
                    'price_unit': price_unit,
                }))

            sale_order = request.env['sale.order'].sudo().create({
                'partner_id': partner_id,
                'order_line': order_lines,
            })

            return {
                "success": True,
                "sale_order_id": sale_order.id,
                "name": sale_order.name,
            }

        except Exception as e:
            return {"error": str(e)}
