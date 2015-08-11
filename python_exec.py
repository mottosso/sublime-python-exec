import os
import time
import tempfile
import subprocess
import contextlib

import sublime
import sublime_plugin


class PythonExecCommand(sublime_plugin.WindowCommand):
    """Run Python in active view

    If view has been saved, run the file, otherwise run
    contents from memory.

    Usage:
        Create a `.sublime-build` file, set `target` to `python_exec`.

        PythonExec.sublime-build

        {
            "target": "python_exec",
            "selector": "source.python"
        }


    """

    def run(self, *args, **kwargs):
        path = self.window.active_view().file_name()

        if path:
            # Saved
            self._run_file(path)
        else:
            # Unsaved
            self._run_active_view()

    def _run_active_view(self):
        """Run contents of the active view"""
        view = self.window.active_view()
        substr = view.substr(sublime.Region(0, view.size()))

        with temp_code(substr) as path:
            return self._subprocess(path)

    def _run_file(self, path):
        """Run file from disk

        Arguments:
            path (str): Absolute path to Python file

        """

        return self._subprocess(path)

    def _subprocess(self, path):
        """Run file from disk and append output to Sublime

        Arguments:
            path (str): Absolute path to Python file

        """

        self.window.run_command("show_panel", {"panel": "output.exec"})
        output_view = self.window.create_output_panel("exec")

        __start = time.time()

        CREATE_NO_WINDOW = 0x08000000
        popen = subprocess.Popen(
            ["python", "-u", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=CREATE_NO_WINDOW
        )

        for line in popen.stdout:
            output_view.run_command("append", {
                "characters": line.decode("utf-8").replace("\r", ""),
                "force": True,
                "scroll_to_end": True
            })

        # Block until finished
        popen.communicate()

        __end = time.time()
        __duration = __end - __start

        output_view.run_command("append", {
            "characters": "[Finished in %.2fs]" % __duration,
            "force": True,
            "scroll_to_end": True
        })


@contextlib.contextmanager
def temp_code(code):
    """Temporarily write `code` to disk

    Usage:
        with temp_code("print 'Hello World'") as path:
            print(path)

    """

    tempdir = tempfile.gettempdir()
    temppath = os.path.join(tempdir, "__tempfile.py")

    with open(temppath, "w") as f:
        f.write(code)

    try:
        yield temppath
    finally:
        os.remove(temppath)
