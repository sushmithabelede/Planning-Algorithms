#include <iostream>
#include <vector>
#include <queue>
#include <stack>

using namespace std;

#define ROW 9
#define COL 10

struct Point {
    int x;
    int y;
};

struct queueNode {
    Point p;
    int dist;
};



bool isValid(int mat[][COL],Point p) {
    if (p.x <= ROW - 1 && p.y <= COL - 1 && p.x >= 0 && p.y >= 0) {
        if (mat[p.x][p.y] == 1) {
            return true;
        }
        else return false;
    }
    else return false;
}


int DFS(int mat[][COL], Point source, Point dest) {

    if (dest.x >= ROW || dest.x < 0 || dest.y >= COL || dest.y < 0) return -1;
  
    std::stack< queueNode > Q;

    bool visited[ROW][COL];
    memset(visited, false, sizeof visited);

    visited[source.x][source.y] = true;
    queueNode src = { source, 0 };
    Q.push(src);


    while (!Q.empty()) {
        queueNode current;
        current = Q.top();
        Q.pop();

        if (current.p.x == dest.x && current.p.y == dest.y) {
            return current.dist;
        }

        //check the adjacent nodes to the current node

        int row[] = { 1,-1,0,0 };
        int col[] = { 0,0,-1,1 };

        for (int i = 0; i < 4; i++) {
            Point nextPt = { current.p.x + row[i],current.p.y + col[i] };
            //std::cout << "entering for " << current.p.x + row[i] <<" "<< current.p.y + col[i]<< std::endl;
            if (isValid(mat, nextPt)) {
                if (!visited[nextPt.x][nextPt.y]) {
                    queueNode nextNd = { nextPt,current.dist + 1 };
                    visited[nextNd.p.x][nextNd.p.y] = true;
                    std::cout << "current " << current.p.x << " " << current.p.y << " dist: " << current.dist << std::endl;
                    std::cout << "visiting " << current.p.x + row[i] << " " << current.p.y + col[i] << " dist: " << nextNd.dist << std::endl;

                    if (nextNd.p.x == dest.x && nextNd.p.y == dest.y) {
                        return current.dist + 1;
                    }
                    Q.push(nextNd);
                    std::cout << "Q size: " << Q.size() << std::endl;
                }
            }

        }
        std::cout << std::endl;

    }

}

int BFS(int mat[][COL], Point source, Point dest ) {
    
    if (!isValid(mat, dest)) return -1;
    if (!isValid(mat, source)) return -1;

    bool visited[ROW][COL];
    memset(visited, false, sizeof visited);

    visited[source.x][source.y] = true;

    queue<queueNode> Q;
    queueNode src = { source, 0 };

    Q.push(src);

    while (!Q.empty()) {

        queueNode current;
        current = Q.front();
        Q.pop();
        
        if (current.p.x == dest.x && current.p.y == dest.y) {
            return current.dist;
        }

        //check the adjacent nodes to the current node

        int row[] = { 1,-1,0,0 };
        int col[] = { 0,0,-1,1 };

        for (int i = 0; i < 4; i++) {
            Point nextPt = { current.p.x + row[i],current.p.y + col[i] };
            //std::cout << "entering for " << current.p.x + row[i] <<" "<< current.p.y + col[i]<< std::endl;
            if (isValid(mat, nextPt)) {
                if (!visited[nextPt.x][nextPt.y]) {
                    queueNode nextNd = { nextPt,current.dist + 1 };
                    visited[nextNd.p.x][nextNd.p.y] = true;
                    std::cout << "current " << current.p.x  << " " << current.p.y<<" dist: "<<current.dist<< std::endl;
                    std::cout<<"visiting "<< current.p.x + row[i] << " " << current.p.y + col[i] <<" dist: "<<nextNd.dist<< std::endl;
                    
                    if (nextNd.p.x == dest.x && nextNd.p.y == dest.y) {
                        return current.dist+1;
                    }
                    Q.push(nextNd);
                    std::cout << "Q size: " << Q.size() << std::endl;
                }
            }

        }
        std::cout<<std::endl;
       

    }


}



// Driver program to test above function
int main()
{ 
    int mat[ROW][COL] =
    {
        { 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 },
        { 1, 0, 1, 0, 1, 1, 1, 0, 1, 1 },
        { 1, 1, 1, 0, 1, 1, 0, 1, 0, 1 },
        { 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 },
        { 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 },
        { 1, 0, 1, 1, 1, 1, 0, 1, 0, 0 },
        { 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 },
        { 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 },
        { 1, 1, 0, 0, 0, 0, 1, 0, 0, 1 }
    };

    Point source = { 0, 0 };
    Point dest = { 3, 4 };

    int dist = DFS(mat, source, dest);

    if (dist != -1)
        cout << "Shortest Path is " << dist;
    else
        cout << "Shortest Path doesn't exist";

    return 0;
}
