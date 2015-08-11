# Python Exec for Sublime Text 3

Run Python in Sublime Text without saving.

This is a limited replacement build system for Python, meant for quick sketching in arbitrary views without the need to save.

### Usage

1. Save `python_exec.py` and `PythonExec.sublime-build` in your `Preferences: Browse Packages` directory.
2. Ctrl+B
3. Select `PythonExec`
4. To switch back, repeat 2-3 and select `Python`

### Limitations

- Single-threaded, which means long-running Python processes will not output until finished.