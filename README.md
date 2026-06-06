# Ecommerce Backend

REST API for products, auth, cart, orders, and checkout.

## Django API (`backend/`)

See [backend/README.md](backend/README.md) for setup, environment variables, and endpoints.

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py runserver
```

API base: `http://localhost:8000/api/`

## Stripe checkout server (`server/`)

Optional Node.js service for Stripe checkout sessions.

```bash
cd server
npm install
npm run dev
```

Runs on `http://localhost:7000` by default. Set `STRIPE_SECRET_KEY` in `server/.env`.
# django_ecommerce_backend
