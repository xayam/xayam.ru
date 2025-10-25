import datetime
import os

def find_files_os_walk(start_dir, filename_pattern):
    found_files = []
    with open("template.htaccess", mode="r") as f:
        template_htaccess = f.read()
    for root, _, files in os.walk(start_dir):
        for filename in files:
            if filename_pattern in filename:
                path_filename = os.path.join(root, filename).replace("\\", "/")
                with open(path_filename, mode="r") as f:
                    current_htaccess = f.read()
                if current_htaccess == template_htaccess:
                    found_files.append(path_filename)
    return found_files

def main():
    files = find_files_os_walk('../docs', '.htaccess')
    parent_folders = set()
    for filename in files:
        folder = "/".join(filename.split("/")[2:-1])
        if folder:
            parent_folders.add(folder)
    parent_folders = list(parent_folders)
    files = []
    for current_folder in parent_folders:
        for name in os.listdir("../docs/" + current_folder):
            if name != ".htaccess":
                files.append({
                    "current_folder": current_folder,
                    "isdir": os.path.isdir("../docs/" + current_folder + "/" + name),
                    "name": name,
                    "parent_folder": "/".join(current_folder.split("/")[:-1]),
                    "size": os.stat("../docs/" + current_folder + "/" + name).st_size,
                    "modified": str(datetime.datetime.fromtimestamp(os.path.getmtime(
                        "../docs/" + current_folder + "/" + name
                    ))).split(".")[0].rjust(27, "_").replace("_", "&nbsp;")
                })
    files.sort(key=lambda item: (item["current_folder"], -item["isdir"], item["name"]))
    for index in range(len(files)):
        size = files[index]["size"]
        if size > 2 ** 30:
            files[index]["size"] = f"{size / 2 ** 30:.2f} GB"
        elif size > 2 ** 20:
            files[index]["size"] = f"{size / 2 ** 20:.2f} MB"
        elif size > 2 ** 10:
            files[index]["size"] = f"{size / 2 ** 10:.2f} KB"
        else:
            files[index]["size"] = f"{size}__B"
        files[index]["size"] = str(files[index]["size"]).rjust(27, "_")
        files[index]["size"] = str(files[index]["size"]).replace("_", "&nbsp;")

    with open("template.html", mode="r") as f:
        template_html = f.read()
    pred = 0
    current_files = [files[pred]]
    for index in range(1, len(files)):
        if current_files[-1]["current_folder"] == files[index]["current_folder"]:
            current_files.append(files[index])
        else:
            result = "\n"
            for current in current_files:
                result += "        <tr>\n            <td>"
                if current["isdir"]:
                    index_dir = "/index.html"
                    result += "[DIR ]"
                else:
                    index_dir = ""
                    result += "[FILE]"
                result += " <a href=\"" + current["name"] + index_dir + \
                          "\">" + current["name"]  + "</a></td>\n            <td>"
                result += current["modified"] + "</td>\n            <td>"
                result += current["size"] + "</td>\n"
                result += "        </tr>\n"
            result = result[:-1]
            index_html = template_html.replace(
                "{{{LIST_OF_FOLDERS_AND_FILES}}}", result
            )

            index_html = index_html.replace(
                "{{{CURRENT_CATALOG}}}", current_files[-1]["current_folder"]
            )
            create_html = "../docs/" + current_files[-1]["current_folder"] + "/index.html"
            with open(create_html, encoding="UTF-8", mode="wt") as f:
                f.write(index_html)
                print(create_html)
            current_files = [files[index]]


if __name__ == "__main__":
    main()