import tkinter as tk
from tkinter import messagebox
import random
import heapq

SIZE = 6

root = tk.Tk()
root.title("🏴‍☠️ Treasure Hunter AI")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

level = tk.StringVar(value="Easy")

human_score = 0
ai_score = 0


# ---------------- A* ALGORITHM ---------------- #

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal):

    pq = []
    heapq.heappush(pq, (0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while pq:

        _, current = heapq.heappop(pq)

        if current == goal:

            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path

        r, c = current

        neighbors = [
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1)
        ]

        for nr, nc in neighbors:

            if not (0 <= nr < SIZE and 0 <= nc < SIZE):
                continue

            if board[nr][nc] == "X":
                continue

            new_cost = cost_so_far[current] + 1

            if ((nr, nc) not in cost_so_far or
                    new_cost < cost_so_far[(nr, nc)]):

                cost_so_far[(nr, nc)] = new_cost

                priority = new_cost + heuristic(
                    (nr, nc), goal
                )

                heapq.heappush(
                    pq,
                    (priority, (nr, nc))
                )

                came_from[(nr, nc)] = current

    return []


# ---------------- GAME SETUP ---------------- #

def start_game():
    global board, human, ai
    global human_score, ai_score

    human_score = 0
    ai_score = 0

    settings = {
        "Easy": (4, 5),
        "Medium": (6, 8),
        "Hard": (8, 10)
    }

    treasures, obstacles = settings[level.get()]

    board = [[" " for _ in range(SIZE)]
             for _ in range(SIZE)]

    human = [0, 0]
    ai = [SIZE - 1, SIZE - 1]

    # Place obstacles
    count = 0
    while count < obstacles:

        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)

        if board[r][c] == " " and \
                [r, c] != human and \
                [r, c] != ai:

            board[r][c] = "X"
            count += 1

    # Place treasures
    count = 0
    while count < treasures:

        r = random.randint(0, SIZE - 1)
        c = random.randint(0, SIZE - 1)

        if board[r][c] == " ":
            board[r][c] = "T"
            count += 1

    draw()


# ---------------- DRAW BOARD ---------------- #

def draw():

    for r in range(SIZE):
        for c in range(SIZE):

            text = ""
            bg = "#7CB342"   # grass

            if board[r][c] == "T":
                text = "💰"
                bg = "#FFD700"

            elif board[r][c] == "X":
                text = "🪨"
                bg = "#424242"

            if [r, c] == human:
                text = "😀"
                bg = "#4CAF50"

            if [r, c] == ai:
                text = "🤖"
                bg = "#2196F3"

            cells[r][c].config(
                text=text,
                bg=bg,
                fg="white"
            )

    score_label.config(
        text=f"🏆 Human: {human_score}     🤖 AI: {ai_score}"
    )


# ---------------- AI MOVE ---------------- #

def ai_move():
    global ai_score

    treasures = []

    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == "T":
                treasures.append((r, c))

    if not treasures:
        check_game()
        return

    target = min(
        treasures,
        key=lambda t:
        heuristic((ai[0], ai[1]), t)
    )

    path = astar(
        (ai[0], ai[1]),
        target
    )

    if path:

        next_step = path[0]

        ai[0] = next_step[0]
        ai[1] = next_step[1]

    if board[ai[0]][ai[1]] == "T":
        board[ai[0]][ai[1]] = " "
        ai_score += 1

    draw()
    check_game()


# ---------------- HUMAN MOVE ---------------- #

def move(event):
    global human_score

    directions = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    if event.keysym not in directions:
        return

    dr, dc = directions[event.keysym]

    nr = human[0] + dr
    nc = human[1] + dc

    if (0 <= nr < SIZE and
            0 <= nc < SIZE and
            board[nr][nc] != "X"):

        human[0] = nr
        human[1] = nc

        if board[nr][nc] == "T":
            board[nr][nc] = " "
            human_score += 1

        draw()

        root.after(300, ai_move)


# ---------------- GAME OVER ---------------- #

def check_game():

    treasures_left = sum(
        row.count("T") for row in board
    )

    if treasures_left == 0:

        if human_score > ai_score:
            result = "🎉 Human Wins!"

        elif ai_score > human_score:
            result = "🤖 AI Wins!"

        else:
            result = "🤝 Draw!"

        messagebox.showinfo(
            "Game Over",
            f"Human Score: {human_score}\n"
            f"AI Score: {ai_score}\n\n"
            f"{result}"
        )


# ---------------- GUI ---------------- #

title = tk.Label(
    root,
    text="🏴‍☠️ TREASURE HUNTER AI",
    font=("Arial", 22, "bold"),
    bg="#1E1E1E",
    fg="gold"
)
title.pack(pady=10)

top_frame = tk.Frame(
    root,
    bg="#1E1E1E"
)
top_frame.pack()

tk.Label(
    top_frame,
    text="Difficulty:",
    font=("Arial", 12, "bold"),
    bg="#1E1E1E",
    fg="white"
).pack(side="left", padx=5)

tk.OptionMenu(
    top_frame,
    level,
    "Easy",
    "Medium",
    "Hard"
).pack(side="left", padx=5)

tk.Button(
    top_frame,
    text="🎮 New Game",
    command=start_game,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold")
).pack(side="left", padx=5)

score_label = tk.Label(
    root,
    font=("Arial", 16, "bold"),
    bg="#1E1E1E",
    fg="white"
)
score_label.pack(pady=10)

frame = tk.Frame(
    root,
    bg="#1E1E1E"
)
frame.pack(pady=10)

cells = []

for r in range(SIZE):

    row = []

    for c in range(SIZE):

        lbl = tk.Label(
            frame,
            width=6,
            height=3,
            relief="raised",
            bd=2,
            font=("Segoe UI Emoji", 18, "bold")
        )

        lbl.grid(
            row=r,
            column=c,
            padx=2,
            pady=2
        )

        row.append(lbl)

    cells.append(row)

root.bind("<Key>", move)

start_game()

root.mainloop()
