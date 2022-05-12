Shayan is a assertion qualifier tool. It can rank the assertions based on their interestingness.
To run Shayan:
1- An input file should be provided to describe the ocuurences of antecedents and consequents of assertions accoriding to the simulation trace.
	Contingency tabla consists of 9 cells representing ocurrence of antecedent and consequents of each assertion.
	assertion = antecedent->consequent

	Contingency table:
		     c    !c
		   _________________
	   a  |	f11	| f10 |	f1+ |	
		  |_____|_____|_____|
		  |	f10	| f00 | f1+ |
	   !a |_____|_____|_____|
		  |	f1+	| f+0 |	f++	|
		  |_____|_____|_____|
	
	f11 represents the ocurence of atencenet and consequent of an assertion being true according to the simulation trace
	f10 represents the ocurence of atencenet being true but the consequent of the assertion being false according to the simulation trace
	f01 represents the ocurence of atencenet being false but the consequent of the assertion being true according to the simulation trace
	 and so on...
The input file should be the same as "shayan_input_liveness_elbdr.txt"
Each row describes on contingency table.
For example:
ID of the assertion,f11,f10,f01,f00,f1+,f0+,f+1,f+0,f++ 
C_0,2048,0,0,96,2048,96,2048,96,2144


2- run in terminal g++ -std=c++11 shayan_test.cpp -o shayan_test

3- run in terminal ./shayan_test path_to_txt_or_vcs_input_file

4- In the terminal you can see the value related to each metric. The assertion with the higher rank is more interesting.
   Please see the example below.

   Property   Support      CC     Rank      IS   
   1            0.96       1.00   0.97      1.05
   2            0.04       1.00   0.43      0.05
   3            0.03       0.55   0.24      0.03
   4            0.04       1.00   0.43      0.05
   5            0.01       -nan   -nan      0.01
   6            0.00       0.45   0.18      0.00



Cheers,
Tara.
