#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <vector>
#include <algorithm>

using namespace std;

#include "client.h"

static const char* GRAPH_FILE = "gen_graph/graph.out";
static const int VERSION_MAGIC = 809915476;
static const int INF_T = 1440 * 500 + 1;

bool load_graph();

static const int DIJ_NO_CONN = 1;
static const int DIJ_OK = 0;

struct vertex : vector<pair<int, int> > {
	void add_edge(int to, int nr){
		push_back(make_pair(to, nr));
	}	
};

struct el_conn {
	int dep_station;
	int arr_station;
	int dep_time;
	int arr_time;
	int dep_stop;
	int arr_stop;

	el_conn(int a, int b, int c, int d, int e, int f) :
		dep_station(a),
		arr_station(b),
		dep_time(c),
		arr_time(d),
		dep_stop(e),
		arr_stop(f)
	{
	}

	bool operator < (const el_conn& other) const {
		return dep_time < other.dep_time;
	}

};

struct connection : vector<el_conn> {
	void sort(){
		::sort(begin(), end());
	}

	void add(int t[6]){
		push_back(el_conn(t[0], t[1], t[2], t[3], t[4], t[5]));
	}

	el_conn* get_after(int t){
		connection::iterator it = ::lower_bound(begin(), end(), el_conn(0, 0, t, 0, 0, 0));
		if(it == end()) return NULL;

		return &(*it);
	}
};


int dijkstra(query_simple, connection&, simple_stats*);
#endif
