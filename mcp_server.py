from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from typing import Callable, List, Optional
import importlib

class FastMCP:
    def __init__(self, name: str):
        self.name = name
        self.app = FastAPI(title=name)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def tool(self, path: Optional[str] = None, methods: Optional[List[str]] = None):
        """Decorator to register a tool endpoint"""
        methods = methods or ["POST"]
        def decorator(fn: Callable):
            route = path or f"/tools/{fn.__name__}"
            self.app.add_api_route(route, fn, methods=methods)
            return fn
        return decorator

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the MCP server"""
        try:
            uvicorn = importlib.import_module("uvicorn")
        except ModuleNotFoundError as exc:
            raise RuntimeError("uvicorn is not installed; install with 'pip install uvicorn'") from exc
        uvicorn.run(self.app, host=host, port=port)