from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.middleware import RequestIDMiddleware
from app.models import URLRequest
from app.audit import audit_url

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="URL Audit Service",
    version="1.0.0"
)

# Add the middleware
app.add_middleware(RequestIDMiddleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def home():
    return {"message": "URL Audit Service is running!"}

@app.post("/audit")
@limiter.limit("10/minute")
async def audit(request: Request, body: URLRequest):
    return await audit_url(str(body.url))