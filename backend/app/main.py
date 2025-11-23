from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.infrastructure.agents.definitions import setup_agents_client


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,
                  openapi_url=f"{settings.API_V1_STR}/openapi.json")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Events
    @app.on_event("startup")
    async def startup_event():
        setup_agents_client()

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
