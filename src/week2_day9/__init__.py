
"""Entry point for the week2_day9 package."""


def main() -> None:
    """Start the FastAPI calculator API."""
    import uvicorn

    uvicorn.run(
        "week2_day9.main:app",
        host="127.0.0.1",
        port=8000,
    )
