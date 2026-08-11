"""Cloudflare Worker entrypoint that serves the FastAPI app."""

from workers import WorkerEntrypoint

from genimg.api import app  # noqa: F401 – FastAPI app used by asgi.fetch


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)
