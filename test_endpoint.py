import unittest
import json
from main import app

class SortProductsEndpointTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Debería de devolver un 200 si el orden es el correcto
    def test_sort_products(self):
        payload = {
            "salesWeight": 0.5,
            "stockWeight": 0.5,
            "productSales": [
                {"productId": "1", "sales": 50000},
                {"productId": "2", "sales": 100000},
                {"productId": "3", "sales": 100000},
                {"productId": "4", "sales": 75000}
            ],
            "productStock": [
                {"productId": "1", "stock": 100000},
                {"productId": "2", "stock": 400000},
                {"productId": "3", "stock": 200000},
                {"productId": "4", "stock": 300000}
            ]
        }

        response = self.app.post('/sort-products', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ["2", "4", "3", "1"])

    # Debería de devolver un 400 de error por ir vacío
    def test_empty_payload(self):
        payload = {}
        response = self.app.post('/sort-products', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    # Debería de devolver un 400 si faltan productSales
    def test_missing_product_sales(self):
        payload = {
            "salesWeight": 0.5,
            "stockWeight": 0.5,
            "productStock": [
                {"productId": "1", "stock": 100000}
            ]
        }
        response = self.app.post('/sort-products', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "productSales y productStock son requeridos")

    # Debería de devolver un 400 si faltan productStock
    def test_missing_product_stock(self):
        payload = {
            "salesWeight": 0.5,
            "stockWeight": 0.5,
            "productSales": [
                {"productId": "1", "sales": 50000}
            ]
        }
        response = self.app.post('/sort-products', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "productSales y productStock son requeridos")

    # Debería de devolver un 400 si no hay productos comunes
    def test_no_common_products(self):
        payload = {
            "salesWeight": 0.5,
            "stockWeight": 0.5,
            "productSales": [
                {"productId": "1", "sales": 50000}
            ],
            "productStock": [
                {"productId": "2", "stock": 100000}
            ]
        }
        response = self.app.post('/sort-products', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "No hay productos comunes en productSales y productStock")

if __name__ == '__main__':
    unittest.main()
