import os

# ------------------------------ getting failed properties number ------------------------------
failed_properties_file = "../Shayan_out/Arbiter_failed_properties.txt"
Arbiter_properties_sva = '../properties_sva/Arbiter_properties.sva'
temp_file = "../properties_sva/temp.txt"
string_to_delete = ['failed_properties_list = [ ', ' ]', ' ', '\n']


# function to clean "Arbiter_failed_properties.txt" report and extract failed properties number
def delete_words(i_file, o_file, string):
    with open(i_file, "r") as inp_file:
        with open(o_file, "w") as output_file:
            for lines in inp_file:
                for w in string:
                    lines = lines.replace(w, "")
                output_file.write(lines)
        inp_file.close()
        output_file.close()


# delete 'failed_properties_list = [ ', ' ]', ' ', '\n' from "Arbiter_failed_properties.txt"
delete_words(failed_properties_file, temp_file, string_to_delete)

os.replace(temp_file, failed_properties_file)

f = open(failed_properties_file)
failed_list = (f.read().split(','))
f.close()


# -------------------------------------------------------------------------------------------------
# function to insert '//' at the beginning of the failed property line

def add_text_to_beginning_of_the_line(source_text, searched_word, added_word, added_word_index):
    with open(source_text, 'r') as input_file:
        lines = []
        for line in input_file:
            if searched_word in line:
                split_line = line.split()
                split_line.insert(added_word_index, added_word)
                lines.append(' '.join(split_line) + '\n')
            else:
                lines.append(line)

    with open(temp_file, 'w') as f:
        for line in lines:
            f.write(line)
        f.close()
    os.replace(temp_file, Arbiter_properties_sva)


# -------------------------------------------------------------------------------------
words = ['property Arbiter_property_', 'property Arbiter_sequence_antecedent_',
         'property Arbiter_sequence_consequence_']
covers = ['Arbiter_assertion_', 'Arbiter_00_cover_', 'Arbiter_01_cover_', 'Arbiter_10_cover_', 'Arbiter_11_cover_']

for word in words:
    for number in failed_list:
        add_text_to_beginning_of_the_line(Arbiter_properties_sva, word + str(number) + ';', "//", 0)

for cover in covers:
    for number in failed_list:
        add_text_to_beginning_of_the_line(Arbiter_properties_sva, cover + str(number) + ' :', "//", 0)
