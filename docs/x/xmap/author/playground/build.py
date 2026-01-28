import json


def load_config(config_json: str):
    with open(config_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_list(template, config):
    begin_end = {
        'css': ['<style>', '</style>'],
        'json': ['<script type="text/javascript">', '</script>'],
        'function': ['<script type="text/javascript">', '</script>'],
        'js': ['<script type="text/javascript">', '</script>'],
    }
    for what in begin_end:
        result = ''
        for c in config[what]:
            try:
                result += begin_end[what][0] + '\n'
                if what in ['json', 'function']:
                    with open(config[what][c], mode='r', encoding='utf-8') as f:
                        value = f.read()
                    if what == 'json':
                        result += 'let ' + c + ' = ' + value + ';\n\n'
                    else:
                        result += 'function ' + c + '() {\n' + value + '\n};\n\n'
                else:
                    with open(c, mode='r', encoding='utf-8') as f:
                        result += f.read() + '\n\n'
            except FileNotFoundError:
                print(f"ERROR! File {c} not exists!")
            finally:
                result += '\n' + begin_end[what][1] + '\n\n'
        template = template.replace('{{{' + what + '}}}', result, 1)
    return template

def build_app(config):
    with open(config['input'], mode='r', encoding='utf-8') as f:
        template = f.read()
    result = read_list(template, config)
    with open(config['output'], mode='w', encoding='utf-8') as f:
        f.write(result)

def main():
    configs = ['games_config.json', ]
    for config in configs:
        build_app(config=load_config(config))

if __name__ == '__main__':
    main()
