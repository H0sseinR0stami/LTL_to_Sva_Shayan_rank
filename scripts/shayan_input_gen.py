import sys


# function to get maximum number of properties
def prop_count(p_file_name):
    if not isinstance(p_file_name, str):
        raise ValueError(p_file_name + "is not a string!")
    prop_file = open(p_file_name, 'r')
    dut_name = ""
    if "Arbiter" in p_file_name:
        dut_name = "Arbiter"
    prop_max_num = 0
    if dut_name == "Arbiter":
        for l in prop_file:
            if "00_cover" in l and (int(l[l.index("00_cover_") + 9:])) > prop_max_num:
                prop_max_num = (int(l[l.index("00_cover_") + 9:]))
    return prop_max_num


def generate_shayan_input_from_coverage_report(prop_file_name, p_max_num):
    global num_of_properties
    sys.stdout = open("input_shayan_Arbiter", "w")
    # print("// -----------------------------------------------------")
    # print(" ")

    prop_file = open(prop_file_name, 'r')

    dut_name = ""
    if "Arbiter" in prop_file_name:
        dut_name = "Arbiter"

    c00 = 0
    c01 = 0
    c10 = 0
    c11 = 0
    counter = 0
    prop_symp_dict = {}
    cov_00_dict = {}
    cov_01_dict = {}
    cov_10_dict = {}
    cov_11_dict = {}
    property_number = []
    if dut_name == "Arbiter":
        for line in prop_file:
            cov_00_dict[counter] = []
            if "00_cover" in line and c00 < p_max_num:
                c00 = c00 + 1
                property_number.append(int(line[line.index("00_cover_") + 9:]))
                # Read 2 lines afterwards, focus is on the 2nd line!
                next_line = next(prop_file)
                next_line = next(prop_file)
                cov_00_dict[counter] = next_line.split()[0]
                # print("C_" + dut_name + "_property_" + str(counter+1) + "_00_cover_count = " + cov_00_dict[counter])

                counter = counter + 1

        prop_file.close()

        num_of_properties = counter
        counter = 0

        prop_file = open(prop_file_name, 'r')

        for line in prop_file:
            cov_01_dict[counter] = []
            if "01_cover" in line and c01 < p_max_num:
                c01 = c01 + 1
                next_line = next(prop_file)
                next_line = next(prop_file)
                cov_01_dict[counter] = next_line.split()[0]
                # print("C_" + dut_name + "_property_" + str(counter+1) + "_01_cover_count = " + cov_01_dict[counter])

                counter = counter + 1

        prop_file.close()

        counter = 0

        prop_file = open(prop_file_name, 'r')

        for line in prop_file:
            cov_10_dict[counter] = []
            if "10_cover" in line and c10 < p_max_num:
                c10 = c10 + 1
                next_line = next(prop_file)
                next_line = next(prop_file)
                cov_10_dict[counter] = next_line.split()[0]
                # print("C_" + dut_name + "_property_" + str(counter+1) + "_10_cover_count = " + cov_10_dict[counter])

                counter = counter + 1

        prop_file.close()

        counter = 0

        prop_file = open(prop_file_name, 'r')

        for line in prop_file:
            cov_11_dict[counter] = []
            if "11_cover" in line and c11 < p_max_num:
                c11 = c11 + 1
                next_line = next(prop_file)
                next_line = next(prop_file)
                cov_11_dict[counter] = next_line.split()[0]
                # print("C_" + dut_name + "_property_" + str(counter+1) + "_11_cover_count = " + cov_11_dict[counter])

                counter = counter + 1

        prop_file.close()

        counter = 0

    # Only for debugging!
    # print "cov_00_dict length = " + str(len(cov_00_dict))
    # print "Number of Properties = " + str(num_of_properties)

    # We want to print the cover values in csv format parsable by Shayan tool !!
    # Shayan format (order) is :
    # 11	10	01	00	11+10	01+00	11+01	10+00	11+10+01+00

    for property_index in range(0, num_of_properties):
        print("C_" + dut_name + "_property_" + str(int(property_number[property_index])) + "," + str(
            int(cov_11_dict[property_index])) + "," + str(int(cov_10_dict[property_index])) + "," + str(
            int(cov_01_dict[property_index])) + "," + str(int(cov_00_dict[property_index])) + "," + str(
            int(cov_11_dict[property_index]) + int(cov_10_dict[property_index])) + "," + str(
            int(cov_01_dict[property_index]) + int(cov_00_dict[property_index])) + "," + str(
            int(cov_11_dict[property_index]) + int(cov_01_dict[property_index])) + "," + str(
            int(cov_10_dict[property_index]) + int(cov_00_dict[property_index])) + "," + str(
            int(cov_11_dict[property_index]) + int(cov_10_dict[property_index]) + int(
                cov_01_dict[property_index]) + int(cov_00_dict[property_index])))

    failed_properties_file = open(dut_name + "_failed_properties.txt", 'w')

    num_of_failed_properties = 0
    for property_index in range(0, num_of_properties):
        if int(cov_10_dict[property_index]) > 0:
            num_of_failed_properties = num_of_failed_properties + 1

    failed_properties_file.write("failed_properties_list = [ ")
    iteration = 0
    for property_index in range(0, num_of_properties):
        if (int(cov_10_dict[
                    property_index]) > 0):  # if property is failing, it must be removed from list of properties!
            iteration = iteration + 1
            if iteration == num_of_failed_properties:
                # put the failed property number in list
                failed_properties_file.write(str(int(property_number[property_index])) + " ]")
            else:
                # put the failed property number in list
                failed_properties_file.write(str(int(property_number[property_index])) + " , ")
                if iteration % 24 == 0:
                    failed_properties_file.write(str(int(property_number[property_index])) + " , \n")
    failed_properties_file.write("\n")

    failed_properties_file.close()

    print("\nNumber of failed properties : " + str(num_of_failed_properties))
    sys.stdout.close()
    return cov_00_dict, prop_symp_dict
