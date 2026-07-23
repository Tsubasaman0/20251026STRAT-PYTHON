from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.questions import router as questions_router


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(title="AI会議室", version="0.1.0")
    application.mount(
        "/static",
        StaticFiles(directory=BASE_DIR / "static"),
        name="static",
    )
    application.include_router(questions_router)

    @application.get("/", response_class=HTMLResponse)
    async def show_home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={},
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_error(
        _request: Request,
        _error: Exception,
    ) -> JSONResponse:
        # 内部情報をブラウザへ漏らさず、利用者が再試行できる表現に統一する。
        return JSONResponse(
            status_code=500,
            content={"detail": "処理中にエラーが発生しました。もう一度お試しください。"},
        )

    return application


app = create_app()
