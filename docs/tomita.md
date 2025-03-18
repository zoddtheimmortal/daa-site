# The worst-case time complexity for generating all maximal cliques and computational experiments

Etsuji Tomita, Akira Tanaka, Haruhisa Takahashi

## Recursive Approach

The following C++ implementation is based on [Computational Techniques for Maximum Clique Problems.](https://doi.org/10.1016/j.tcs.2006.06.015)

```cpp
#include<vector>
#include<iostream>
#include<queue>
#include<set>
#include<algorithm>
#include<unordered_map>
#include <unordered_set>

#define ll long long

using namespace std;

set<int> Q;
ll n;

ll max_clique_size=INT64_MIN;
ll total_cliques=0;

time_t start, finish;
unordered_map<ll,ll> distro;

int findu(const vector<vector<int>>& adj, const vector<int>& cand) {
    int max_count = -1;
    int pivot = -1;

    unordered_set<int> cand_set(cand.begin(), cand.end());

    for (int v = 0; v < n; v++) {
        int conn_count = 0;
        for (int neighbor : adj[v]) {
            if (cand_set.count(neighbor)) {
                conn_count++;
            }
        }

        if (conn_count > max_count) {
            max_count = conn_count;
            pivot = v;
        }
    }
    return pivot;
}

vector<int> find_intersection(const vector<int>& a, const vector<int>& b) {
    vector<int> res;
    res.reserve(min(a.size(), b.size()));

    vector<int> sorted_a = a;
    vector<int> sorted_b = b;
    sort(sorted_a.begin(), sorted_a.end());
    sort(sorted_b.begin(), sorted_b.end());

    set_intersection(sorted_a.begin(), sorted_a.end(),
                     sorted_b.begin(), sorted_b.end(),
                     back_inserter(res));
    return res;
}

void expand(vector<vector<int>>& adj,vector<int> subg,vector<int> cand){
    if(subg.empty()){
        total_cliques++;
        max_clique_size=max(max_clique_size,(ll)Q.size());
        distro[Q.size()]++;
        // for (int v : Q) cout << v << " ";
        // cout<<endl;
    }else{
        int u=findu(adj,cand);
        queue<int> ext_u;
        for(auto it:cand){
            int flag=0;
            for(auto it:adj[u]){
                if(it==u){
                    flag=1;
                    break;
                }
            }
            if(flag==0){
                ext_u.push(it);
            }
        }
        while(!ext_u.empty()){
            int q=ext_u.front();
            Q.insert(q);
            vector<int> subg_q=find_intersection(subg,adj[q]);;
            vector<int> cand_q=find_intersection(cand,adj[q]);
            expand(adj,subg_q,cand_q);
            for(int i=0;i<cand.size();i++){
                if(cand[i]==q){
                    cand.erase(cand.begin()+i);
                    break;
                }
            }
            Q.erase(q);
            ext_u.pop();
        }
    }
}

void cliques(vector<vector<int>>& adj,vector<int> &v,vector<pair<int,int>> e){
    Q.clear();
    expand(adj,v,v);
}

int main(){
    int m;
    cin>>n>>m;
    vector<vector<int>> adj(n);
    vector<pair<int,int>> e;
    for(int i=0;i<m;i++){
        int a,b;
        cin>>a>>b;
        e.push_back({a,b});
    }

    for(auto it:e){
        adj[it.first].push_back(it.second);
        adj[it.second].push_back(it.first);
    }
    vector<int> v;
    for(int i=0;i<n;i++){
        v.push_back(i);
    }
    cliques(adj,v,e);

    cout<<"----------------------STATS----------------------"<<endl;
    cout<<"Total cliques: "<<total_cliques<<endl;
    cout<<"Max clique size: "<<max_clique_size<<endl;
    cout<<"Clique size distribution: "<<endl;

    for(auto it:distro){
        cout<<it.first<<": "<<it.second<<endl;
    }
    return 0;
}

```

### Issues

-   Recursive runs well for - [SNAP: Enron Email Network Dataset](https://snap.stanford.edu/data/email-Enron.html) and [SNAP: Wikipedia Vote Network](https://snap.stanford.edu/data/wiki-Vote.html), but runs into Stack Overflow for [SNAP: AS Skitter Internet Topology Graph](https://snap.stanford.edu/data/as-Skitter.html) dataset due to deep recursion.
-   Thus, to further optimize the algorithm, we convert it into an iterative version

## Iterative Approach

## Results

### Wikipedia Vote Network Dataset

```java
----------------------STATS----------------------
Total cliques: 460106
Max clique size: 17
Execution time: 26648 ms
Clique size distribution:
1: 1184
2: 8649
3: 13711
4: 27290
5: 48403
6: 68854
7: 83242
8: 76722
9: 54456
10: 35470
11: 21736
12: 11640
13: 5449
14: 2329
15: 740
16: 208
17: 23
----------------------------------------------------
```

![Wiki Vote Clique Distribution](./graphs/wiki-graph.png)

### Enron Email Network Dataset

```java
----------------------STATS----------------------
Total cliques: 226859
Max clique size: 20
Execution time: 35683 ms
Clique size distribution:
2: 14070
3: 7077
4: 13319
5: 18143
6: 22715
7: 25896
8: 24766
9: 22884
10: 21393
11: 17833
12: 15181
13: 11487
14: 7417
15: 3157
16: 1178
17: 286
18: 41
19: 10
20: 6
----------------------------------------------------
```

![Email Enron Clique Distribution](./graphs/email-graph.png)
