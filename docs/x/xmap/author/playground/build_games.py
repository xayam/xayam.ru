import json


def load_config(config_json: str):
    with open(config_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_list(template, config):
    begin_end = {
        'css': ['<style>', '</style>'],
        'js': ['<script type="text/javascript">', '</script>'],
        'json': ['<script type="text/javascript">', '</script>']
    }
    for what in begin_end:
        result = begin_end[what][0] + '\n'
        for c in config[what]:
            try:
                if what == 'json':
                    with open(config[what][c], mode='r', encoding='utf-8') as f:
                        value = f.read()
                        result += 'let ' + c + ' = ' + value + ';\n'
                else:
                    with open(c, mode='r', encoding='utf-8') as f:
                        result += f.read() + '\n\n'
            except FileNotFoundError:
                print(f"ERROR! File {c} not exists!")
        result += '\n' + begin_end[what][1] + '\n\n'
        template = template.replace('{{{' + what + '}}}', result, 1)
    return template

def build(config):
    with open(config['input'], mode='r', encoding='utf-8') as f:
        template = f.read()
    result = read_list(template, config)
    with open(config['output'], mode='w', encoding='utf-8') as f:
        f.write(result)

def main():
    build(config=load_config('config.json'))

if __name__ == '__main__':
    main()
