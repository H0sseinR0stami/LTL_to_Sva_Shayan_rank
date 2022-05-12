from math import log
import sys


def clean_string(line_string):
    new_string = ""
    for char in line_string:
        if char != "(" and char != ")" and char != "\n" and char != "\r" and char != " ":
            new_string += char
    return new_string


def generate_prop_dictionary_sva_from_ltl(prop_file_name):
    if not isinstance(prop_file_name, str):
        raise ValueError(prop_file_name + "is not a string!")

    # save prints out puts to txt file
    sys.stdout = open("Arbiter_properties.sva", "w")

    print("// -----------------------------------------------------")
    print(" ")

    prop_file = open(prop_file_name, 'r')

    # -------------------------------------------------------------------------------------
    # Count number of non-empty lines of property file
    file = open(prop_file_name, "r")
    nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
    line_count = len(nonempty_lines)
    prop_file.close()
    # -------------------------------------------------------------------------------------

    prop_file = open(prop_file_name, 'r')

    dut_name = "Arbiter"

    original_prop_file = open(dut_name + "_properties_LTL.txt", 'w')

    counter = 0
    prop_dict = {}
    prop_cond_dict = {}
    seq_cond_dict = {}
    prop_symp_dict = {}
    seq_symp_dict = {}
    properties_with_until_list = []
    line_number = 1

    for line in prop_file:
        prop = ""
        prop_cond = ""
        prop_symp = ""
        seq_cond = ""
        seq_symp = ""
        original_ltl_property = line

        # Ignore the first G character in property, as the SVA will have an always in the beginning!
        line = line[1:]

        for item in line:
            if item == "=":
                prop += "=="
            elif item == "G":
                prop += "always[0:$]"
            elif item == "F":
                prop += "s_eventually[0:$]"
            elif item == "X":
                prop += "nexttime[1]"
            elif item == "U":
                prop += "until"
            elif item == "+":
                prop += "||"
            elif item == "&":
                prop += "&&"
            elif item == "\n":
                pass;
            elif item == "<" and line[line.index(item) + 2] == ">":
                prop += "["
            elif item == ">" and line[line.index(item) - 2] == "<":
                prop += "]"

            else:
                prop += item
        # Correcting possible mistakes!
        if "->" in prop:
            prop = prop[:prop.index("->")] + "|->" + prop[prop.index("->") + 2:]
        if "-]" in prop:
            prop = prop[:prop.index("-]")] + "|->" + prop[prop.index("-]") + 2:]
        if ">==" in prop:
            prop = prop[:prop.index(">==")] + "]==" + prop[prop.index(">==") + 3:]
        if ">==" in prop:
            prop = prop[:prop.index(">==")] + "]==" + prop[prop.index(">==") + 3:]

        # Separate antecedent and consequence
        if "|->" in prop:
            prop_cond = prop[:prop.index("|->")] + " ) ) "
            prop_symp = " ( ( " + prop[prop.index("|->") + 3:]

        # if antecedent as rst==1 checking, all output ports should be checked for unknown 'X' value(s) !!
        if "rst==1" in prop_cond:
            if prop_cond[prop_cond.index("rst==1") - 3:prop_cond.index("rst==1") - 2] != "!":
                seq_cond += prop_cond[:prop_cond.index("rst==1")] + "rst==1"

                if dut_name == "Arbiter":
                    # Arbiter output(s) : nextstate (6 bits, shows Arbitr state(s))
                    if "nextstate" in prop_symp:
                        seq_cond += " && (!$isunknown(nextstate)) "
                seq_cond += prop_cond[prop_cond.index("rst==1") + 6:]
            else:
                seq_cond = prop_cond
        else:
            seq_cond = prop_cond

        prop_dict[counter] = prop
        prop_cond_dict[counter] = prop_cond
        seq_cond_dict[counter] = seq_cond
        prop_symp_dict[counter] = prop_symp

        # To be removed later !!
        # if ("until" in prop_cond) or ("until" in prop_symp):
        if "until" in prop_cond:  # until in consequence is allowed.
            properties_with_until_list.append(1)
        else:  # For now only print properties with until in consequence!
            properties_with_until_list.append(0)

            # if line_number in failed_properties_list:
            # pass
            # else:
            # original_prop_file.write(original_ltl_property)
            original_prop_file.write(original_ltl_property)

        line_number = line_number + 1

        counter = counter + 1

    print("// List of properties : ")
    print(" ")
    index = 0
    passing_properties_index = 0
    # for key, value in prop_dict.items():
    for key, value in seq_cond_dict.items():
        for key2, value2 in prop_symp_dict.items():
            if key == key2:
                if properties_with_until_list[key] == 0:  # To be removed later !!
                    index = index + 1
                    # print "property " + dut_name + "_property_" + str(key+1) + "; \t" + str(value) + " |-> " + str(
                    # value2) + " ; \t endproperty" do not print failing properties! if index in
                    # failed_properties_list: pass else: passing_properties_index = passing_properties_index + 1
                    print("property " + dut_name + "_property_" + str(index) + "; \t" + str(value) + " implies " + str(
                        value2) + " ; \t endproperty")
                    break
                else:
                    break
    print("// -----------------------------------------------------")
    print(" ")
    index = 0
    passing_properties_index = 0

    print("// List of Assertions : ")
    print(" ")
    for key, value in prop_dict.items():
        for key2, value2 in seq_cond_dict.items():
            if key == key2:
                if properties_with_until_list[key] == 0:  # To be removed later !!
                    index = index + 1

                    # if index in failed_properties_list:
                    # pass
                    # else:
                    # passing_properties_index = passing_properties_index + 1
                    if ("rst" in value2) and ("isunknown" in value2):
                        # print dut_name + "_assertion_" + str(key+1) + " : \t assert  property \t(@ (posedge clk) \t
                        # ( " + dut_name + "_property_" + str(key+1) + " ) ) ; "
                        print(dut_name + "_assertion_" + str(
                            index) + " : \t assert  property \t(@ (posedge clk) \t ( " + dut_name + "_property_" + str(
                            index) + " ) ) ; ")
                        break
                    else:
                        # print dut_name + "_assertion_" + str(key+1) + " : \t assert  property \t(@ (posedge clk)
                        # disable iff (rst) ( " + dut_name + "_property_" + str(key+1) + " ) ) ; "
                        print(dut_name + "_assertion_" + str(
                            index) + " : \t assert  property \t(@ (posedge clk) disable iff (rst) ( " + dut_name + "_property_" + str(
                            index) + " ) ) ; ")
                        break
                else:
                    break

    print("// -----------------------------------------------------")
    print(" ")
    index = 0
    passing_properties_index = 0

    print("// List of antecedents : ")
    print(" ")
    for key, value in seq_cond_dict.items():
        if properties_with_until_list[key] == 0:  # To be removed later !!
            index = index + 1
            # if index in failed_properties_list: pass else: passing_properties_index = passing_properties_index + 1
            # print "property " + dut_name + "_sequence_antecedent_" + str(key+1) + "; \t" + str(value) + " ;
            # endproperty"
            print("property " + dut_name + "_sequence_antecedent_" + str(index) + "; \t" + str(
                value) + " ;   endproperty")
        else:
            pass

    print("// -----------------------------------------------------")
    print(" ")
    index = 0
    passing_properties_index = 0

    print("// List of consequences : ")
    print(" ")
    for key, value in prop_symp_dict.items():
        if properties_with_until_list[key] == 0:  # To be removed later !!
            index = index + 1
            # if index in failed_properties_list: pass else: passing_properties_index = passing_properties_index + 1
            # print "property " + dut_name + "_sequence_consequence_" + str(key+1) + "; \t" + str(value) + " ;
            # endproperty"
            print("property " + dut_name + "_sequence_consequence_" + str(index) + "; \t" + str(
                value) + " ;   endproperty")
        else:
            pass

    print("// -----------------------------------------------------")
    print(" ")
    prop_index = 0
    passing_properties_index = 0

    for index in range(0, 4):  # Should get values 0, 1, 2 and 3
        print("// List of \"" + str(bin(index)[2:].zfill(2)) + "\" Coverage directives : ")
        print(" ")

        for key, value in seq_cond_dict.items():
            if properties_with_until_list[key] == 0:  # To be removed later !!
                prop_index = prop_index + 1
                # if prop_index in failed_properties_list:
                # pass
                # else:
                # passing_properties_index = passing_properties_index + 1

                if ("rst" in value) and ("isunknown" in value):
                    if index == 0:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) \t ( (not " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  (not " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 1:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) \t ( (not " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  ( " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 2:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) \t ( ( " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  (not " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 3:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) \t ( ( " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  ( " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                else:
                    if index == 0:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) disable iff (rst) ( (not " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  (not " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 1:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) disable iff (rst) ( (not " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  ( " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 2:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) disable iff (rst) ( ( " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  (not " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
                    elif index == 3:
                        print(dut_name + "_" + str(bin(index)[2:].zfill(2)) + "_cover_" + str(
                            prop_index) + " : \t cover  property \t(@ (posedge clk) disable iff (rst) ( ( " + dut_name + "_sequence_antecedent_" + str(
                            prop_index) + " )  and  ( " + dut_name + "_sequence_consequence_" + str(
                            prop_index) + " ) ) ) ; ")
            else:  # if properties_with_until_list[key] == 1:
                pass

        print("// -----------------------------------------------------")
        print(" ")
        prop_index = 0

    sys.stdout.close()
    original_prop_file.close()
    prop_file.close()
    return prop_cond_dict, prop_symp_dict
