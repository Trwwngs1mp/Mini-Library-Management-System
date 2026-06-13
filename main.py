#!/usr/bin/env python3
"""
Mini Library Management System
Main entry point for the application.
"""

import sys
import os

# Ensure src package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from src.view.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()