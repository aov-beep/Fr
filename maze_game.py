"""
Консольна гра "Лабіринт" —  на Python.

Керування: W / A / S / D або стрілки.
Мета: дійти від старту '@' до фінішу 'G' за відведений час.

Потребує Windows-консоль (використовує модуль msvcrt для читання клавіш
без Enter.
"""

import os
import sys
import time
import random

try:
    import msvcrt
except ImportError:
    msvcrt = None

MAP_FILE = "map.txt"
TIME_LIMIT = 40



def get_max_length(lines):
    max_length = len(lines[0])
    for line in lines:
        if len(line) > max_length:
            max_length = len(line)
    return max_length


def read_map(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    width = get_max_length(lines)
    height = len(lines)

    game_map = [[' ' for _ in range(height)] for _ in range(width)]
    for y in range(height):
        for x in range(width):
            game_map[x][y] = lines[y][x] if x < len(lines[y]) else ' '

    return game_map


def render_map(game_map, player_x, player_y):
    width = len(game_map)
    height = len(game_map[0])
    rows = []
    for y in range(height):
        row_chars = []
        for x in range(width):
            if x == player_x and y == player_y:
                row_chars.append('@')
            else:
                row_chars.append(game_map[x][y])
        rows.append(''.join(row_chars))
    return "\n".join(rows)




def get_direction(key):
    direction = [0, 0]
    if key in ('w', 'up'):
        direction[1] = -1
    elif key in ('s', 'down'):
        direction[1] = 1
    elif key in ('a', 'left'):
        direction[0] = -1
    elif key in ('d', 'right'):
        direction[0] = 1
    return direction


def handle_input(key, player_x, player_y, game_map):
    direction = get_direction(key)
    next_x = player_x + direction[0]
    next_y = player_y + direction[1]

    if not (0 <= next_x < len(game_map) and 0 <= next_y < len(game_map[0])):
        return player_x, player_y, False

    next_cell = game_map[next_x][next_y]

    won = False
    if next_cell == ' ' or next_cell == 'G':
        player_x, player_y = next_x, next_y
        if next_cell == 'G':
            won = True

    return player_x, player_y, won


def read_key():
    """Зчитує клавішу, включно зі стрілками (Windows, без Enter)."""
    ch = msvcrt.getch()
    if ch in (b'\x00', b'\xe0'):
        ch2 = msvcrt.getch()
        arrows = {b'H': 'up', b'P': 'down', b'K': 'left', b'M': 'right'}
        return arrows.get(ch2, '')
    try:
        return ch.decode('utf-8').lower()
    except UnicodeDecodeError:
        return ''


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')




def generate_maze(width=50, height=25):
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    grid = [['#' for _ in range(width)] for _ in range(height)]
    grid[1][1] = ' '
    stack = [(1, 1)]

    while stack:
        x, y = stack[-1]
        neighbours = []
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 2 and 0 < ny < height - 2 and grid[ny][nx] == '#':
                neighbours.append((nx, ny, dx, dy))

        if neighbours:
            nx, ny, dx, dy = random.choice(neighbours)
            grid[y + dy // 2][x + dx // 2] = ' '
            grid[ny][nx] = ' '
            stack.append((nx, ny))
        else:
            stack.pop()

    grid[height - 3][width - 2] = 'G'
    return ["".join(row) for row in grid]


def ensure_map_file(path):
    if os.path.exists(path):
        return
    lines = generate_maze()
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))



def main():
    if msvcrt is None:
        print("Ця гра використовує модуль msvcrt і працює лише в консолі Windows.")
        sys.exit(1)

    ensure_map_file(MAP_FILE)
    game_map = read_map(MAP_FILE)

    player_x, player_y = 1, 1
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        remaining = TIME_LIMIT - elapsed

        clear_console()
        print(render_map(game_map, player_x, player_y))
        print(f"\nЧас, що залишився: {max(remaining, 0):0.1f} с")

        if remaining <= 0:
            print("\nЧас вийшов! Спробуй пройти лабіринт швидше.")
            sys.exit(0)

        if msvcrt.kbhit():
            key = read_key()
            player_x, player_y, won = handle_input(key, player_x, player_y, game_map)

            if won:
                clear_console()
                print(render_map(game_map, player_x, player_y))
                total_time = time.time() - start_time
                print(f"\nТи пройшов лабіринт за {total_time:0.1f} с.")
                print("Ти молодець!")
                sys.exit(0)
        else:
            time.sleep(0.03)


if __name__ == "__main__":
    main()
