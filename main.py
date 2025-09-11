import sys
from rich.console import Console
import typer

from shutil import copyfile
from pathlib import Path
import datetime
import os

import lib

console = Console()
app = typer.Typer()
keys: tuple[bytes, bytes] = lib.ensure_key_existed('key.txt')


def ask_bool(prompt: str) -> bool:
    while True:
        answer = console.input(
            f'\n[bold yellow]{prompt} [/][magenta](y/n)[/] ').lower()
        if answer in ['y', 'n']:
            return answer == 'y'
        else:
            console.print('[red]Invalid input.[/]')


def enc_one_file(filename: str) -> None:
    console.print(f'MAIN - encrypt [yellow]{filename}[/]')
    with open(filename, 'rb') as f:
        data = f.read()
    enc = lib.AESTool(keys[0], keys[1]).encrypt(data)
    console.print(f'  encrypt done [cyan]{filename}[/]')
    save_path = Path('_public') / Path(filename).with_suffix('.enc').name

    with open(save_path, 'w', encoding='utf-8') as f:
        b64 = lib.bytes_to_base64(enc)
        f.write(b64)
    console.print(f'  save to [blue]{save_path}[/]')


def dec_one_file(filename: str) -> None:
    console.print(f'MAIN - decrypt [yellow]{filename}[/]')
    with open(filename, 'r', encoding='utf-8') as f:
        b64 = f.read()
    data = lib.base64_to_bytes(b64)
    dec = lib.AESTool(keys[0], keys[1]).decrypt(data)
    if dec is None:
        console.print(f'  decrypt failed [yellow]{filename}[/]')
    else:
        console.print(f'  decrypt done [green]{filename}[/]')
        save_path = Path('_temp') / Path(filename).with_suffix('.md').name
        with open(save_path, 'wb') as f:
            f.write(dec)
        console.print(f'  save to [blue]{save_path}[/]')


@app.command('enc')
def enc_all_files() -> None:
    """
    Encrypt all files in _private folder and save them in _public folder.
    """
    for file in Path('_private').glob('*.md'):
        enc_one_file(str(file))


@app.command('dec')
def dec_all_files() -> None:
    """
    Decrypt all files in _public folder and save them in _temp folder.
    """
    for file in Path('_public').glob('*.enc'):
        dec_one_file(str(file))


@app.command('o')
def overwrite_copy_back() -> None:
    """
    Copy back all decrypted files to _private folder.
    """
    for file in Path('_temp').glob('*.md'):
        dst = Path('_private') / file.name
        copyfile(file, dst)
        console.print(f'MAIN - Copy back [green]{file}[/] to [blue]{dst}[/]')


@app.command('ps')
def push_to_git() -> None:
    """
    Push all encrypted files to git.
    """
    os.system('git add _public/*.enc')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system(f'git commit -m "Update at {date}"')
    os.system('git push origin master')


@app.command('pl')
def pull_from_git() -> None:
    """
    Pull all encrypted files from git.
    """
    with console.status('Pulling from git...'):
        os.system('git pull origin master')


COMMANDS = {
    'e': (enc_all_files, 'Encrypt all files'),
    'd': (dec_all_files, 'Decrypt all files'),
    'o': (overwrite_copy_back, 'Copy back all decrypted files'),
    'ps': (push_to_git, 'Push all encrypted files to git'),
    'pl': (pull_from_git, 'Pull all encrypted files from git'),
}


def print_commands():
    console.print('\n[bold yellow]Commands[/]')
    for key, value in COMMANDS.items():
        console.print(f'  [bold]{key}[/] - {value[1]}')


def main():
    while True:
        print_commands()
        cmd = console.input('\n[bold yellow]Enter command[/] ').lower()
        if cmd in COMMANDS:
            func, _ = COMMANDS[cmd]
            func()
        elif cmd in ('q', 'Q', 'quit', 'exit'):
            console.print('[bold green]Bye![/]')
            break
        else:
            console.print(f'[red]Invalid command: {cmd}[/]')


if __name__ == '__main__':
    # main()
    if len(sys.argv) == 1:
        main()
    else:
        app()
