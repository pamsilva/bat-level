import os
import pandas as pd

from decimal import *
from datetime import datetime

from matplotlib import pyplot as plt


CURRENT_DIR = os.path.abspath(os.path.curdir)


def stupid_time_delta_parser(string_value):
    raw_data = string_value.split(" ")
    value = Decimal(raw_data[0].strip())
    delta_type = raw_data[1].strip().lower()

    res = None
    if delta_type == "days":
        res = value * 24
    elif delta_type == "hours":
        res = value
    elif delta_type == "minutes":
        res = value / 60
    else:
        raise ValueError(f"Don't know how to parse {string_value}")

    return res


def load_data(filename):
    fp = open(filename, "r")
    lines = fp.readlines()

    res = []
    for l in lines:
        values = l.split("|")

        elem = {}
        elem["timestamp"] = datetime.strptime(values[0].strip(), "%a %d %b %H:%M:%S %Z %Y")
        elem["percentage"] = int(values[1].strip().split(" ")[1][:-1])
        elem["time-left"] = stupid_time_delta_parser(values[2].strip().split(":")[1].strip()) if values[2].strip() else None
        elem["voltage"] = Decimal(values[3].strip().split(" ")[1].strip())
        elem["energy-rate"] = Decimal(values[4].strip().split(" ")[1].strip())

        res.append(elem)

    return res


def detach_cycles(df):
    intervals = df[~df["time-left"].isnull()]["timestamp"].diff()
    breaks = intervals[intervals > "00:40:00"].index.values

    res = []
    prev = 0
    for point in breaks:
        print(f'cycle: {df["timestamp"].iloc[prev]} to {df["timestamp"].iloc[point]}')
        res.append(df.iloc[prev:point])
        prev = point

    return res


def pretty_plot(i, c):
    fig, axs = plt.subplots(4, figsize=(12, 9), sharex=True)

    fig.suptitle(f'Cycle {i + 1} from {min(c["timestamp"])} to {max(c["timestamp"])}')
    
    axs[0].plot(c["timestamp"], c["percentage"])
    axs[0].set(ylabel="Battery %")
    axs[1].plot(c["timestamp"], c["time-left"], "tab:green")
    axs[1].set(ylabel="Hours left")
    axs[2].plot(c["timestamp"], c["voltage"], "tab:red")
    axs[2].set(ylabel="Volts")
    axs[3].plot(c["timestamp"], c["energy-rate"], "tab:purple")
    axs[3].set(ylabel="Rate in Watts", xlabel="Time")

    for ax in fig.get_axes():
        ax.label_outer()
        ax.grid()
        
    fig.tight_layout()
    plt.savefig(f"{CURRENT_DIR}/cycle-{i + 1}.png")


def main():
    data = load_data("/home/pedro/battery-level.data")

    df = pd.DataFrame(data)
    cycles = detach_cycles(df)

    for i, c in enumerate(cycles):
        pretty_plot(i, c)


if __name__ == "__main__":
    main()
