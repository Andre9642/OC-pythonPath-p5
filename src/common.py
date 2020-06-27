import json

ERR_UNKNOWN_ID_API = -1


def write_in_file(data, filename="json_extract.txt"):
    with open(filename, "wb") as handle:
        for e in data:
            handle.write((str(e) + "\n").encode())


def write_json_in_file(self, json_):
    with open("out.txt", "w") as handle:
        handle.write(json.dumps(json_, indent=4, sort_keys=True))
