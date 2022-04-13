import re, os
import sys

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

def find_extend_tag(filetext):
    regex_block = r"\{extends\s*?file=\"(.*)\"\s*?\}"
    matches = re.finditer(regex_block, filetext, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        matched_text = match.group(1)

        filetext = filetext.replace(match.group(), "{{% extends \"{text}\" %}}".format(text = matched_text))

    return filetext

def find_foreach_tag(filetext):
    regex_block = r"({foreach(.*)})"
    matches = re.finditer(regex_block, filetext, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        matched_text = match.group(2)
        matched_text_all = match.group(1)

        array = ""
        key = ""
        item = ""

        #match the from
        regex_block_from = r"from=([\$a-z0-9\.\_\[\]\'\"]*)"
        matches_from = re.finditer(regex_block_from, matched_text)

        for matchNum, match in enumerate(matches_from, start=1):
            matched_text_from = match.group(1)
            array = matched_text_from

        #match key
        regex_block_key = r"key=([a-z\_]*)"
        matches_key = re.finditer(regex_block_key, matched_text)

        for matchNum, match in enumerate(matches_key, start=1):
            matched_text_key = match.group(1)
            key = matched_text_key

        #match item
        regex_block_item = r"item=([a-z\_]*)"
        matches_item = re.finditer(regex_block_item, matched_text)

        for matchNum, match in enumerate(matches_item, start=1):
            matched_text_item = match.group(1)
            item = matched_text_item

        array = array.replace("$", "")
        forLoop = "{{% for {} in {} %}}".format(item,array)
        
        if key:
            forLoop = "{{% for {},{} in {} %}}".format(key,item,array)   
        
        filetext = filetext.replace(matched_text_all, forLoop)

    return filetext

def find_if_tag(filetext):
    regex_block = r"({if(.+?)})"
    matches = re.finditer(regex_block, filetext, re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE)

    for matchNum, match in enumerate(matches, start=1):
        matched_text = match.group(2)
        matched_text_all = match.group(1)

        print(matched_text)
        print(matched_text_all)

        regex_if_content = r"{if(.*)}"
        matches_if_content = re.finditer(regex_if_content,matched_text_all,re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE)

        for matchNum, match in enumerate(matches_if_content, start=1):
            matched_if_text = match.group(1)

            matched_if_text = matched_if_text.replace("$", "")

            for twig, smarty in if_tags_conditions:
                if matched_if_text.find(twig):
                    matched_if_text.replace(twig, smarty)

            ifBlock = "{{% if{} %}}".format(matched_if_text)
            filetext = filetext.replace(matched_text_all, ifBlock)

    return filetext

def find_elseif_tag(filetext):
    regex_block = r"({elseif(.+?)})"
    matches = re.finditer(regex_block, filetext, re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE)

    for matchNum, match in enumerate(matches, start=1):
        matched_text = match.group(2)
        matched_text_all = match.group(1)

        regex_if_content = r"{elseif(.*)}"
        matches_if_content = re.finditer(regex_if_content,matched_text_all, re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE)

        for matchNum, match in enumerate(matches_if_content, start=1):
            matched_if_text = match.group(1)

            matched_if_text = matched_if_text.replace("$", "")

            for twig, smarty in if_tags_conditions:
                if matched_if_text.find(twig):
                    matched_if_text.replace(twig, smarty)

            ifBlock = "{{% elseif{} %}}".format(matched_if_text)
            filetext = filetext.replace(matched_text_all, ifBlock)

    return filetext
    
def find_variables_tag(filetext):
    regex_block = r"([\{]{1,2}\$(.*)[\}]{1,2})"
    matches = re.finditer(regex_block, filetext, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        matched_variable = match.group(1)
        matched_variable_content = match.group(2)

        if re.search(r"\*\}", matched_variable):
            continue

        if matched_variable_content.find("}"):
            matched_variable_content = matched_variable_content.replace("}", "")

        new_var = "{{ %s }}" % matched_variable_content

        filetext = filetext.replace(matched_variable, new_var)
        
        
    return filetext

# for file in os.listdir('files/'):
#     if not file.startswith('.'):
#         print(file)
        # filename = file.replace(".tpl", ".twig")
        # test_str = open("files/"+file)
        # file_str = test_str.read()
        # regex = r"(\{.*\})"
        # matches = re.finditer(regex, file_str, re.MULTILINE)

        # for matchNum, match in enumerate(matches, start=1):
        #     match = match.group()
        #     if match in close_tags.keys():
        #         file_str = file_str.replace(match, close_tags[match])

        # file_str = find_block_tag(file_str)
        # file_str = find_extend_tag(file_str)
        # file_str = find_foreach_tag(file_str)
        # file_str = find_if_tag(file_str)
        # file_str = find_elseif_tag(file_str)
        # file_str = find_variables_tag(file_str)

        # new = open("formated/"+filename, 'w+')
        # new.write(file_str)

walk_dir = './files'

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    print('--\nroot = ' + root)
    list_file_path = os.path.join(root, 'my-directory-list.txt')
    print('list_file_path = ' + list_file_path)

    with open(list_file_path, 'wb') as list_file:
        for subdir in subdirs:
            print('\t- subdirectory ' + subdir)

        for filename in files:
            file_path = os.path.join(root, filename)

            print('\t- file %s (full path: %s)' % (filename, file_path))

            with open(file_path, 'rb') as f:
                f_content = f.read()
                # list_file.write(('The file %s contains:\n' % filename).encode('utf-8'))
                # list_file.write(f_content)
                # list_file.write(b'\n')