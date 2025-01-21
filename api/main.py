import typer
import uvicorn
import os


def main(
    port: int = 8080,
    debug: bool = bool(os.getenv("DEBUG", False)),
):
    run_kwargs = {"host": "0.0.0.0", "port": port, "reload": debug, "loop": "uvloop"}

    uvicorn.run("src.app:app", **run_kwargs)


if __name__ == "__main__":
    typer.run(main)
