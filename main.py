import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=False,
        #access_log=False,
        log_level="critical"  # disables info/debug logs from uvicorn.*
    )