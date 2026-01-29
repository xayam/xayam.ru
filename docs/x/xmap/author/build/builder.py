import json

class Builder:

    def __init__(self, name: str):
        self.name = name
        self.config_filename = f"build/{self.name}.json"
        self.template_filename = f"{self.name}/template.html"
        self.config = None
        self.template = None
        self.decorations = {
            'style': ['<style>', '</style>'],
            'javascript': ['<script type="text/javascript">', '</script>']
        }
        self.schemes = {
            'style': ['css'],
            'javascript': ['json', 'function', 'js']
        }
        self.init()

    def init(self):
        with open(self.config_filename, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        with open(self.template_filename, mode='r', encoding='utf-8') as f:
            self.template = f.read()

    def run(self):
        rendered = self.render()
        for output in self.config["outputs"]:
            with open(output, mode='w', encoding='utf-8') as f:
                f.write(rendered)

    def render(self):
        for s in self.schemes:
            for t in self.schemes[s]:
                temp = self.decorations[s][0] + '\n'
                for c in self.config[t]:
                    temp = self.process(temp, t, c)
                temp += '\n' + self.decorations[s][1] + '\n\n'
                self.template = self.template.replace('<!--{{{' + t + '}}}-->', temp, 1)
        return self.template

    def process(self, temp: str, what: str, c: str):
        try:
            if what in ['json', 'function']:
                with open(f"{self.name}/{self.config[what][c]}", mode='r', encoding='utf-8') as f:
                    value = f.read()
                if what == 'json':
                    temp += 'let ' + c + ' = ' + value + ';\n\n'
                else:
                    temp += 'function ' + c + '() {\n' + value + '\n};\n\n'
            else:
                with open(f"{self.name}/{c}", mode='r', encoding='utf-8') as f:
                    temp += f.read() + '\n\n'
        except FileNotFoundError:
            print(f"[WARNING] File {c} not exists!")
        return temp
