from fastmcp import FastMCP
from contextlib import AsyncExitStack, asynccontextmanager
from starlette.applications import Starlette
from starlette.routing import Mount

from modules.module_a.server import mcp as mcp_a
from modules.module_b.server import mcp as mcp_b

# 为每个模块生成 ASGI 应用实例
app_a_sse = mcp_a.http_app(path="/", transport="sse")
app_a_streamable = mcp_a.http_app(path="/", transport="http")

app_b_sse = mcp_b.http_app(path="/", transport="sse")
app_b_streamable = mcp_b.http_app(path="/", transport="http")

# 统一 Lifespan
@asynccontextmanager
async def combined_lifespan(app):
    async with AsyncExitStack() as stack:
        for mcp_app in [app_a_sse, app_a_streamable, app_b_sse, app_b_streamable]:
            if mcp_app.lifespan:
                await stack.enter_async_context(mcp_app.lifespan(app))
        yield

# 顶层路由
root = Starlette(
    routes=[
        Mount("/module_a/sse", app=app_a_sse),
        Mount("/module_a/streamable", app=app_a_streamable),
        Mount("/module_b/sse", app=app_b_sse),
        Mount("/module_b/streamable", app=app_b_streamable),
    ],
    lifespan=combined_lifespan
)

# 运行服务: uvicorn main:root --reload --host 0.0.0.0 --port 8001
