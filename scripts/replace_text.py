import fileinput


def replace_text(text_file_path, text_to_search, replacement_text):

    with fileinput.FileInput(text_file_path, inplace=True) as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')
