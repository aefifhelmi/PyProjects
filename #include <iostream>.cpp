#include <iostream>

using namespace std;

const int listSize = 4;

int main(){
    do{
        string broski[listSize];
        int index;

        cout << "Enter Your Name: ";

        for (index = 0; index < listSize; index++){
            cin >> broski[index];
        }

        for (index = 0; index < listSize; index++){
        cout << broski[index] << " ";
        }
    }
    while ();
}
