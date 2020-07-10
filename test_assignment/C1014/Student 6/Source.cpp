#include<iostream>
using namespace std;




int main()
{
	//Given Information
	const int NUM_STUDENTS = 50;

	float heights[NUM_STUDENTS] = { 52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73 };

	//setting my varibales as integers and floats respectivly
	float newgirlheight, lowval, highval;
	int hnum, lnum, mnum;
	
	//input to find out the height of the 51st girl
	cout << "Enter the height of the 51st girl ";
	cin >> newgirlheight;

	//indices for the intital start, end, and middle heights
	lnum = 0;
	hnum = NUM_STUDENTS-1;
	mnum = (lnum + hnum) / 2;

	//indices for the intital start, end, and middle heights
	lowval = heights[lnum];
	highval = heights[hnum];
	//	
	//
	//

	//output to show if the newgirl is the shortest
	if (newgirlheight < lowval)
	{
		cout << "The 51st girl is the shortest and belongs in the front" << endl;
	}
	//output to show if the newgirl is the tallest
	if (newgirlheight > highval)
	{
		cout << "The 51st girl is the tallest and belongs at the end" << endl;
	}
	//statement to show that if the newgirl is in between the shortest and the tallest value to follow the following steps
	else if (lowval<newgirlheight && newgirlheight<highval)
	{	
		//for loop that happens 6 times since 2^6=64>50
		for (int i = 0; i < 6; i++)
		{
			//if new girl height is larger than the middle value them the low value will equal the middle value
			//and the new middle num will equal the higher number and the new lower number divided by 2and the middle value 
			if (newgirlheight > heights[mnum])
			{
				lnum = mnum;
				mnum = (lnum + hnum) / 2;
			}
			else
				//if the newgirl height is shorter than the middle height 
				//the the new high num will equal the middle number
				//and the new middle num will equal the lower number and the new higher number divided by 2
			{
				hnum = mnum;
				mnum = (lnum + hnum) / 2;
				
			}
			//Various outputs
			cout <<i+1<<"th Split" <<endl;
			cout << "The Low value is " << heights[lnum] << endl;
			cout << "The High value is " << heights[hnum] << endl;
		}
		//prints the where the girl goes between
	}cout << "The Newly Added Girl belongs between the " << lnum << "th person and " << hnum <<"th person"<< endl;


	
	system("pause");
	return 0;
}