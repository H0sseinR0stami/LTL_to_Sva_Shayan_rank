import os
import shutil

os.chdir("..\\Shayan")
os.system('cmd /c "g++ -std=c++11 shayan_test.cpp -o shayan_test"')

os.system('cmd /c "shayan_test input_shayan_Arbiter > output_shayan_Arbiter"')
