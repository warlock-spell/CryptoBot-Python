# @Project:     Crypto-Bot
# @Filename:    root_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 03:25 pm

import tkinter as tk
import components.styles as st

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Bot")
        self.configure(bg=st.BG_COLOR_1)

        # Component style: 2 frames -> left and right
        # Left frame: 2 frames -> top and bottom -> top_left and bottom_left
        # Right frame: 2 frames -> top and bottom -> top_right and bottom_right
        self.left_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self.left_frame.pack(side=tk.LEFT)

        self.right_frame = tk.Frame(self, bg=st.BG_COLOR_1)
        self.right_frame.pack(side=tk.RIGHT)