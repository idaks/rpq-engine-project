#include <iostream>
#include <cstdlib>
#include <fstream>
#include <string>
#include <math.h>
#include <queue>

using namespace std;
ofstream myfile1;

void times5(int idx){
    if(idx*5<=1000){
        myfile1<<idx<<","<<idx*5<<","<<"5"<<'\n';
        times5(idx*5);
    }
}

void times3(int idx){
    if(idx*3<=1000){
        myfile1<<idx<<","<<idx*3<<","<<"3"<<'\n';
        times3(idx*3);
        times5(idx*3);
    }
}
void times2(int idx){
    if(idx*2<=1000){
        myfile1<<idx<<","<<idx*2<<","<<"2"<<'\n';
        times2(idx*2);
        times3(idx*2);
        times5(idx*2);
    }
}


void cur(){
    times2(1);
    times3(1);
    times5(1);
}

int main(int argc, char **argv) {
    
    string fn1 = "data/sail.csv";
    
    myfile1.open (fn1, ios::out);
    if (myfile1.is_open())
    {
        myfile1<<"startNode,endNode,label\n";
        cur();
        myfile1.close();
    }
    else cout << "Unable to open file";
    return 0;
}