import os

from typer import Option, Typer
from typing_extensions import Annotated

from joom3y.joom3y import scan

app = Typer()


@app.command()
def main(
    url: Annotated[str, Option("--url", "-u", help="The Joomla URL to scan.")],
    threads: Annotated[
        int, Option("--threads", "-t", help="Number of threads to use.")
    ] = os.cpu_count(),
):
    scan(url, threads)


if __name__ == "__main__":
    app()
