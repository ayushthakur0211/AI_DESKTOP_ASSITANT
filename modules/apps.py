import subprocess
import os


def open_chrome():
    subprocess.Popen("start chrome", shell=True)


def open_edge():
    subprocess.Popen("start msedge", shell=True)


def open_notepad():
    subprocess.Popen("notepad")


def open_calculator():
    subprocess.Popen("calc")


def open_paint():
    subprocess.Popen("mspaint")


def open_explorer():
    subprocess.Popen("explorer")


def open_vscode():
    paths = [
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
    ]

    for path in paths:
        path = os.path.expandvars(path)

        if os.path.exists(path):
            subprocess.Popen(path)
            return True

    subprocess.Popen("code", shell=True)