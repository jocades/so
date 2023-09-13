import os
import json
import shutil
from pathlib import Path
from subprocess import DEVNULL
from ..utils import cmd
from rich import print


source_path = Path(__file__).parent / 'template'


def init_client(project_path: Path, new_app: bool, intall_deps: bool):
    # install next js if necessary
    if new_app:
        cmd(f'pnpm dlx create-next-app@latest --use-pnpm {project_path}', cwd=project_path.parent)

    # manage setup files
    for file in ['prettier.config.js', 'tailwind.config.ts', '.env.local', '.gitignore', 'next-config.js']:
        shutil.copy(source_path / file, project_path / file)

    if (project_path / 'tailwind.config.js').exists():
        (project_path / 'tailwind.config.js').unlink()

    if (project_path / 'src' / 'app' / 'globals.css').exists():
        (project_path / 'src' / 'app' / 'globals.css').unlink()

    # update package.json
    data = json.loads((source_path / 'package.json').read_text())
    pkgs = json.loads((project_path / 'package.json').read_text())

    for k in data:
        if k not in pkgs:
            pkgs[k] = {}
        for sub_k, v in data[k].items():
            pkgs[k][sub_k] = v

    (project_path / 'package.json').write_text(json.dumps(pkgs, indent=2))

    # merge src folder
    for item in (source_path / 'src').glob('**/*'):
        if item.is_file():
            relative_path = item.relative_to(source_path / 'src')
            dest = project_path / 'src' / relative_path

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

    print(f"[bold green]✓[/] Setup files copied")

    os.chdir(project_path)

    # install dependencies
    if intall_deps:
        cmd('pnpm install')

    cmd('git add .', stdout=DEVNULL)
    cmd(['git', 'commit', '-m', 'add setup files'], stdout=DEVNULL)

    print(f"\n[bold green]✓[/] Project [blue]{project_path}[/] created successfully")
