# @Project:     Crypto-Bot
# @Filename:    logging_component.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 03:49 pm

import tkinter as tk
import components.styles as st


class Logging(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logging_text = tk.Text(self,
                                    height=10,
                                    width=60,
                                    state=tk.DISABLED,
                                    bg=st.BG_COLOR_1,
                                    fg=st.FG_COLOR_2,
                                    font=st.GLOBAL_FONT)

        self.logging_text.pack(side=tk.TOP)

    def add_log(self, message: str):

        # Unlock the text widget
        self.logging_text.configure(state=tk.NORMAL)

        # Add the message
        self.logging_text.insert("1.0", message + "\n") # 1.0 means line 1, character 0

        # Lock it again after adding the message
        self.logging_text.configure(state=tk.DISABLED)

