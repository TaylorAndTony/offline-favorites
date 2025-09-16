from rich.console import Console

import csv

console = Console()


# target = './_private/B站up主备注-离线版.csv'
target = './local/B站up主备注-离线版.csv'

def read_csv(file) -> list[list[str]]:
    with open(file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        return [row for row in reader]


def write_csv(data: list[list[str]], file) -> None:
    with open(file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(data)
        writer.writerows(data)


def main():
    console.print(f'Use file: [cyan]{target}')
    read = read_csv(target)
    console.print(f"共{len(read)}条数据")
    console.print(f"第一条数据：{read[0]}")
    console.print(f"最后一条数据：{read[-1]}")
    last_id = read[-1][0]
    if not last_id.isdigit():
        console.print("[red]最后一条数据不是数字，请检查原始 csv 文件")
        new_id = -1
    else:
        new_id = int(last_id) + 1
    while True:
        console.print(f"最新 ID 为 {new_id}")
        ask = console.input('\n[yellow]* 输入从前端脚本复制的 csv 字符串，q 退出: ')
        if ask in ('q', 'Q'):
            console.print("[green]退出程序")
            break
        parts = ask.split(',')
        length = len(parts)
        if length != 5:
            console.print("[red]输入格式错误，请检查输入内容")
            continue
        more_tags = console.input('[yellow]* 输入更多标签，空格分割，回车跳过: ')
        if more_tags:
            parts[3] = f'{more_tags} {parts[3].strip()}'
        data = [str(new_id)] + parts[1:]
        all_data = read + [data]
        write_csv(all_data, target)
        console.print(f"[green]已保存数据：{data}")
        read = all_data
        new_id += 1


if __name__ == '__main__':
    main()
