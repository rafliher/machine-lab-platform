from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
import os

from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.hosts import router as host_router
from app.api.containers import router as container_router

from app.core.events import startup as on_startup
from dotenv import load_dotenv

load_dotenv()  # dev convenience

# Check if we're in development mode
is_development = os.getenv("ENVIRONMENT", "development").lower() == "development"

app = FastAPI(
    title="Machine‑Lab Manager",
    description="API for managing container hosts, VPN profiles, and containerized environments",
    version="1.0.0",
    # Only show docs in development
    docs_url="/docs" if is_development else None,
    redoc_url="/redoc" if is_development else None,
    openapi_url="/openapi.json" if is_development else None,
)

# DEV
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(host_router)
app.include_router(container_router)

@app.on_event("startup")
async def app_startup():
    await on_startup()

@app.get("/health", tags=["meta"])
async def health():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}


# Custom OpenAPI schema with better documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Machine‑Lab Manager API",
        version="1.0.0",
        description="""
        ## Machine Lab Platform Manager API
        
        This API manages containerized environments with VPN integration for secure access.
        
        ### Features:
        - **Authentication**: Admin login with API key management
        - **Host Management**: Register and monitor container hosts
        - **Container Lifecycle**: Launch, restart, and terminate containerized environments
        - **VPN Integration**: Automatic VPN profile creation and traffic routing
        - **Real-time Monitoring**: Host health and resource usage tracking
        
        ### Authentication:
        Most endpoints require admin authentication using the `X-Admin-Key` header.
        Host heartbeat endpoints use the `X-Server-Key` header for server-to-server communication.
        
        ### Workflow:
        1. Login to get an admin API key
        2. Register container hosts
        3. Upload and launch containerized environments
        4. Monitor host and container status
        5. Manage VPN profiles for secure access
        """,
        routes=app.routes,
        tags=[
            {
                "name": "auth",
                "description": "Authentication and API key management"
            },
            {
                "name": "hosts", 
                "description": "Container host registration and monitoring"
            },
            {
                "name": "containers",
                "description": "Container lifecycle management with VPN integration"
            },
            {
                "name": "users",
                "description": "VPN profile management for users and containers"
            },
            {
                "name": "meta",
                "description": "System health and metadata endpoints"
            }
        ]
    )
    
    # Add security scheme for API keys
    openapi_schema["components"]["securitySchemes"] = {
        "AdminKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-Admin-Key",
            "description": "Admin API key obtained from login endpoint"
        },
        "ServerKey": {
            "type": "apiKey", 
            "in": "header",
            "name": "X-Server-Key",
            "description": "Server key for host-to-manager communication"
        }
    }
    
    # Add security to endpoints that require it
    for path_data in openapi_schema["paths"].values():
        for method_data in path_data.values():
            if isinstance(method_data, dict) and "tags" in method_data:
                if method_data["tags"][0] in ["hosts", "containers", "users"]:
                    if "/heartbeat" in str(path_data):
                        method_data["security"] = [{"ServerKey": []}]
                    else:
                        method_data["security"] = [{"AdminKey": []}]
                elif method_data["tags"][0] == "auth" and "login" not in method_data.get("operationId", ""):
                    method_data["security"] = [{"AdminKey": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


if is_development:
    app.openapi = custom_openapi
    
    @app.get("/api-docs", response_class=HTMLResponse, include_in_schema=False)
    async def custom_swagger_ui():
        """Custom Swagger UI page available only in development mode."""
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=f"{app.title} - API Documentation",
            swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
        )