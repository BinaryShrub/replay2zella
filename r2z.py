#!/usr/bin/env python3
import csv
import datetime
import sys

symbol = "MNQ"
commission = 0.5
fees = 0.37

def epoch(date_str):
    date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    return int(date.timestamp())

def get_expiration(date_str):
    # Contract Switch Date to Contract Expiration
    switch_date_to_expiration = {
        "06/18/2019": "SEP 2019",
        "09/17/2019": "DEC 2019",
        "12/17/2019": "MAR 2020",
        "03/17/2020": "JUN 2020",

        "06/16/2020": "SEP 2020",
        "09/15/2020": "DEC 2020",
        "12/15/2020": "MAR 2021",
        "03/16/2021": "JUN 2021",

        "06/15/2021": "SEP 2021",
        "09/14/2021": "DEC 2021",
        "12/14/2021": "MAR 2022",
        "03/15/2022": "JUN 2022",

        "06/14/2022": "SEP 2022",
        "09/13/2022": "DEC 2022",
        "12/13/2022": "MAR 2023",
        "03/14/2023": "JUN 2023",

        "06/13/2023": "SEP 2023",
        "09/12/2023": "DEC 2023",
        "12/12/2023": "MAR 2024",
        "03/12/2024": "JUN 2024",

        "06/17/2024": "SEP 2024",
        "09/17/2024": "DEC 2024",
        "12/17/2025": "MAR 2025",
    }

    expiration = "NO_EXP"
    date = epoch(date_str)
    for switch_date_str, expiration_str in switch_date_to_expiration.items():
        switch_date = epoch(switch_date_str)
        if date < switch_date:
            expiration = expiration_str
            break
    
    if expiration == "NO_EXP":
        raise ValueError("No expiration found for the given date")

    return expiration

def main(input):
    with open(input, 'r') as infile, open(f"{input[:-4]}_tradezella.csv", 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        next(reader)  # Skip the header row

        writer.writerow(["Date", "Time", "Symbol", "Buy/Sell", "Quantity", "Price", "Spread", "Expiration", "Strike", "Call/Put", "Commission", "Fees"])

        for row in reader:
            signal, date_time, price, contract_count = row[2], row[3], row[4], row[5]
            buy_sell = signal.split()[0]

            date, time = date_time.split()
            time = f"{time}:00"

            year, month, day = date.split('-')
            date = f"{month}/{day}/{year}"

            expiration = get_expiration(date)

            writer.writerow([date, time, symbol, buy_sell, contract_count, price, "Future", expiration, "", "", commission, fees])

if __name__ == "__main__":
    main(sys.argv[1])