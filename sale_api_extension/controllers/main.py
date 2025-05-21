from odoo import http
from odoo.http import request
import json

API_TOKEN = "MI_TOKEN_SECRETO"  # Puedes mover esto a parámetros del sistema si deseas

class SaleOrderAPIController(http.Controller):

    @http.route('/api/sale_order/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        try:
            # Leer token del header
            token = request.httprequest.headers.get('X-API-Token')
            if token != API_TOKEN:
                return {"error": "Token inválido o faltante"}

            data = request.jsonrequest

            partner_id = data.get('partner_id')
            order_lines_data = data.get('order_lines', [])

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
