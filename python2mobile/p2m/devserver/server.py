"""
P2M DevServer - FastAPI + WebSocket live reload and event bridge.

Flow:
  Browser click → WS → dispatch(action) → handler updates state
  → Render.execute(view_func) → render_content() → WS → browser innerHTML swap
"""
import json
from typing import Callable, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


def start_server(
    html_content: str,
    port: int = 3000,
    view_func: Optional[Callable] = None,
    project_dir: str = ".",
):
    from p2m.core import events
    from p2m.core.render_engine import RenderEngine
    from p2m.core.runtime import Render
    from fastapi.staticfiles import StaticFiles
    from pathlib import Path

    app = FastAPI()
    app.state.html_content = html_content
    app.state.view_func = view_func

    assets_path = Path(project_dir) / "assets"
    if assets_path.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

    @app.get("/", response_class=HTMLResponse)
    async def root():
        return app.state.html_content

    @app.websocket("/ws")
    async def ws_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    data = json.loads(raw)
                    etype = data.get("type", "")
                    action = data.get("action", "")

                    if etype == "click":
                        args = data.get("args", [])
                        events.dispatch(action, *args)
                    elif etype in ("change", "input"):
                        value = data.get("value", "")
                        events.dispatch(action, value)

                    # Re-render and push new content
                    if app.state.view_func:
                        tree = Render.execute(app.state.view_func)
                        engine = RenderEngine()
                        content = engine.render_content(tree)
                        await websocket.send_text(
                            json.dumps({"type": "render", "html": content})
                        )

                except json.JSONDecodeError:
                    pass
                except Exception as exc:
                    import traceback
                    traceback.print_exc()
                    try:
                        await websocket.send_text(
                            json.dumps({"type": "error", "message": str(exc)})
                        )
                    except Exception:
                        pass

        except WebSocketDisconnect:
            pass
        except Exception as exc:
            print(f"[P2M] WebSocket fatal: {exc}")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
