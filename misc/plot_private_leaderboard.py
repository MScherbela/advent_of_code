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
                    timestamp=part_data["get_star_ts"],
                )
            )

df = pd.DataFrame(data)
start_times = {}
for i in range(1, 26):
    start_times[i] = datetime.datetime(2024, 12, i, 6, 0, 0).timestamp()
df["start_time"] = df["day"].map(start_times)
df["t"] = df["timestamp"] - df["start_time"]

df_delta = df.pivot_table(values="t", index=["name", "day"], columns="part")
df_delta = df_delta[2] - df_delta[1]
df_delta = df_delta.reset_index().rename(columns={0: "delta_t"})

plt.close("all")
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
for name in df_delta.name.unique():
    df_name = df_delta[df_delta.name == name]
    ax.plot(df_name.day, df_name.delta_t / 60, label=name, marker="o")
ax.set_ylim([0, 300])
ax.set_xlabel("Day")
ax.set_ylabel("Time (part2) - Time (part1) [minutes]")
ax.legend()
