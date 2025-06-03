# test/test_api.py

import time

import requests


def fetch_mensa_data():
    url = 'http://localhost:8000/api/Mensa%20Roma%20Tre/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Print summary line
            print(f"Queue Length: {data['queue_len']}\t"
                  f"Wait Time: {data['wait_time']} sec\t"
                  f"Free Tables: {data['free_tables']}\t"
                  f"Free Seats: {data['free_seats']}\t"
                  f"Pct Free Seats: {data['pct_free_seats']}%")

            blocks = data['block_list']
            block_nbr = len(blocks)

            # Header: Block numbers as column titles
            header = ["Table#"]
            for b in range(block_nbr):
                header.append(f"Block {b+1}")
            print("\t".join(header))

            # For each table index (0 to 9), print that row for all blocks
            for table_index in range(10):
                row = [f"{table_index+1:2d}"]  # table number
                for b in range(block_nbr):
                    table = blocks[b][table_index]  # list of 4 seats
                    # Represent seats as X=occupied, O=free, joined without spaces
                    seats = "".join("X" if s == 1 else "O" for s in table)
                    row.append(seats)
                print("\t".join(row))

            print("\n" + "-" * 80 + "\n")
        else:
            print(f"Error: Status Code {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    i = 0
    while True:
        print(f"Fetch iteration: {i}")
        i += 1
        fetch_mensa_data()
        time.sleep(1)
