#!/usr/bin/env python
# coding=utf-8

import os, sys, csv, json, re

def main():

    inputfile = "data/input.csv"

    # Load input csv file
    if os.path.exists(inputfile):
        try:
            with open(inputfile, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                input_data = list(reader)

        except ValueError as e:
            sys.stderr.write('Error: I got a problem reading your csv. Is it in a good format?\n')
            print(e)
            sys.exit(0)
    else:
        sys.stderr.write("Error: No input csv file found at 'data/input.csv'.\n")
        sys.exit(0)


    output = {"lines": dict()}
    ignore_first_line = True

    # Loop through bus lines
    for i in input_data:

        # Skip first header row
        if ignore_first_line is False:

            # Building the basic structure of the timetable

            output["lines"][i[0]] = list()
            output["lines"][i[0]].append({
                "from": i[1],
                "to": i[2],
                "service": [ "Mo-Fr" ],
                "stations": [i[1], i[2]],
                "times": generate_times(i, "Mo-Fr", 1)
            })
            output["lines"][i[0]].append({
                "from": i[1],
                "to": i[2],
                "service": [ "Sa" ],
                "stations": [i[1], i[2]],
                "times": generate_times(i, "Sa", 1)
            })
            output["lines"][i[0]].append({
                "from": i[1],
                "to": i[2],
                "service": [ "Su" ],
                "stations": [i[1], i[2]],
                "times": generate_times(i, "Su", 1)
            })
            output["lines"][i[0]].append ({
                "from": i[2],
                "to": i[1],
                "service": [ "Mo-Fr" ],
                "stations": [i[2], i[1]],
                "times": generate_times(i, "Mo-Fr", 2)
            })
            output["lines"][i[0]].append({
                "from": i[2],
                "to": i[1],
                "service": [ "Sa" ],
                "stations": [i[2], i[1]],
                "times": generate_times(i, "Sa", 2)
            })
            output["lines"][i[0]].append({
                "from": i[2],
                "to": i[1],
                "service": [ "Su" ],
                "stations": [i[2], i[1]],
                "times": generate_times(i, "Su", 2)
            })
        ignore_first_line = False


    # Write output json file
    with open('data/output.json', 'w', encoding='utf8') as outfile:
        json.dump(output, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    # End program
    sys.exit()


def generate_times(data, service, direction):

    # Prepare schedule
    opening_hours = data[2+direction].split(";")
    operation_schedule = {}

    for i, d in enumerate(opening_hours):

        # Clean leading space (if there)
        opening_hours[i] = re.sub(r"^\s+" , "" , d)

        # Convert into understandable service schedules
        opening_hours[i] = dict(opening_hours[i].split(" ") for s in opening_hours[i])
        key, value = opening_hours[i].popitem()
        operation_schedule[key] = value

    data_index = int()
    schedule = dict()
    times = list()
    duration = int(data[5])

    if service == "Mo-Fr":
        data_index = 6
    elif service == "Sa":
        data_index = 13
    elif service == "Su":
        data_index = 20
    else:
        sys.stderr.write("Error: Can not handle service time " + service + "\n")
        sys.exit(0)

    schedule[6] = data[data_index] #6-7
    schedule[7] = data[data_index+1] #7-9
    schedule[8] = data[data_index+1] #7-9
    schedule[9] = data[data_index+2] #9-16
    schedule[10] = data[data_index+2] #9-16
    schedule[11] = data[data_index+2] #9-16
    schedule[12] = data[data_index+2] #9-16
    schedule[13] = data[data_index+2] #9-16
    schedule[14] = data[data_index+2] #9-16
    schedule[15] = data[data_index+2] #9-16
    schedule[16] = data[data_index+3] #16-18
    schedule[17] = data[data_index+3] #16-18
    schedule[18] = data[data_index+4] #18-19
    schedule[19] = data[data_index+5] #19-20
    schedule[20] = data[data_index+6] #20-21

    schedule_items = schedule.items()
    for item in schedule_items:
        if item[1] is not "0":
            minutes = 60 // int(item[1])

            if minutes == 60:
                times.append(calculate_times(int(item[0]), 15, duration))
            elif minutes == 30:
                times.append(calculate_times(int(item[0]), 15, duration))
                times.append(calculate_times(int(item[0]), 45, duration))
            else:
                next_time = 00
                for n in range(int(item[1]),0,-1):
                    times.append(calculate_times(int(item[0]), next_time, duration))
                    next_time = next_time + minutes

    return times

def calculate_times(hour, start_time, duration):

    calculated_time = list()
    end_time = start_time + duration

    if start_time < 10:
        start_time = "0" + str(start_time)
    else:
        start_time = str(start_time)

    calculated_time.append(str(hour) + ":" + start_time)

    # Calculate end_time
    if end_time >= 60:
        hour = hour + int(end_time/60)
        end_time = end_time%60

    if end_time < 10:
        end_time = "0" + str(end_time)
    else:
        end_time = str(end_time)

    calculated_time.append(str(hour) + ":" + end_time)

    return calculated_time


if __name__ == "__main__":
    main()
