# Instructions for this repo

This repository is a MonaOS-based port of classic Tetris targeting the GitHub Badger. The code runs on-device under MonaOS and uses the badgeware library for rendering and input/output (display and buttons).

## Runtime Environment

**This codebase must only be run with MicroPython.** The code is designed specifically for the MicroPython interpreter running on embedded hardware (GitHub Badger with MonaOS). It uses MicroPython-specific modules and features that are not available in standard CPython, and conversely, it avoids CPython features that are not available in MicroPython.

## Architecture overview

- Entry point: `tetris/__init__.py`
  - Game loop with `setup()` and `loop()` methods inside a `Tetris` class.
  - Game state encapsulated in the `Tetris` class instance: `current`, `next_piece`, `blocks`, `score`, `rows`, `lost`, etc.
  - Core helpers (methods of `Tetris` class):
    - Board/pieces: `each_block`, `occupied`, `unoccupied`, `random_piece`
    - Game control: `move`, `rotate`, `drop`, `drop_piece`, `remove_lines`, `remove_line`, `reset`
    - Scoring/rows: `set_score`, `add_score`, `set_rows`, `add_rows`, `set_visual_score`, `clear_score`, `clear_rows`
    - Grid access: `get_block`, `set_block`, `clear_blocks`
    - Rendering: `draw`, `draw_court`, `draw_next`, `draw_score`, `draw_piece`, `draw_block`
    - Input handling: `on_left_button`, `on_right_button`, `on_rotate_button` (uses global `debounce` function)
- Badgeware integration
  - Rendering and I/O are provided by the badgeware library available on MonaOS. The game uses badgeware's display primitives for drawing and badgeware's button input for controls.
  - Color/monochrome handling and frame updates follow the badgeware display API; button mappings align with the GitHub Badger hardware layout.

## Key conventions and patterns

- Snake case for functions and variables throughout `tetris/__init__.py`.
- Object-oriented design with game state encapsulated in a `Tetris` class. The game creates a single instance `_game` and runs it in a simple main loop.
- The playfield is an `nx` by `ny` grid (15x15). `blocks[x][y]` holds either `None` or a piece type dict (`i, j, l, o, s, t, z`).
- Piece rotation uses 16-bit bitmasks in `type["blocks"][dir]` and is iterated via `each_block`.

## Developer workflows

- Running on device (MonaOS): deploy the app to the GitHub Badger running MonaOS following the standard MonaOS app deployment flow. The system launches `tetris/__init__.py` on-device.
- Desktop execution: This repo imports MonaOS/badgeware-only modules that are MicroPython-specific. For local syntax checks, you can use MicroPython stubs under `typings/` (where available) and expect editor diagnostics for platform-specific modules. Ruff/Pylance warnings are expected on desktop when running with CPython.
- No test suite is present. If adding tests, isolate hardware-bound code behind light wrappers or flags.
- **Important**: The code uses only MicroPython-compatible features. Avoid using CPython-only modules or language features not supported by MicroPython (e.g., full enum module, typing annotations at runtime, etc.).

## Rendering and input specifics

- Display size is derived via the badgeware display API, and block size computed as:
  - `dx = (0.6 * WIDTH) / nx`
  - `dy = (0.75 * HEIGHT) / ny`
- Court rendering offsets the playfield by `+6` blocks on X to make room for next-piece/score.
- Buttons used: mapped via badgeware's input layer to the Badger's hardware buttons for Left, Right, and Rotate. See the input handlers in code for exact mappings.
- Debounce logic uses a simple timestamp-based approach with a module-scoped `last_button_press` to avoid rapid repeats.

## Adding features safely

- Keep function naming and call sites in snake_case.
- When changing rendering, update `draw_*` functions.
- When introducing new inputs or animations, reuse `debounce` pattern and avoid blocking sleeps in the main loop except for post-lose pause.
- If refactoring globals, do it incrementally: first encapsulate score/rows, then piece state, verifying `move`, `drop`, and `occupied` continue to work.

## External dependencies and environment

- **MicroPython runtime** (required) - All code must be compatible with MicroPython.
- MonaOS on the GitHub Badger hardware.
- badgeware library for display rendering and button I/O. These platform modules are not pip-installable for desktop; use MicroPython stubs or ignore diagnostics in editors.
- Standard MicroPython modules: `random`, `time`, `machine` (for hardware PWM/Pin control).

## Examples from code

- Iterate a piece shape across the grid:
  - `each_block(piece_type, x, y, dir, lambda bx, by: set_block(bx, by, piece_type))`
- Check placement before moving/rotating:
  - `if unoccupied(current["type"], new_x, new_y, new_dir): ...`
- Line removal and scoring:
  - `remove_lines()` scans from bottom up; after `n` lines: `add_rows(n)` and `add_score(100 * 2 ** (n - 1))`.

## Agent tips

- Respect embedded constraints (keep memory use modest; avoid heavy libraries).
- Don’t reorder badgeware/MonaOS imports; keep hardware- and OS-specific code centralized.
- If you need to silence desktop-only import warnings, prefer editor config or per-file ignore; do not alter runtime behavior for device.
- **MicroPython compatibility**: Only use features available in MicroPython. Avoid CPython-only modules and features. Test with MicroPython when possible.
