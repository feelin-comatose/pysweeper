# pysweeper

Minesweeper ("Spleen Sweeper") made with pygame-ce.

## Run

```bash
pip install -r requirements.txt
python main.py
```

The game asks in the terminal for the number of columns, rows (1–200 each) and mines, then opens the window.

## Controls

- **Left click**: open a tile (click an open number to chord)
- **Right click**: place or remove a flag
- **Middle click**: chord (open all unflagged neighbours of a number whose flags are all placed)
- **R**: restart
- **Q**: quit

The first click is always safe. The window title shows how many mines are left.
