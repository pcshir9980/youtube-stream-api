from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/info")
def get_info(url: str):
    try:
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        if info.get("is_live"):
            raise HTTPException(
                status_code=400,
                detail="Live streams are not supported"
            )

        formats = []

        for f in info.get("formats", []):
            if f.get("url") and f.get("vcodec") != "none":
                formats.append({
                    "format_id": f.get("format_id"),
                    "height": f.get("height"),
                    "ext": f.get("ext"),
                    "protocol": f.get("protocol"),
                })

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "formats": formats
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
