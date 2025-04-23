# Note:
# The full original code in this single file is not publicly shared to protect intellectual property rights for potential commercial applications. It could be provided upon request via email (yiweihou233@gmail.com).
# For design insights, please refer to the paper (*Preventing Disruption of System Backup Against Ransomware Attacks*, ISSTA'25).
# Except for this script, all the other parts are publicly available in this repository.

import json
import argparse
import time


def process_json_object(json_object, cmds, line_number, filename):
    header = json_object.get("header", {})
    properties = json_object.get("properties", {})
    
    if header.get("provider_name") == "MSNT_SystemTrace" and header.get("task_name") == "Process":
        command_line = properties.get("CommandLine")
        if command_line and any(cmd in command_line for cmd in cmds):
            print(f"[A] Native Living-off-the-land Binaries: Suspicious Ransomware Detected!")
            print(f"In {filename} #{line_number}: {command_line}\n")
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor the collected ETW events and defend VSC deletions.")
    parser.add_argument("data_file", help="Path to the structured ETW events file")
    args = parser.parse_args()
    
    with open("cmds_native_living_off_the_land_binaries.txt", "r") as file:
        cmds = [line.strip() for line in file if line.strip()]
        # print(cmds)

    file_offset = 0
    try:
        with open(args.data_file, "r") as f:
            while True:
                f.seek(file_offset)
                line_number = 0
                for line in f:
                    line_number += 1
                    if line.strip():
                        try:
                            json_object = json.loads(line)
                            process_json_object(json_object, cmds, line_number, args.data_file)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON from line #{line_number} in {args.data_file}.")
                            print(f"Line content: {line}")
                            print(f"Error: {e}")
                
                file_offset = f.tell()
                time.sleep(1)
    except FileNotFoundError:
        print(f"Error: The file '{args.data_file}' does not exist.")
    except KeyboardInterrupt:
        print("\nRemembrall stopped.")
