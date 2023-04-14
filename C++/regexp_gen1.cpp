// Online C++ compiler to run C++ program online
#include <iostream>
#include <string>
#include <cctype>

using namespace std;

int main() {
    
    string input;
    string output;
    while(true){
        cout << "Enter the refactoring pattern:" << endl;
        cin >> input;

        if(input == "quit")
        {
            output.pop_back();
            break;
        }
        else
        {
            output += "[ \\.;'\\\"\\?!]" + input + ".*|" + "^" + input + ".*|";
        }
    }
    
    

    cout << output;
    return 0;
}