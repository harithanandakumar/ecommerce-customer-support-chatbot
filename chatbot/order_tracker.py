import json
from typing import Dict, Optional, List

class OrderTracker:
    """Track and manage customer orders."""
    
    def __init__(self, orders_file='data/sample_orders.json'):
        with open(orders_file, 'r') as f:
            self.orders = json.load(f)
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Retrieve order by ID."""
        for order in self.orders['orders']:
            if order['order_id'].upper() == order_id.upper():
                return order
        return None
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel order if eligible."""
        for order in self.orders['orders']:
            if order['order_id'].upper() == order_id.upper():
                if order['status'] in ['pending', 'processing']:
                    order['status'] = 'cancelled'
                    return True
        return False
    
    def list_user_orders(self, customer_id: str) -> List:
        """List all orders for a customer."""
        return [o for o in self.orders['orders'] if o['customer_id'] == customer_id]
