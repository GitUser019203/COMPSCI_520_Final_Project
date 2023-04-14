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
        getline(cin, input);

        if(input == "quit")
        {
            output.pop_back();
            break;
        }
        else
        {
            int index = input.find_first_of('*');
            if(index != string::npos)
            {
            input.insert(index, 1, '.');
            
            }
 
            output += "[ \\.;'\\\"\\?!]" + input + "[ \\.;'\\\"\\?!]|" + "[ \\.;'\\\"\\?!]" + input + "$|" + "^" + input + "[ \\.;'\\\"\\?!]|" + "^" + input + "$|";
        }
    }
    
    

    cout << output;
    return 0;
}