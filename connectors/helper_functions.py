# @Project:     Crypto-Bot
# @Filename:    helper_functions.py
# @Author:      Daksh Gaur
# @Email:       hi@daksh.fyi
# @Time:        14-07-2023 11:56 am


def tick_to_decimals(tick_size: float) -> int:
    tick_size_str = "{0:.8f}".format(tick_size)

    while tick_size_str[-1] == "0": # Remove trailing zeroes
        tick_size_str = tick_size_str[:-1]

    split_tick = tick_size_str.split(".")

    return len(split_tick[1]) if len(split_tick) > 1 else 0 # Return number of decimal places
