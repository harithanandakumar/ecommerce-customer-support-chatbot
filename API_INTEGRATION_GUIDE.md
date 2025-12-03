# API Integration Guide

Comprehensive guide for integrating the e-commerce customer support chatbot with third-party e-commerce platforms and services.

## Table of Contents
1. [Integration Overview](#integration-overview)
2. [Shopify Integration](#shopify-integration)
3. [WooCommerce Integration](#woocommerce-integration)
4. [Magento Integration](#magento-integration)
5. [BigCommerce Integration](#bigcommerce-integration)
6. [Payment Gateway Integration](#payment-gateway-integration)
7. [Shipping Provider Integration](#shipping-provider-integration)
8. [CRM Integration](#crm-integration)
9. [Analytics Integration](#analytics-integration)
10. [Webhook Management](#webhook-management)

## Integration Overview

### Architecture
The chatbot uses a plugin-based architecture for third-party integrations:
```
Chatbot Core
    ↓
[Integration Layer]
    ↓
[Platform Adapters: Shopify, WooCommerce, Magento, BigCommerce]
    ↓
[External Services]
```

### Authentication Methods
- **OAuth 2.0:** For secure platform authentication
- **API Keys:** For service-to-service communication
- **JWT Tokens:** For internal service communication
- **Webhooks:** For event-driven integrations

---

## Shopify Integration

### Setup
1. Create custom Shopify app in Partner Dashboard
2. Configure scopes:
   - `read_orders` - Access order data
   - `read_customers` - Access customer data
   - `read_fulfillments` - Track order status
   - `write_fulfillments` - Update fulfillment

### API Endpoints
```
GET /admin/api/2024-01/orders/{order_id}.json
GET /admin/api/2024-01/orders/{order_id}/fulfillments.json
POST /admin/api/2024-01/orders/{order_id}/fulfillments.json
GET /admin/api/2024-01/customers/{customer_id}.json
```

### Implementation
```python
import shopify

shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)
session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

# Get order
order = shopify.Order.find(order_id)
print(f"Order status: {order.financial_status}")

# Get fulfillments
fulfillments = shopify.Fulfillment.find(order_id)
for fulfillment in fulfillments:
    print(f"Tracking: {fulfillment.tracking_info}")
```

### Webhooks
Register for webhooks:
- `orders/created`
- `orders/updated`
- `fulfillments/create`
- `customers/create`

---

## WooCommerce Integration

### Setup
1. Generate REST API credentials in WooCommerce settings
2. Configure scope: `read_write`
3. Add to chatbot configuration:
```json
{
  "woocommerce": {
    "store_url": "https://mystore.com",
    "consumer_key": "ck_...",
    "consumer_secret": "cs_...",
    "version": "wc/v3"
  }
}
```

### API Endpoints
```
GET /wp-json/wc/v3/orders/{id}
GET /wp-json/wc/v3/orders/{id}/notes
POST /wp-json/wc/v3/orders/{id}/notes
GET /wp-json/wc/v3/customers/{id}
```

### Implementation
```python
from woocommerce import API

wcapi = API(
    url=STORE_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3"
)

# Get order
order = wcapi.get(f"orders/{order_id}").json()
print(f"Order status: {order['status']}")

# Get order notes
notes = wcapi.get(f"orders/{order_id}/notes").json()
for note in notes:
    print(f"Note: {note['note']}")
```

---

## Magento Integration

### Setup
1. Create API integration in Magento Admin
2. Generate access tokens
3. Configure authentication:
```python
magento_config = {
    "store_url": "https://mymagento.com",
    "api_token": "token...",
    "api_version": "V1"
}
```

### API Endpoints
```
GET /rest/V1/orders/{id}
GET /rest/V1/orders
POST /rest/V1/shipment
GET /rest/V1/customers/{id}
```

### Implementation
```python
import requests

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Get order
response = requests.get(
    f"{STORE_URL}/rest/V1/orders/{order_id}",
    headers=headers
)
order = response.json()
print(f"Order status: {order['status']}")
```

---

## BigCommerce Integration

### Setup
1. Create API account in BigCommerce control panel
2. Generate API credentials (Channel ID, Access Token)
3. Configure in chatbot:
```python
bigcommerce_config = {
    "store_hash": "store_hash",
    "access_token": "token...",
    "api_version": "v3"
}
```

### API Endpoints
```
GET /stores/{store_hash}/v3/orders/{order_id}
GET /stores/{store_hash}/v3/orders
GET /stores/{store_hash}/v3/customers/{customer_id}
POST /stores/{store_hash}/v3/orders/{order_id}/messages
```

---

## Payment Gateway Integration

### Stripe Integration
```python
import stripe

stripe.api_key = STRIPE_API_KEY

# Get payment intent
payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
print(f"Status: {payment_intent.status}")

# Create refund
refund = stripe.Refund.create(
    payment_intent=payment_intent_id,
    reason="customer_request"
)
```

### PayPal Integration
```python
from paypalrestsdk import Payment

payment = Payment.find(payment_id)
print(f"Status: {payment.state}")

# Sale refund
sale = payment.sale
refund_result = sale.refund()
```

---

## Shipping Provider Integration

### FedEx
```python
from fedex.services.ship_service import FedexProcessShipmentRequest

# Track shipment
tracking = get_tracking_info(tracking_number, carrier='FEDEX')
print(f"Status: {tracking['status']}")
```

### UPS
```python
from ups_api import TrackingAPI

tracking = TrackingAPI(api_key=UPS_API_KEY)
status = tracking.track(tracking_number)
print(f"Status: {status['tracking_info']['status']}")
```

### DHL
```python
from dhl_api import Track

dhl = Track(username=DHL_USERNAME, password=DHL_PASSWORD)
shipment = dhl.track(tracking_number)
print(f"Status: {shipment.status}")
```

---

## CRM Integration

### Salesforce
```python
from simple_salesforce import Salesforce

sf = Salesforce(
    username=SF_USERNAME,
    password=SF_PASSWORD,
    security_token=SF_TOKEN
)

# Get customer
customer = sf.Account.get_by_custom_id('Order__c', order_id)
print(f"Account: {customer['Name']}")
```

### HubSpot
```python
from hubspot import HubSpot

client = HubSpot(access_token=HUBSPOT_TOKEN)

# Create contact
SimplePublicObjectInput = {...}
api_response = client.crm.contacts.basic_api.create(
    simple_public_object_input=SimplePublicObjectInput
)
```

---

## Analytics Integration

### Google Analytics
```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient

client = BetaAnalyticsDataClient()
request = RunReportRequest(...)
response = client.run_report(request)
```

### Mixpanel
```python
from mixpanel import Mixpanel

mp = Mixpanel(MIXPANEL_TOKEN)
mp.track(user_id, 'Order Lookup', {'order_id': order_id})
```

---

## Webhook Management

### Register Webhook
```python
def register_webhook(event_type, callback_url):
    """Register webhook for specific event."""
    webhook_config = {
        "event": event_type,
        "url": callback_url,
        "auth_token": generate_token()
    }
    save_webhook_config(webhook_config)
    return webhook_config["id"]
```

### Handle Webhook
```python
from flask import request, jsonify

@app.route('/webhooks/order-update', methods=['POST'])
def handle_order_webhook():
    payload = request.json
    
    # Verify webhook signature
    if not verify_webhook_signature(payload):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Process event
    handle_order_update(payload['order'])
    return jsonify({'status': 'success'}), 200
```

### Webhook Security
- Always verify webhook signatures
- Use HTTPS endpoints
- Implement rate limiting
- Store webhook logs for debugging
- Retry failed webhook deliveries

---

## Error Handling

```python
class IntegrationError(Exception):
    """Base integration error."""
    pass

class AuthenticationError(IntegrationError):
    """Authentication failed."""
    pass

class RateLimitError(IntegrationError):
    """API rate limit exceeded."""
    pass

class ValidationError(IntegrationError):
    """Data validation failed."""
    pass
```

---

## Testing

```python
def test_shopify_integration():
    """Test Shopify API connection."""
    try:
        order = get_order('test_order_id')
        assert order is not None
        assert 'id' in order
        print("✓ Shopify integration working")
    except Exception as e:
        print(f"✗ Shopify integration failed: {e}")

def test_woocommerce_integration():
    """Test WooCommerce API connection."""
    try:
        order = wcapi.get("orders/1").json()
        assert order['id'] == 1
        print("✓ WooCommerce integration working")
    except Exception as e:
        print(f"✗ WooCommerce integration failed: {e}")
```

---

## Best Practices

1. **Rate Limiting:** Implement exponential backoff for retries
2. **Caching:** Cache order data with 5-minute TTL
3. **Async Processing:** Use message queues for webhook processing
4. **Monitoring:** Log all API calls and errors
5. **Security:** Rotate API keys regularly
6. **Testing:** Test integrations in sandbox environment first
7. **Documentation:** Keep integration docs updated
8. **Versioning:** Pin API versions for stability

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API keys/tokens |
| 429 Rate Limited | Too many requests | Implement backoff |
| 503 Service Unavailable | Platform down | Retry with exponential backoff |
| Webhook not firing | Webhook not registered | Check webhook configuration |
| Data mismatch | Sync issue | Force full data sync |

---

For support, visit the [GitHub repository](https://github.com/harithanandakumar/ecommerce-customer-support-chatbot) or contact the development team.
