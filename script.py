import re
import os

regex = r"(\{.*\})"

if_tags = {
    "and": "and",
    "or": "or"
}

if_tags_conditions = {
    "eq": "===",
    "bt": ">=",
    "lt": "<="
}

close_tags = {
    "{/if}": "{% endif %}",
    "{/foreach}": "{% endfor %}",
    "{else}": "{% else %}",
    "{foreachelse}": "{% else %}",
    "{/block}": "{% endblock %}",
}

generic_tags = {
    "block": "{%block %% %}"
}


def find_block_tag(filetext):
    regex_block = r"\{block\s*?name=\"(.*)\"\s*?\}"
    matches = re.finditer(regex_block, filetext, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        matched_text = match.group(1)
        # print(matched_text)
        filetext = filetext.replace(match.group(), "{{% block {text} %}}".format(text = matched_text))

    return filetext


for file in os.listdir('files/'):
    filename = file.replace(".tpl", ".twig")
    test_str = open("files/"+file)
    file_str = test_str.read()
    matches = re.finditer(regex, file_str, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        match = match.group()
        if match in close_tags.keys():
            file_str = file_str.replace(match, close_tags[match])

    file_str = find_block_tag(file_str)

    new = open("formated/"+filename, 'x')
    new.write(file_str)
