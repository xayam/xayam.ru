import json


def load_config(config_json: str):
    with open(config_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_list(template, config, what):
    begin_end = {
        'css': ['<style>', '</style>'],
        'js': ['<script type="text/javascript">', '</script>'],
        'board': ['', ''],
    }
    result = begin_end[what][0] + '\n'
    for c in config[what]:
        try:
            with open(c, mode='r', encoding='utf-8') as f:
                result += f.read() + '\n\n'
        except FileNotFoundError:
            print(f"ERROR! File {c} not exists!")
    result += '\n' + begin_end[what][1] + '\n\n'
    result = template.replace('{{{' + what + '}}}', result, 1)
    return result

def build(config):
    with open(config['input'], mode='r', encoding='utf-8') as f:
        template = f.read()

    result = read_list(template, config, 'css')
    result = read_list(result, config, 'js')

    with open(config['output'], mode='w', encoding='utf-8') as f:
        f.write(result)

def main():
    build(config=load_config('config.json'))

if __name__ == '__main__':
    main()
