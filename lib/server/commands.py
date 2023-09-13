import os
from subprocess import DEVNULL
from pathlib import Path
from time import sleep
from typing import Optional
from typing_extensions import Annotated
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from typer import Option, Argument, Exit
from .templates import Writer
from ..utils import cmd


project_name = "express-docker-typescript-starter-kit"
github_repo_url = f"https://github.com/jocades/{project_name}"


console = Console()


def init_server(
    project_path: Path,
    source_branch: str,
    intall_deps: bool,
):
    if project_path.exists():
        print(f"Project path '{project_path}' already exists")
        raise Exit()

    cmd(f"git clone --single-branch --branch {source_branch} {github_repo_url} {project_path}",
        stdout=DEVNULL)

    os.chdir(project_path)

    if intall_deps:
        cmd('npm install')

    cmd('rm -rf .git')
    cmd('git init')
    cmd('git add .')
    cmd(['git', 'commit', '-m', 'Initial commit'], stdout=DEVNULL)

    print(f"\n[bold green]✓[/] Project [blue]{project_path}[/] created successfully")


def route(
    name: str,
    methods: Annotated[Optional[list[str]], Argument(help="Add specific http methods")] = None,
    with_model: Annotated[bool, Option('-m', '--model', help="Create a model")] = False,
    with_handler: Annotated[bool, Option('-h', '--handler', help="Use the generic route handler")] = False,
):
    if with_handler and not with_model:
        print("The --handler option must be used with the --model option")
        raise Exit()

    writer = Writer(name, with_model, with_handler)
    writer.write(methods)
    print(f"Route '{name}' created successfully [green]✓[/] ")


def model(name: str):
    print(name)


def test(
    project_path: Annotated[Path, Argument(help="Project path")] = Path.cwd() / 'server',
    intall_deps: Annotated[bool, Option('-i', '--install', help="Install dependencies")] = False,
):
    print(project_path)
    print(intall_deps)
    console.print("[ok]Project[/] path already exists")

    JOBS = [100, 150, 25, 70, 110, 90]

    progress = Progress(auto_refresh=False)
    master_task = progress.add_task("overall", total=sum(JOBS))
    jobs_task = progress.add_task("jobs")

    progress.console.print(
        Panel(
            "[bold blue]A demonstration of progress with a current task and overall progress.",
            padding=1,
        )
    )

    with progress:
        for job_no, job in enumerate(JOBS):
            progress.log(f"Starting job #{job_no}")
            sleep(0.2)
            progress.reset(jobs_task, total=job, description=f"job [bold yellow]#{job_no}")
            progress.start_task(jobs_task)
            for wait in progress.track(range(job), task_id=jobs_task):
                sleep(0.01)
            progress.advance(master_task, job)
            progress.log(f"Job #{job_no} is complete")
        progress.log(
            Panel(":sparkle: All done! :sparkle:", border_style="green", padding=1)
        )
