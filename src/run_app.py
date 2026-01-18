from main import create_app
import uvicorn


def main():
    app = create_app()
    # Run uvicorn programmatically to avoid import/reloader complexity
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="debug")


if __name__ == "__main__":
    main()
