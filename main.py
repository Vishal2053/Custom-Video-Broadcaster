import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from stream_utils import Streaming
import threading

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

stream_thread = None

streaming = Streaming()


@app.get("/")
def surf_ui():
    return FileResponse('static/index.html')

@app.get("/start")
def start_streame(
    source: str = Query("0"),
    fps: int = Query(15),
    blur_strength : int = Query(21),
    background : str = Query("none")
):
    streaming.update_streamming_config(in_source=source, fps= fps, out_source=None, blur_strength=blur_strength,background=background)
    
    if streaming.running:
        return JSONResponse(content={"message": "Streaming already running"}, status_code=400)
    streaming_thread = threading.Thread(target=streaming.stream_video, args=())
    streaming_thread.start()
    
    return {'message': f'Streaming started from source {source} at {fps} fps with blur strength {blur_strength}'}

@app.get("/stop")
def stop_stream():
    return streaming.update_running_status(False)

@app.get("/devices")
def devices():
    return streaming.list_available_devices()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)