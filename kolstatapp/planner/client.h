#ifndef CLIENT_H
#define CLIENT_H

//HEADERS

struct query_header {
	int query_type;
};

struct answer_header {
	int answer_type;
};

//SIMPLE

struct query_simple {
	int source_st;
	int dest_st;
	int dep_time;
};

struct answer_simple {
	int count;
};

struct answer_simple_conn {
	int length;
};

struct answer_simple_elem {
	int dep_stop;
	int arr_stop;	
};

struct simple_stats {
	int num_vertices;
	int max_heap;
	int num_pop;

	simple_stats(): num_vertices(0), max_heap(0), num_pop(0) {}
};

//ERROR

struct answer_error {
	int errnum;
	int message_length;
};

void* do_work(void*);

//CONSTANTS

const int VERSION_QUERY = 0;
const int SIMPLE_QUERY = 1;

const int ANSWER_OK = 0;
const int ANSWER_ERROR = 1;

const int ERR_UNDEFINED = 0;
const int ERR_NOT_IMPLEMENTED = 1;
const int ERR_BAD_REQUEST = 2;

const int COUNT = 3;
const int DELTA = 30;

#endif 
