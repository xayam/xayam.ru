import re
import json
import sys


class Builder:

    def __init__(self, name: str):
        self.name = name
        self.config_json = f"{self.name}.json"
        self.template_html = f"{self.name}/template.html"
        self.config = None
        self.outputs = None
        self.input = None
        self.template = None
        self.init()

    def init(self):
        with open(self.config_json, 'r', encoding='utf-8') as f:
            config_json = json.load(f)
        self.config = config_json['config']
        config_json.pop('config', None)
        self.outputs = config_json['outputs']
        config_json.pop('outputs', None)
        self.input = config_json
        with open(self.template_html, mode='r', encoding='utf-8') as f:
            self.template = f.read()

    def run(self):
        self.render()

    def render(self):
        n = 1
        for match in self.input:
            for tasks in self.input[match]:
                task_matches = re.findall(r"\{[\+\-]+\}", tasks)[0][1:-1]
                task_names = re.findall(r"\{[a-zA-z0-9_]*\}", tasks)
                if task_names:
                    task_names = task_names[0]
                else:
                    task_names = ''
                for task in task_matches:
                    paths = self.input[match][tasks]
                    result = ''
                    begin = self.config['{' + task + '}{' + match + '}'][0] + '\n'
                    end = '\n' + self.config['{' + task + '}{' + match + '}'][1] + '\n\n'
                    path_list = []
                    for path in paths:
                        if task == '-':
                            p = './' + path[len(self.name) + 1:]
                            begin2 = begin.replace("{@href_style}", "href='" + p + "'")
                            begin2 = begin2.replace("{@src_script}", "src='" + p + "'")
                            begin2 = begin2.replace("{@src_image}", "src='" + p + "'")
                            result += begin2
                            result += end
                            # self.save(result, n, task, match)
                        elif task == '+':
                            if not path.endswith('.png'):
                                with open(path, mode='r', encoding='utf-8') as f:
                                    path_list.append((path, f.read()))
                            else:
                                with open(path, mode='rb') as f:
                                    p = "data/png:" + f.read().decode()
                                    path_list.append((p, ''))
                    for path, content in path_list:
                        begin2 = begin.replace("{@src_image}", "src='" + path + "'")
                        result += begin2
                        result += content
                        result += end
                    n = self.save(result, n, task, match)

    def save(self, result, n, task, match):
        self.template = self.template.replace(
            self.config["decorate"][0] + match + self.config["decorate"][1],
            result,
            1
        )
        for output in self.outputs['{' + task + '}']:
            out = self.config['root'] + output.replace('{@number}', str(n))
            with open(out, mode='w', encoding='utf-8') as f:
                if n == 6:
                    t1 = "".join([f"\\{k}" for k in self.config["decorate"][0]])
                    t2 = self.config["temp"][0]
                    t3 = self.config["temp"][1]
                    t4 = "".join([f"\\{k}" for k in self.config["decorate"][1]])
                    te = t1 + t2 + t4 + '.+?' + t1 + t3 + t4
                    self.template = re.sub(
                        te,'', self.template, 1,
                        flags=re.MULTILINE | re.UNICODE | re.DOTALL
                    )
                f.write(self.template)
        return n + 1
