import time
from functools import wraps

from web_scrawler_script.main import async_get_data, REFERENCES, EXTERNAL_URLS, INTERNAL_URLS
from web_scrawler_script.utils import save_to_file
from web_scrawler_script.node_class import Node

import asyncio
import typer


app = typer.Typer(pretty_exceptions_show_locals=False)


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        f(*args, **kwargs)
        stop = time.perf_counter()
        result_time = stop - start
        typer.secho(f"\n-----Program took: {result_time:.2f} seconds-----\n", fg=typer.colors.BRIGHT_MAGENTA)

    return wrapper


@app.command()
@timer
def crawl(page: str, format: str, output: str) -> None:
    start_node = Node(page)
    typer.echo(asyncio.run(async_get_data(base_url=page, node=start_node)))

    Node.REFERENCES = REFERENCES
    if len(REFERENCES) == 0:
        typer.secho("There's not anything to save. Please provide another link.", fg=typer.colors.RED)
        typer.echo()
        return

    save_to_file(format, output, start_node)
    typer.echo(f"[+] Total External links: {typer.style(len(EXTERNAL_URLS), fg=typer.colors.GREEN, bold=True)}")
    typer.echo(f"[+] Total Internal links: {typer.style(len(INTERNAL_URLS), fg=typer.colors.GREEN, bold=True)}")
    total = len(EXTERNAL_URLS) + len(INTERNAL_URLS)
    typer.echo(f"[+] Total links: {typer.style(total, fg=typer.colors.GREEN, bold=True)}")
    typer.echo()


@app.command()
@timer
def print_tree(page: str) -> None:
    start_node = Node(page)

    typer.echo(asyncio.run(async_get_data(base_url=page, node=start_node)))

    start_node.depth_first_search(array=[])

    # print the structure of the page as a tree
    print(start_node)


if __name__ == "__main__":
    app()
