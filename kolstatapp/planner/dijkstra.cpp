#include "dijkstra.h"
#include "client.h"
#include "heap.h"
#include <vector>
#include <cstdio>
#include <ctime>
#include <algorithm>
#include <queue>

using namespace std;

int num_vertices;
int num_edges;

vector<vertex> graph;
vector<connection> edges;

int read_int(FILE* file){
	int res;
	fread(&res, sizeof(res), 1, file);
	return res;
}

bool load_graph(){
	FILE* file = fopen(GRAPH_FILE, "r");
	
	int version;

	printf("Loading graph file...\n");

	version = read_int(file);

	if(version != VERSION_MAGIC){
		printf("FATAL! Wrong graph file header!");
		return false;
	}

	time_t creation = read_int(file);

	printf("Created at %s", ctime(&creation));

	num_vertices = read_int(file);
	num_edges = read_int(file);

	printf("Parameters: V'=%d E=%d\n", num_vertices, num_edges);

	graph.resize(num_vertices);

	for(int i=0; i<num_vertices; i++){
		if(i % 107 == 0){
			printf("\rReading vertices... %4d/%4d (%6.2lf%%) ", i, num_vertices, 100.0 * i / num_vertices);
			fflush(stdout);
		}
		int degree = read_int(file);
		for(int j=1; j<=degree; j++){
			int where = read_int(file);
			int nr = read_int(file);
			graph[i].add_edge(where, nr);
		}
	}

	printf("\033[2K\rReading vertices... done\n");

	edges.resize(num_edges + 1);

	for(int i=1; i <= num_edges; i++){
		if(i % 107 == 0){
			printf("\rReading connections... %4d/%4d (%6.2lf%%) ", i, num_edges, 100.0 * i / num_edges);
			fflush(stdout);
		}
		int num = read_int(file);
		for(int j=1; j<=num; j++){
			int t[6];
			for(int k=0; k<6; k++) t[k] = read_int(file);
			edges[i].add(t);
		}
		edges[i].sort();
	}

	printf("\033[2K\rReading connections... done\n");

	printf("Loaded graph file.\n");

	fclose(file);
	return true;
}

int dijkstra(query_simple q, connection& result, simple_stats* st){
	if(q.source_st == q.dest_st) return DIJ_NO_CONN;

	bool* vis = new bool[num_vertices];
	int* d = new int[num_vertices];
	el_conn** p = new el_conn*[num_vertices];
	int* wsk = new int[num_vertices + 1];
	vbox* kop = new vbox[num_vertices + 1];

	fill(vis, vis + num_vertices, false);
	fill(d, d + num_vertices, INF_T);
	
	d[q.source_st] = q.dep_time;
	p[q.source_st] = NULL;

	Heap kol(kop, wsk);
	kol.push(vbox(-q.dep_time, q.source_st));

	while(!kol.empty()){
		int v = kol.pop();

		st->num_pop ++;
		if(vis[v]) continue;
		st->num_vertices ++;

		vis[v] = true;
		if(v == q.dest_st) break;

		for(vertex::iterator it = graph[v].begin(); it != graph[v].end(); it ++){
			int u = it->first;
			int nr = it->second;

			el_conn* conn = edges[nr].get_after(d[v]);
			if(conn == NULL) continue;

			int nt = conn->arr_time;

			
			if(nt < d[u]){
				d[u] = nt;
				p[u] = conn;
				kol.push(vbox(-nt, u));
				if(kol.size > st->max_heap)
					st->max_heap = kol.size;
			}
		}
	}

	delete[] vis;
	delete[] wsk;
	delete[] kop;

	if(d[q.dest_st] >= INF_T){
		delete[] d;
		delete[] p;
		return DIJ_NO_CONN;
	}

	int w = q.dest_st;
	
	while(p[w]){
		result.push_back(*p[w]);
		w = p[w]->dep_station;
	}

	result.sort();

	return DIJ_OK;
}
