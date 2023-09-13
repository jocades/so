from subprocess import run, CompletedProcess, CalledProcessError
from rich import print
from rich.console import Console
from typer import Exit

console = Console()


def cmd(command: str | list[str], **kwargs) -> CompletedProcess:
    try:
        command = command.split() if isinstance(command, str) else command
        return run(command, check=True, **kwargs)
    except CalledProcessError as e:
        print(e.stderr)
        raise Exit()
