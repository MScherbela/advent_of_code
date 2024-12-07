# %%
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

url = "https://adventofcode.com/2024/leaderboard/private/view/2659480.json"

cookie_fname = "SESSION_COOKIE.txt"
if not os.path.exists(cookie_fname):
    raise FileNotFoundError(
        f"Please save your session cookie to {cookie_fname} and rerun the script."
    )
with open(cookie_fname) as f:
    session_cookie = f.read().strip()

cookies = {"session": session_cookie}
response = requests.get(url, cookies=cookies)
if response.status_code != 200:
    raise ValueError("Invalid response")
raw_data = response.json()
# %%

data = []
for member_data in raw_data["members"].values():
    name = member_data["name"]
    for day, day_data in member_data["completion_day_level"].items():
        for part, part_data in day_data.items():
            data.append(
                dict(
                    name=name,
                    day=int(day),
                    part=int(part),
                    t=datetime.datetime.fromtimestamp(part_data["get_star_ts"]),
                )
            )

df = pd.DataFrame(data)
df = df.sort_values(["name", "day", "part"]).reset_index(drop=True)
start_times = {}
for i in range(1, 26):
    start_times[i] = datetime.datetime(2024, 12, i, 0, 0, 0)
df["start_time"] = df["day"].map(start_times)

df_delta = df.pivot_table(values="t", index=["name", "day"], columns="part")
df_delta = df_delta[2] - df_delta[1]
df_delta = df_delta.reset_index().rename(columns={0: "delta_t"})


plt.close("all")
fig, axes = plt.subplots(2, 1, figsize=(8, 6))
for idx_name, name in enumerate(df_delta.name.unique()):
    color = f"C{idx_name}"
    for part, ls, marker in zip([1, 2], ["--", "-"], ["o", "x"]):
        df_plot = df[(df.name == name) & (df.part == part)]
        axes[0].plot(
            df_plot.day,
            (df_plot.t - df_plot.start_time).dt.total_seconds() / 3600,
            label=f"{name} part {part}",
            marker=marker,
            ls=ls,
            color=color,
        )

    df_delta_name = df_delta[df_delta.name == name]
    axes[1].plot(
        df_delta_name.day,
        df_delta_name.delta_t.dt.total_seconds() / 60,
        label=name,
        marker="o",
    )

for ax in axes:
    ax.set_xlabel("Day")
    ax.legend()


axes[1].set_ylim([0, 120])
axes[1].set_ylabel("Duration part 1 - part 2 / min")
axes[0].set_ylim([6, 24])
axes[0].set_ylabel("Time of completion / h")

fig.tight_layout()
