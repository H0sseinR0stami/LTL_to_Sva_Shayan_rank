import os
import shutil
from replace_text import replace_text
from ltl_parser import generate_prop_dictionary_sva_from_ltl
from shayan_input_gen import *

# path
Arbiter_properties_text_path = '../properties_sva/Arbiter-properties.txt'
Arbiter_properties_sva_path = '../properties_sva/Arbiter_properties.sva'
LTL_properties_path = '../properties_ltl/properties.txt'

# clearing
if os.path.exists(Arbiter_properties_text_path):
    os.remove(Arbiter_properties_text_path)
if os.path.exists('../properties_sva/Arbiter_properties.sva'):
    os.remove('../properties_sva/Arbiter_properties.sva')
if os.path.exists('../sim/input_shayan_Arbiter'):
    os.remove('../sim/input_shayan_Arbiter')
if os.path.exists('../sim/Arbiter_failed_properties.txt'):
    os.remove('../sim/Arbiter_failed_properties.txt')
if os.path.exists('../sim/Arbiter_cover_report_req_grant_check.txt'):
    os.remove('../sim/Arbiter_cover_report_req_grant_check.txt')
if os.path.exists("../Shayan/input_shayan_Arbiter"):
    os.remove('../Shayan/input_shayan_Arbiter')
if os.path.exists("../Shayan_out/Arbiter_failed_properties.txt"):
    os.remove("../Shayan_out/Arbiter_failed_properties.txt")
if os.path.exists("../Shayan_out/output_shayan_Arbiter"):
    os.remove("../Shayan_out/output_shayan_Arbiter")


# creating necessary folders'
if not os.path.exists('../properties_sva'):
    os.makedirs('../properties_sva')

if not os.path.exists('../Shayan_out'):
    os.makedirs('../Shayan_out')

shutil.copy(LTL_properties_path, Arbiter_properties_text_path)

# replacing "Grant" with "grant
replace_text(Arbiter_properties_text_path, 'Grant', 'grant')

# generating SVA from LTL
generate_prop_dictionary_sva_from_ltl(Arbiter_properties_text_path)
os.remove('Arbiter_properties_LTL.txt')
os.remove(Arbiter_properties_text_path)
shutil.move('Arbiter_properties.sva', '../properties_sva')

# replacing "grant" with "Grant
replace_text(Arbiter_properties_sva_path, 'grant', 'Grant')

# compiling RTL design with SVA properties
exec(open("compiler.py").read())

# generating shayan input gen
prop_max_num = (prop_count("../sim/Arbiter_cover_report_req_grant_check.txt"))
generate_shayan_input_from_coverage_report("../sim/Arbiter_cover_report_req_grant_check.txt", prop_max_num)

# moving the results
shutil.move("../sim/input_shayan_Arbiter", '../Shayan')
shutil.move("../sim/Arbiter_failed_properties.txt", '../Shayan_out')

# run Shayan app to rank assertions
exec(open("../scripts/shayan_output_gen.py").read())
shutil.move("./output_shayan_Arbiter", '../Shayan_out')
os.remove("./input_shayan_Arbiter")

exec(open("../scripts/sva_handle.py").read())

# clearing
if os.path.exists(Arbiter_properties_text_path):
    os.remove(Arbiter_properties_text_path)

if os.path.exists('../sim/input_shayan_Arbiter'):
    os.remove('../sim/input_shayan_Arbiter')
if os.path.exists('../sim/Arbiter_failed_properties.txt'):
    os.remove('../sim/Arbiter_failed_properties.txt')
if os.path.exists('../sim/Arbiter_cover_report_req_grant_check.txt'):
    os.remove('../sim/Arbiter_cover_report_req_grant_check.txt')
if os.path.exists("../Shayan/input_shayan_Arbiter"):
    os.remove('../Shayan/input_shayan_Arbiter')
if os.path.exists("../Shayan_out/Arbiter_failed_properties.txt"):
    os.remove("../Shayan_out/Arbiter_failed_properties.txt")
if os.path.exists("../Shayan_out/output_shayan_Arbiter"):
    os.remove("../Shayan_out/output_shayan_Arbiter")

# compiling RTL design with SVA properties
exec(open("../scripts/compiler.py").read())

# generating shayan input gen
prop_max_num = (prop_count("../sim/Arbiter_cover_report_req_grant_check.txt"))
generate_shayan_input_from_coverage_report("../sim/Arbiter_cover_report_req_grant_check.txt", prop_max_num)

# moving the results
shutil.move("../sim/input_shayan_Arbiter", '../Shayan')
shutil.move("../sim/Arbiter_failed_properties.txt", '../Shayan_out')

# run Shayan app to rank assertions
exec(open("../scripts/shayan_output_gen.py").read())
shutil.move("./output_shayan_Arbiter", '../Shayan_out')
