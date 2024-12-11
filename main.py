import os
import datetime
import pathlib
import time
import json


def print_color(r, g, b, text):
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(
        r, g, b, text))


with open("config.json") as config_file:
    config = json.loads(config_file.read())

start_path = config["start_path"]
min_inactive_time_in_seconds = config["min_inactive_time_in_seconds"]
dirctories_to_exclude = config["dirctories_to_exclude"]
min_file_size = config["min_file_size"]
print_every_iteration = config["print_every_iteration"]
output_file_path = config["output_file_path"]


def is_excluded(file_path, dirctories_to_exclude):
    for dirctorie_to_exclude in dirctories_to_exclude:
        if file_path.startswith(dirctorie_to_exclude):
            return True
    return False


def show_all_files():
    total_size = 0
    output_file = open(output_file_path, "w")
    for i, file in enumerate(pathlib.Path(start_path).rglob("*")):
        try:
            if is_excluded(file.parent.as_posix(), dirctories_to_exclude):
                continue
            if i % print_every_iteration == 0:
                print(i, file)
            if file.is_file():
                try:
                    time_last_access = datetime.datetime.fromtimestamp(
                        os.path.getatime(file))
                except Exception as e:
                    print_color(255, 0, 0, e)
                    continue
                time_inactive = datetime.datetime.fromtimestamp(
                    time.time()) - time_last_access
                if time_inactive.total_seconds() > min_inactive_time_in_seconds and file.stat().st_size > min_file_size:
                    print(file, time_last_access, "inactive for:", end=' ')
                    print_color(255, 0, 0, f" {
                                time_inactive.total_seconds() / 3600} hours size:{file.stat().st_size / 1_000_000} MB")
                    output_file.write(
                        f"{file} - {time_inactive.total_seconds() / 3600} - {file.stat().st_size / 1_000_000} MB\n")
                    total_size += os.path.getsize(file)
        except Exception as e:
            print_color(255, 0, 0, e)
            continue
    output_file.close()
    print("total memory that can be clear:", total_size / (1024 * 1024), "mb")


if __name__ == "__main__":
    show_all_files()
