import json


def load_config(config_json: str):
    with open(config_json, "r", encoding="utf-8") as f:
        return json.load(f)

def read_list(input_list: list, begin: str, end: str):
    result = begin + "\n"
    for c in input_list:
        try:
            with open(c, mode="r", encoding="utf-8") as f:
                result += f.read() + "\n\n"
        except FileNotFoundError:
            print(f"ERROR! File {c} not exists!")
    return result + "\n" + end

def build(config):
    with open(config["input"], mode="r", encoding="utf-8") as f:
        template = f.read()

    result = read_list(config["css"], "<style>", "</style>")
    template = template.replace("{{{STYLES}}}", result, 1)

    result = read_list(config["js"], '<script type="text/javascript">', "</script>")
    template = template.replace("{{{SCRIPTS}}}", result, 1)

    with open(config["output"], mode="w", encoding="utf-8") as f:
        f.write(template)

def main():
    build(config=load_config("config.json"))

if __name__ == "__main__":
    main()
