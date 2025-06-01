# utils.py

import random
from datetime import datetime

import numpy as np

MAX_WAIT_SEC = 20 * 60  # 20 minutes in seconds
UPDATE_TIME = 1


def compute_table_stats(block_array: np.ndarray) -> dict:
    block_nbr = block_array.shape[0]
    total_seats = block_nbr * 10 * 4
    occupied_seats = int((block_array == 1).sum())
    free_seats = total_seats - occupied_seats

    free_tables = 0
    for block in block_array:
        sums_per_table = block.sum(axis=1)
        free_tables += int((sums_per_table == 0).sum())

    pct_free_seats = (free_seats / total_seats) * 100 if total_seats else 0.0
    return {
        "free_tables": free_tables,
        "free_seats": free_seats,
        "pct_free_seats": round(pct_free_seats, 2),
    }


def init_mensa_data(mensa) -> dict:
    block_nbr = mensa.block_nbr
    capacity = block_nbr * 10 * 4
    queue_speed = 0.01 * capacity / 60
    max_queue = queue_speed * MAX_WAIT_SEC
    queue_len = random.randint(0, int(max_queue))

    print("QUEUE SPEED:", queue_speed, "MAX QUEUE:", max_queue)

    timestamp = int(datetime.now().timestamp())
    # 25% chance a seat is occupied
    block_array = (np.random.rand(block_nbr, 10, 4) < 0.25).astype(int)
    wait_time = int(queue_len / queue_speed) if queue_speed > 0 else 0
    stats = compute_table_stats(block_array)

    return {
        "queue_len": queue_len,
        "timestamp": timestamp,
        "block_list": block_array,
        "wait_time": wait_time,
        "free_tables": stats["free_tables"],
        "free_seats": stats["free_seats"],
        "pct_free_seats": stats["pct_free_seats"],
    }


def update_mensa_data(mensa, mensa_data: dict) -> dict:
    current_ts = int(datetime.now().timestamp())
    time_delta = current_ts - mensa_data["timestamp"]
    if time_delta < UPDATE_TIME:
        return mensa_data

    block_nbr = mensa.block_nbr
    capacity = block_nbr * 10 * 4
    queue_speed = 0.05 * capacity / 60
    # update queue length by ±5%
    change_pct = random.uniform(-0.05, 0.05)
    new_queue = int(mensa_data["queue_len"] * (1 + change_pct))
    max_queue = queue_speed * MAX_WAIT_SEC

    if new_queue < max_queue / 2 and random.random() < 0.5:
        new_queue += random.randint(1, 2)

    mensa_data["queue_len"] = max(0, min(new_queue, int(max_queue)))
    mensa_data["timestamp"] = current_ts
    mensa_data["wait_time"] = int(mensa_data["queue_len"] /
                                  queue_speed) if queue_speed > 0 else 0

    block_array: np.ndarray = mensa_data["block_list"]

    for i in range(block_nbr):
        block = block_array[i]

        # fill 0–2 empty tables with weighted probability
        empty_tables = [idx for idx, row in enumerate(block) if row.sum() == 0]
        fill_n = random.choices([0, 1, 2, 3, 4],
                                weights=[0.7, 0.1, 0.05, 0.03, 0.02])[0]
        if empty_tables:
            to_fill = random.sample(empty_tables, min(fill_n,
                                                      len(empty_tables)))
            for tbl in to_fill:
                seats_to_fill = random.randint(1, 4)
                cols = random.sample(range(4), seats_to_fill)
                block[tbl, :] = 0
                for c in cols:
                    block[tbl, c] = 1

        # free 0–2 occupied tables with weighted probability
        occupied_any = [idx for idx, row in enumerate(block) if row.sum() > 0]
        free_n = random.choices([0, 1, 2, 3, 4],
                                weights=[0.7, 0.1, 0.05, 0.03, 0.02])[0]
        if occupied_any:
            to_free = random.sample(occupied_any, min(free_n,
                                                      len(occupied_any)))
            for tbl in to_free:
                block[tbl, :] = 0

    stats = compute_table_stats(block_array)
    mensa_data["block_list"] = block_array
    mensa_data["free_tables"] = stats["free_tables"]
    mensa_data["free_seats"] = stats["free_seats"]
    mensa_data["pct_free_seats"] = stats["pct_free_seats"]

    return mensa_data
