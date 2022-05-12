#cd c:\Arbiter_assertion_semantic_analysis\sim
#vsim -do sim_Arbiter_req_grant_check.do

# create the Library working directory

vlib work

# compile the src and tb files along with the includes and options

if {[catch {
    vlog -work work -vopt +incdir+../include -nocovercells "../rtl/Arbiter.sv"
} result]} {
    quit -f
}

# compile the src and tb files along with the includes and options
vlog -work work -vopt +incdir+../include -nocovercells "../rtl/Arbiter.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../tb/bfm_arbiter.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../tb/Arbiter_tb_req_grant_check.sv" -assertdebug -cover bcefsx 


# simulate the top file(testbench)
vsim -assertdebug -t 1ns -coverage -voptargs="+cover=bcesfx" work.Arbiter_tb_req_grant_check


# View Assertions
view assertions

# add the signals into waveform	
#add wave sim/:Arbiter_tb_req_grant_check:BFM:DUT:*

#vcd file wave_dumps_valid_ip.vcd
#vcd add -r -optcells Arbiter_tb_req_grant_check:BFM:DUT:*	

# run the simulation
run -all

#vcd flush

# txt reports
#coverage report -assert -detail -verbose -output Arbiter_assertion_report_req_grant_check.txt :
coverage report -detail -cvg -directive -comments -output Arbiter_cover_report_req_grant_check.txt :




# xml reports
#coverage report -assert -detail -verbose -xml -output Arbiter_assertion_report_req_grant_check.xml  :
#coverage report -detail -cvg -directive -comments -xml -output Arbiter_cover_report_req_grant_check.xml  :

quit -f