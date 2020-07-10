#include <iostream>
using namespace std;

/*
 C1014
 Program that places student in a line using binary search
 */

int main(){
    
    //variables
    float h;
    
    //function being called
    void place(float arr[], float h);
    
    //array
    const int NUM_STUDENTS = 50;
    
    float heights[NUM_STUDENTS] = {52.5, 53, 55.5, 56, 56.25, 56.25, 56.25, 56.5, 56.5, 57.75, 57.75, 57.75, 58.5, 58.5, 58.75, 58.75, 59.5, 59.75, 60, 60, 60.25, 60.75, 60.75, 61.5, 61.5, 61.75, 62.5, 62.5, 63, 65.25, 65.5, 65.75, 66.25, 66.25, 67, 67, 67.25, 68.25, 68.5, 69.25, 69.75, 70, 70.25, 70.5, 71, 71, 72.5, 72.5, 72.75, 73};
    
    //asks for height and sets as h
    cout << "How tall are you in inches?  ";
    cin >> h;
    
    //passes array and inputed height to function
    place(heights, h);
    
    return 0;
}

void place(float arr[], float h){
    //variables
    int min;
    int max;
    int guess;
    int i;
    
    //starting values
    max = 49;
    min = 0;
    guess = 24;
    
    //if student is shorter than the first student
    if(h < 52.5){
        cout << "Go before student 1";
    }
    //if student is taller than the last student
    else if(h > 73){
        cout << "Go after student 50";
    }
    //all other cases
    else{
        for(i=1; i=7; i++){
            //if student is shorter than the midpoint guess
            if(h < arr[guess]){
                max = guess;
                guess = (max + min)/2;
            }
            //if student is taller than the midpoint guess
            else if(h > arr[guess]){
                min = guess;
                guess = (max + min)/2;
            }
            //if student is the same height as the midpoint guess
            else{
                cout << "Go after student " << guess +1;
                break;
            }
            
            //if max and min are consecutive student should go in between
            if(max - min == 1){
                cout << "Go after student " << min +1;
                break;
            }
        }
    }
}




