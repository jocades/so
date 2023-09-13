from enum import Enum
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from rich.prompt import Confirm
from typer import Typer, Option, Argument
from lib.server.commands import init_server
from lib.client.commands import init_client


app = Typer()


class Init(str, Enum):
    server = "server"
    client = "client"


@app.command()
def init(
    project_type: Annotated[Init, Argument(help="Project type")],
    project_path: Annotated[Optional[Path], Argument(help="Project path")] = None,
    source_branch: Annotated[str, Option('-b', '--branch', help="Source branch")] = 'master',
    intall_deps: Annotated[bool, Option('-i', '--install', help="Install dependencies")] = False,
):
    if project_path is None:
        project_path = Path.cwd() / f'myapp-{project_type.value}'
    else:
        project_path = project_path.resolve()

    # server
    if project_type == Init.server:
        init_server(project_path, source_branch, intall_deps)

    # client
    if project_type == Init.client:
        new_app = False

        if not (project_path / 'package.json').exists():
            new_app = Confirm.ask('Install fresh next app?')

        init_client(project_path, new_app, intall_deps)


@app.command()
def client():
    pass


@app.command()
def server():
    pass


if __name__ == "__main__":
    app()
