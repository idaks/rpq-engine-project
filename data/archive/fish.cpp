#include <iostream>
#include <cstdlib>
#include <fstream>
#include <string>
#include <math.h>
#include <queue>

using namespace std;
ofstream myfile1;

void cur(long start){
    if(start*2<=1000){
        myfile1<<start<<","<<start*2<<","<<"2"<<'\n';
        cur(start*2);
    }
    if(start*3<=1000){
        myfile1<<start<<","<<start*3<<","<<"3"<<'\n';
        cur(start*3);
    }
    if(start*5<=1000){
        myfile1<<start<<","<<start*5<<","<<"5"<<'\n';
        cur(start*5);
    }
}

void queue_cur(){
    queue<int> q2;
    queue<int> q3;
    queue<int> q5;
    
    q2.push(1);
    q3.push(1);
    q5.push(1);
    while(!q2.empty() || !q3.empty() || !q5.empty()){
        int q2_front = q2.empty()?2000:q2.front();
        int q3_front = q3.empty()?2000:q3.front();
        int q5_front = q5.empty()?2000:q5.front();
        cout<<q2.size()<<","<<q3.size()<<","<<q5.size()<<endl;
        cout<<"front: "<<q2_front<<","<<q3_front<<","<<q5_front<<endl;
        //queue2 smallest
        if(q2_front!= 2000 && q2_front<=q3_front && q2_front<=q5_front){
            q2.pop();
            //check duplicate
            if(q2_front == q3_front){
                q3.pop();
            }
            if(q2_front == q5_front){
                q5.pop();
            }
            if(q2_front*2 <= 1000){
                q2.push(q2_front*2);
                myfile1<<q2_front<<","<<q2_front*2<<","<<"2"<<'\n';
            }
            if(q2_front*3 <= 1000){
                q3.push(q2_front*3);
                myfile1<<q2_front<<","<<q2_front*3<<","<<"3"<<'\n';
            }
            if(q2_front*5 <= 1000){
                q5.push(q2_front*5);
                myfile1<<q2_front<<","<<q2_front*5<<","<<"5"<<'\n';
            }
        }
        else if(q3_front!= 2000 && q3_front<=q5_front){
            q3.pop();
            if(q3_front == q5_front){
                q5.pop();
            }
            if(q3_front*2 <= 1000){
                q2.push(q3_front*2);
                myfile1<<q3_front<<","<<q3_front*2<<","<<"2"<<'\n';
            }
            if(q3_front*3 <= 1000){
                q3.push(q3_front*3);
                myfile1<<q3_front<<","<<q3_front*3<<","<<"3"<<'\n';
            }
            if(q3_front*5 <= 1000){
                q5.push(q3_front*5);
                myfile1<<q3_front<<","<<q3_front*5<<","<<"5"<<'\n';
            }
        }
        else if(q5_front!= 2000){
            q5.pop();
            if(q5_front*2 <= 1000){
                q2.push(q5_front*2);
                myfile1<<q5_front<<","<<q5_front*2<<","<<"2"<<'\n';
            }
            if(q5_front*3 <= 1000){
                q3.push(q5_front*3);
                myfile1<<q5_front<<","<<q5_front*3<<","<<"3"<<'\n';
            }
            if(q5_front*5 <= 1000){
                q5.push(q5_front*5);
                myfile1<<q5_front<<","<<q5_front*5<<","<<"5"<<'\n';
            }
            
        }
    }
}
int main(int argc, char **argv) {
    /*
    string fn1 = "data/fish.csv";
    
    myfile1.open (fn1, ios::out);
    if (myfile1.is_open())
    {
        myfile1<<"startNode,endNode,label\n";
        cur(1);
        myfile1.close();
    }
    else cout << "Unable to open file";
     */
    
    
    string fn1 = "data/fish_queue.csv";
    
    myfile1.open (fn1, ios::out);
    if (myfile1.is_open())
    {
        myfile1<<"startNode,endNode,label\n";
        queue_cur();
        myfile1.close();
    }
    else cout << "Unable to open file";
    return 0;
}