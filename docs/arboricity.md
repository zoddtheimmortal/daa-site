# Arboricity and Subgraph Listing Algorithms

Norishige Chiba and Takao Nishizeki

## Recursive Approach

The following C++ implementation is based on [Chiba & Nishizeki (1985)](https://doi.org/10.1137/0214017).

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using vi = vector<int>;
using vl = vector<ll>;

#define all(x) x.begin(), x.end()
#define fr(i, a, b) for (ll i = a; i < (b); ++i)
#define rf(i, a, b) for (ll i = b; i >=(a); i--)
#define nL "\n"
#define fast_io ios_base::sync_with_stdio(false);cin.tie(nullptr)

#define MAXSTACK 10000

ll n,m;
vector<set<int>> adj;
vector<int> S,T;
vector<int> reverse_index;

void UPDATE(int i,set<int>& C){
if(i>MAXSTACK){
cerr<<"Stack overflow"<<nL;
exit(1);
}
if(i>n) return;
if(i==n){
for(int v:C){
cout<<reverse_index[v]<<" ";
}
cout<<nL;
return;
}
else{
if(!C.empty()&&!adj[i].empty()){

            // intersection = C U N(i)
            set<int> intersection;
            set_intersection(all(C),adj[i].begin(),adj[i].end(),inserter(intersection,intersection.begin()));

            // difference = C - N(i)
            set<int> difference;
            set_difference(all(C),adj[i].begin(),adj[i].end(),inserter(difference,difference.begin()));

            if(!difference.empty()){
                UPDATE(i+1,C);
            }

            for(int x:intersection){
                for(int y:adj[x]){
                    if(C.find(y)==C.end()&&y!=i){
                        T[y]++;
                    }
                }
            }

            for(int x:difference){
                for(int y:adj[x]){
                    if(C.find(y)==C.end()){
                        S[y]++;
                    }
                }
            }

            bool FLAG=true;

            // maximality test
            for(int y:adj[i]){
                if(C.find(y)==C.end()&&y<i&&T[y]==intersection.size()){
                    FLAG=false;
                }
            }

            // lexico test
            vector<int> diff_sort(difference.begin(),difference.end());
            sort(all(diff_sort));

            auto p=diff_sort.size();
            fr(k,0,p){
                int q=diff_sort[k];
                for(int y:adj[q]){
                    if(C.find(y)==C.end()&&y<i&&T[y]==intersection.size()){
                        if(y>=q){
                            S[y]--;
                        }
                        else if(k==0||y>=diff_sort[k-1]){
                            if(S[y]+k-1==p){
                                FLAG=false;
                            }
                        }
                    }
                }
            }

            if(intersection.size()==0){
                fr(y,0,i){
                    if(C.find(y)==C.end()&&y!=i&&T[y]==intersection.size()&&S[y]==0){
                        if(diff_sort.back()<y){
                            FLAG=false;
                        }
                        else if(diff_sort.back()<i-1){
                            FLAG=false;
                        }
                    }
                }
            }

            for(int x:intersection){
                for(int y:adj[x]){
                    if(C.find(y)==C.end()&&y!=i){
                        T[y]=0;
                    }
                }
            }

            for(int x:difference){
                for(int y:adj[x]){
                    if(C.find(y)==C.end()){
                        S[y]=0;
                    }
                }
            }

            if(FLAG){
                set<int> SAVE=difference;
                C=intersection;
                C.insert(i);
                UPDATE(i+1,C);

                C.erase(i);
                for(int x:SAVE){
                    C.insert(x);
                }
            }
        }
    }

}

void CLIQUE(){
S.resize(n,0);
T.resize(n,0);

    set<int> C={0};
    UPDATE(1,C);

}

void solve(){
cin>>n>>m;

    adj.resize(n);
    fr(i,0,m){
        ll f,s;
        cin>>f>>s;
        adj[f].insert(s);
        adj[s].insert(f);
    }

    vector<pair<int,int>> degree;
    fr(i,0,n){
        degree.push_back({adj[i].size(),i});
    }

    sort(all(degree));

    unordered_map<int,int> new_index;
    fr(i,0,n){
        new_index[degree[i].second]=i;
        reverse_index.push_back(degree[i].second);
    }

    vector<set<int>> new_adj(n);
    fr(i,0,n){
        for(int x:adj[i]){
            new_adj[new_index[i]].insert(new_index[x]);
        }
    }

    adj=new_adj;

    CLIQUE();

}

int main(){
fast_io;
ll t=1;
// cin>>t;

    while(t--){
        solve();
    }

}

```

### Issues

-   Recursive approach runs into stack overflow for larger graphs (>10000 nodes), this can be mitigated by converting the above code into an iterative approach
