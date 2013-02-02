#include <cstdio>
#include <unistd.h>
#include <cstring>
#include "dijkstra.h"
#include "client.h"

void error(int fd, int code, const char* message){
	int len = strlen(message);
	answer_header ah;
	ah.answer_type = ANSWER_ERROR;
	write(fd, &ah, sizeof(ah));
	answer_error ae;
	ae.errnum = code;
	ae.message_length = len;
	write(fd, &ae, sizeof(ae));
	write(fd, message, len);
}

void simple_query(int fd, query_header qh){
	query_simple qs;
	read(fd, &qs, sizeof(qs));

	printf("got query: %d %d %d\n", qs.source_st, qs.dest_st, qs.dep_time);

	vector<pair<connection, simple_stats> > result;

	for(int i=0; i<COUNT; i++){	
		connection conn;
		simple_stats st;
		int ret = dijkstra(qs, conn, &st);
		if(ret == DIJ_NO_CONN) break;
		else if(ret == DIJ_OK) {
			result.push_back(make_pair(conn, st));
			qs.dep_time = 1 + conn.front().dep_time;
		} else error(fd, ERR_UNDEFINED, "Dijkstra returned undefined value.");
	}

	answer_header ah;
	ah.answer_type = ANSWER_OK;
	write(fd, &ah, sizeof(ah));

	answer_simple as;
	as.count = result.size();
	write(fd, &as, sizeof(as));

	for(vector<pair<connection, simple_stats> >::iterator conn = result.begin(); conn != result.end(); conn++){
		answer_simple_conn asc;
		asc.length = conn->first.size();
		write(fd, &asc, sizeof(asc));

		for(connection::iterator it = conn->first.begin(); it != conn->first.end(); it++){
			answer_simple_elem ase;
			ase.arr_stop = it->arr_stop;
			ase.dep_stop = it->dep_stop;
			write(fd, &ase, sizeof(ase));
		}

		write(fd, &(conn->second), sizeof(conn->second));
	}

}

void* do_work(void* data){
	int fd = (long)data;
	query_header qh;

	read(fd, &qh, sizeof(qh));

	int type = qh.query_type;

	switch(type){
		case SIMPLE_QUERY:
			simple_query(fd, qh);
			break;

		default:
			error(fd, ERR_BAD_REQUEST, "Unsupported query type.");
	};

	close(fd);

}
