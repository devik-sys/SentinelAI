import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import os

LOG_FILE = "../intrusion_log.txt"

dates = []

if os.path.exists(LOG_FILE):

    with open(
        LOG_FILE,
        "r"
    ) as file:

        for line in file:

            try:

                date = line[:10]

                dates.append(date)

            except:
                pass

counts = Counter(dates)

days = list(counts.keys())
values = list(counts.values())

plt.figure(
    figsize=(8, 4)
)

plt.bar(
    days,
    values
)

plt.title(
    "Intrusions Per Day"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Count"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    "chart.png"
)

plt.close()

print(
    "Chart Generated!"
)
