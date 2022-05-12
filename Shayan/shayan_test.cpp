#include <stdio.h>
#include <iostream>
#include <fstream>
#include <cstring>
#include <list>
#include <stdlib.h>
#include <algorithm>
#include <string>
#include <sstream>
#include <cmath>
#include <iomanip>
#include <vector>
#include <algorithm>

using namespace std;

struct line
{
	string oneoneCell, onezeroCell, zerooneCell, zerozeroCell, oneXCell, zeroXCell, XzeroCell, XoneCell, XXCell;
	long double data11, data10, data01, data00, data1X, data0X, dataX0, dataX1, dataXX;
	long double CC, R, S, confidence, interest, IS;

};


list<line> Lines;
list<line>::iterator lit;

long double MaxInterest;
long double MinInterest;
vector<long double> InterestVec;

void MakeList(line&);
void UpdateTables();
void Print();
void ImportCSV(char *);

int main(int argc, char ** argv)
{ 

	string myLine;
	line tempLine;

	unsigned long pos1=0;
    unsigned long pos2=0;
    unsigned long pos3=0;
    unsigned long pos4=0;
    unsigned long pos5=0;
    unsigned long pos6=0;
    unsigned long pos7=0;
    unsigned long pos8=0;
    unsigned long pos9=0;
    unsigned long pos10=0;
    unsigned long pos11=0;
    unsigned long pos12=0;
    unsigned long pos13=0;
    unsigned long pos14=0;
    unsigned long pos15=0;
    unsigned long pos16=0;
    unsigned long pos17=0;
    unsigned long pos18=0;


	

	ifstream myFile(argv[1]);
	// ifstream myFile("shayan_input_liveness_elbdr.txt");
	//ifstream myFile("shayan_input_safety_elbdr.txt");

	//readimg from file to fill out the contengency tables.
	//Contingency tabla consists of 9 cells representing ocurrence of antecedent and consequents of each assertion.
	//assertion = antecedent->consequent

	//Contingency table:
	//	     c    !c
	//	   _________________
	// a  |	f11	| f10 |	f1+ |	
	//	  |_____|_____|_____|
	//	  |	f10	| f00 | f1+ |
	// !a |_____|_____|_____|
	//	  |	f1+	| f+0 |	f++	|
	//	  |_____|_____|_____|
	//
	//f11 represents the ocurence of atencenet and consequent of an assertion being true according to the simulation trace
	//f10 represents the ocurence of atencenet being true but the consequent of the assertion being false according to the simulation trace
	//f01 represents the ocurence of atencenet being false but the consequent of the assertion being true according to the simulation trace
	// and so on...
	if (myFile.is_open())
	{
		cout << "File is Okay!" << endl;
		while (getline(myFile, myLine))	
		{
			pos1 = myLine.find(",");
			pos2 = myLine.find(",", pos1 + 1);
			cout << "pos1 " << pos1 << endl;
			cout << "pos2 " << pos2 << endl;
			if (pos1 < pos2)
			{
				tempLine.oneoneCell = myLine.substr(pos1 +1 , pos2 - pos1 -1);
				cout << "tempLine.oneoneCell = " << tempLine.oneoneCell << endl;
				tempLine.data11 = stoi (tempLine.oneoneCell);
			}

			pos3 = myLine.find(",", pos2);
			pos4 = myLine.find(",", pos3 + 1);
			cout << "pos3 " << pos3 << endl;
			cout << "pos4 " << pos4 << endl;
			if (pos3 < pos4)
			{
				tempLine.onezeroCell = myLine.substr(pos3 +1 , pos4 - pos3 -1);
				cout << "tempLine.onezeroCell = " << tempLine.onezeroCell << endl;
				tempLine.data10 = stoi (tempLine.onezeroCell);
			}

			pos5 = myLine.find(",", pos4);
			pos6 = myLine.find(",", pos5 + 1);
			cout << "pos5 " << pos5 << endl;
			cout << "pos6 " << pos6 << endl;
			if (pos5 < pos6)
			{
				tempLine.zerooneCell = myLine.substr(pos5 +1 , pos6 - pos5 -1);
				cout << "tempLine.zerooneCell = " << tempLine.zerooneCell << endl;
				tempLine.data01 = stoi (tempLine.zerooneCell);
			}

			pos7 = myLine.find(",", pos6);
			pos8 = myLine.find(",", pos7 + 1);
			cout << "pos7 " << pos7 << endl;
			cout << "pos8 " << pos8 << endl;
			if (pos7 < pos8)
			{
				tempLine.zerozeroCell = myLine.substr(pos7 +1 , pos8 - pos7 -1);
				cout << "tempLine.zerozeroCell = " << tempLine.zerozeroCell << endl;
				tempLine.data00 = stoi (tempLine.zerozeroCell);
			}
			
			pos9 = myLine.find(",", pos8);
			pos10 = myLine.find(",", pos9 + 1);
			cout << "pos9 " << pos9 << endl;
			cout << "pos10 " << pos10 << endl;
			if (pos9 < pos10)
			{
				tempLine.oneXCell = myLine.substr(pos9 +1 , pos10 - pos9 -1);
				cout << " tempLine.oneXCell " << tempLine.oneXCell << endl;
				tempLine.data1X = stoi (tempLine.oneXCell);
			}

			pos11 = myLine.find(",", pos10);
			pos12 = myLine.find(",", pos11 + 1);
			cout << "pos11 " << pos11 << endl;
			cout << "pos12 " << pos12 << endl;
			if (pos11 < pos12)
			{
				tempLine.zeroXCell = myLine.substr(pos11 +1 , pos12 - pos11 -1);
				cout << " tempLine.zeroXCell " << tempLine.zeroXCell << endl;
				tempLine.data0X = stoi (tempLine.zeroXCell);
			}

			pos13 = myLine.find(",", pos12);
			pos14 = myLine.find(",", pos13 + 1);
			cout << "pos13 " << pos13 << endl;
			cout << "pos14 " << pos14 << endl;
			if (pos13 < pos14)
			{
				tempLine.XoneCell = myLine.substr(pos13 +1 , pos14 - pos13 -1);
				cout << "tempLine.XoneCell = " << tempLine.XoneCell << endl;
				tempLine.dataX1 = stoi (tempLine.XoneCell);
			}

			pos15 = myLine.find(",", pos14);
			pos16 = myLine.find(",", pos15 + 1);
			cout << "pos15 " << pos15 << endl;
			cout << "pos16 " << pos16 << endl;
			if (pos15 < pos16)
			{
				tempLine.XzeroCell = myLine.substr(pos15 +1 , pos16 - pos15 -1);
				cout << "tempLine.XzeroCell = " << tempLine.XzeroCell << endl;
				tempLine.dataX0 = stoi (tempLine.XzeroCell);
			}

			pos17 = myLine.find(",", pos16);
			pos18 = myLine.find(",", pos17 + 1);
			cout << "pos17 " << pos17 << endl;
			cout << "pos18 " << pos18 << endl;
			if (pos17 < pos18)
			{
				tempLine.XXCell = myLine.substr(pos17 +1 , pos18 - pos17 -1);
				cout << "tempLine.XXCell = " << tempLine.XXCell << endl;
				tempLine.dataXX = stoi (tempLine.XXCell);
			}
			
			MakeList(tempLine);
		}
		myFile.close();
		UpdateTables();
		Print();
		ImportCSV(argv[1]);
	}
	else
	{
		cout << "unable to read file" << endl;
	}
	return 0;
}

void MakeList(line& Line)
{
	Lines.push_back(Line);
}

void UpdateTables()
{
	
	cout << " I am in UpdateTables " << endl;
	for (auto& tempLine : Lines)
	{
		//calculating the metric Support
		tempLine.S = (tempLine.data11 / tempLine.dataXX);
		//calculating the metric Correlation Coefficient
    	tempLine.CC = sqrt(tempLine.data0X*tempLine.data1X*tempLine.dataX1*tempLine.dataX0) ? (((tempLine.data11 * tempLine.data00) - (tempLine.data01 * tempLine.data10)) / sqrt(tempLine.data0X*tempLine.data1X*tempLine.dataX1*tempLine.dataX0)) : 0;
    	//calculating the metric Confidence
    	tempLine.confidence = (tempLine.data11) / (tempLine.data1X);
    	//calculating the metric Interest measure
    	tempLine.interest = (tempLine.data11 * tempLine.dataXX) / (tempLine.data1X * tempLine.dataX1);
 		InterestVec.push_back(tempLine.interest);
    	//calculating the metric IS measure
    	tempLine.IS = sqrt ((tempLine.data11 * tempLine.data11 ) / abs(((tempLine.dataX1 - tempLine.dataX0 ) *  (tempLine.data1X - tempLine.data0X))));
    	//calculating the metric Rank
    	tempLine.R = 0.4 * tempLine.CC + 0.6 * tempLine.S;
	}
}

void Print()
{
	
    int i = 0;
    int j = 0;
    int k = 0;
   
    for (auto& temp : Lines )
    {

       cout << ++i << " is the ID of assertion" << "\n";
       cout << endl;
       cout << "       11: " << temp.data11 << "    10: " << temp.data10 << "\n";
       cout << "       01: " << temp.data01 << "    00: " << temp.data00 << "\n";
       cout << endl;
       cout << endl;
       cout << "F+0 : " << temp.dataX0 << "    F+1 : " << temp.dataX1 << "    F0+ : " << temp.data0X << "    F1+ : " << temp.data1X << "\n";
       cout << "N : " << temp.dataXX << "    S : " << temp.S << "    CC : " << temp.CC << "    R : " << temp.R << "\n";
       cout << "\n \n";
       
       //excelFile << i << ": Antecedent: " << temp.Antecedent << "----" << "Concequent: " << temp.Consequent << endl;
       //excelFile << "F11:," << temp.data[0][0] << ",F10:," << temp.data[0][1] << endl;
       //excelFile << "F01:," << temp.data[1][0] << ",F00:," << temp.data[1][1] << endl;
       //excelFile << "F+0 : " << temp.Fplus0 << "    F+1 : " << temp.Fplus1 << "    F0+ : " << temp.F0plus << "    F1+ : " << temp.F1plus << endl;
       //excelFile << "S : " << temp.S <<     CC : " << temp.CC << "    R : " << temp.R << endl;
       //excelFile << endl;
       //excelFile << endl;
    }

    /*
    Valid LBDR output
    E_noLBDRout
    E_singleLBDRout
    E_switchLBDRout
    E_localport1
    E_localport2
    E_Lport
    E_Nport
    E_Sport
    E_Wport
    */

    	cout << "   Property" << "   Support   " << "   CC  " << "   Rank   " <<  "   IS   " << endl;
    for (auto& temp: Lines )                           
    {
    	cout << "   "<<++j<<"   "<<"   "<< std::setprecision(2) << std::fixed <<"      "<< temp.S <<"       "<<temp.CC
    	<<"   "<< temp.R<<"   "<<"   "<<temp.IS <<endl;

    	/*cout << " Property  " << ++j << endl;
    	cout << " Support                 --->  " << std::setprecision(3) << std::fixed << temp.S  << "     11: " << temp.data11 << "    10: " << temp.data10 << "\n";
    	cout << " Correlation Coefficient --->  " << temp.CC << "     01: " << temp.data01 << "    00: " << temp.data00 << "\n";
    	cout << " Rank                    --->  " << temp.R  << endl;
    	cout << " Confidence              --->  " << temp.confidence  << "\n";
    	cout << " Interest                --->  " << temp.interest    << "\n";
    	cout << " IS                      --->  " << temp.IS    << "\n";
    	cout << endl;*/
    }

    // Sort the Interest Vector in ascending order (least value in index 0)
    sort(InterestVec.begin(), InterestVec.end());
    MinInterest = InterestVec.front();
    MaxInterest = InterestVec.back();
    cout << "Min Interest = " << MinInterest << " , Max Interest = " << MaxInterest << endl;

    	for (auto& temp: Lines )                           
    {
        //normalizing Interest range = max(a) - min(a)
    	//a = (a - min(a) / range)
    	//range for Interst is (max=13.3, min=1)
    	cout << " Property  " << ++k;
    	temp.interest = (temp.interest - MinInterest) / MaxInterest;
    	cout << " Normalized Interest                --->  " << temp.interest    << "\n";
    }
}

void ImportCSV(char *filename)
{
	ofstream outfile ("shayan_output.txt");

	outfile << endl <<"Support," << endl; 
	for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.S <<",";	
    }

    outfile << endl <<"Correlation Coefficient," << endl; 
    for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.CC <<",";	
    }

    outfile << endl <<"R," << endl; 
    for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.R <<",";	
    }

    outfile << endl <<"Confidence," << endl; 
    for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.confidence <<",";	
    }

    outfile << endl <<"interest," << endl; 
    for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.interest <<",";	
    }

    outfile << endl <<"IS," << endl; 
    for (auto& temp: Lines )    
	{
		outfile << std::setprecision(3) << std::fixed << temp.IS <<",";	
    }




    outfile.close();

}
