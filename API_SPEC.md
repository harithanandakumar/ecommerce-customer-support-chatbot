# API Specification - E-Commerce Customer Support Chatbot

## Overview
This document describes the REST API endpoints for the E-Commerce Customer Support Chatbot. The API provides interfaces for processing customer queries, tracking orders, managing conversations, and accessing system health metrics.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API does not require authentication. Production deployments should implement JWT or OAuth 2.0.

## Response Format
All responses are returned in JSON format with the following structure:
```json
{
  "success": boolean,
  "data": object,
  "error": string (if applicable),
  "timestamp": ISO 8601 datetime
}
```

## Endpoints

### 1. Process User Input
**Endpoint:** `POST /chat/process`

**Description:** Process a user message through the chatbot and get a response.

**Request Body:**
```json
{
  "message": "Track my order ORD001",
  "user_id": "user_123",
  "session_id": "session_456"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "response": "Your order ORD001 is currently in transit and expected to arrive by Dec 5.",
    "intent": "track_order",
    "confidence": 0.95,
    "session_id": "session_456"
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 2. Get Order Status
**Endpoint:** `GET /orders/{order_id}`

**Description:** Retrieve detailed information about a specific order.

**Parameters:**
- `order_id` (path): Order identifier (e.g., ORD001)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "order_id": "ORD001",
    "status": "in_transit",
    "items": [
      {"sku": "SKU123", "quantity": 2, "price": 29.99}
    ],
    "total": 59.98,
    "created_at": "2025-11-28T10:00:00Z",
    "expected_delivery": "2025-12-05T18:00:00Z"
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 3. Cancel Order Item
**Endpoint:** `POST /orders/{order_id}/cancel`

**Description:** Cancel a specific item from an order.

**Request Body:**
```json
{
  "sku": "SKU123",
  "reason": "Changed mind"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "order_id": "ORD001",
    "cancelled_sku": "SKU123",
    "refund_amount": 29.99,
    "status": "cancellation_processed"
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 4. Search FAQ
**Endpoint:** `GET /faq/search`

**Description:** Search the FAQ database for relevant answers.

**Query Parameters:**
- `query` (required): Search query
- `limit` (optional, default: 3): Number of results

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "query": "shipping cost",
    "results": [
      {
        "question": "What are shipping costs?",
        "answer": "Standard shipping is $5.99...",
        "relevance": 0.92
      }
    ]
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 5. System Health
**Endpoint:** `GET /health`

**Description:** Check system health and readiness.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "uptime_seconds": 3600,
    "checks": {
      "memory_available": true,
      "cpu_available": true,
      "dependencies_loaded": true
    }
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 6. Metrics
**Endpoint:** `GET /metrics`

**Description:** Get system performance metrics.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "uptime_seconds": 3600,
    "total_requests": 1250,
    "error_rate": 0.02,
    "avg_response_time_ms": 145,
    "requests_per_second": 0.35
  },
  "timestamp": "2025-12-02T13:30:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid order ID format",
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Order not found",
  "timestamp": "2025-12-02T13:30:00Z"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "timestamp": "2025-12-02T13:30:00Z"
}
```

## Rate Limiting
- Default: 1000 requests per hour
- Headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Versioning
API uses URL-based versioning (e.g., `/api/v1`, `/api/v2`).

## Examples

### cURL Examples

**Process Message:**
```bash
curl -X POST http://localhost:8000/api/v1/chat/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "user_123"}'
```

**Get Order:**
```bash
curl http://localhost:8000/api/v1/orders/ORD001
```

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```
