from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base
from starlette_exporter import PrometheusMiddleware, handle_metrics

app = FastAPI()
app.include_router(router)

app.add_middleware(PrometheusMiddleware , group_paths=True)
app.add_route("/metrics", handle_metrics)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
