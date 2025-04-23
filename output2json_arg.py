# Remembrall_generator.exe saves output as just a sudo-json file, so this script will convert the file to a structured json file
import argparse
import json


def main():
    parser = argparse.ArgumentParser("Parse the original collected data to a structured JSON file.")
    parser.add_argument("origin_file", help="Path to the original file")
    parser.add_argument("structured_file", help="Path to the structured JSON file output")
    args = parser.parse_args()
    with open(args.origin_file, "r") as f:
        text = f.read()

    # save the data to a new file with JSON array format containing all the JSON objects
    with open(args.structured_file, "w") as outfile:
        outfile.write("[\n")
        lines = [line for line in text.split("\n") if line.strip() != ""]
        for i, line in enumerate(lines):
            j = json.loads(line)
            outfile.write(json.dumps(j, indent=4))
            if i != len(lines) - 1:  # add a comma if it's not the last line
                outfile.write(",\n")
            else:
                outfile.write("\n")
        outfile.write("]\n")

if __name__ == "__main__":
    main()


# # without args as input, the file path is hardcoded
# import json
# events = list()

# file_path = "C:/Users/User/Desktop/output-file-test.json"

# with open(file_path, "r") as f:
#     for line in f:
#         events.append(json.loads(line))

# for event in events:
#     print(json.dumps(event, indent=4))
