#include <sys/socket.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/un.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>

#include "client.h"
#include "config.h"
#include "dijkstra.h"

void fail(const char* message) {
	perror(message);
	exit(1);
}

void new_thread(long fd){
	pthread_t _;
	int rc = pthread_create(&_, NULL, do_work, (void *) fd);
}
bool work = true;

static bool run_server(struct sockaddr_un *sap){
	int fd_skt, fd;

	fd_skt = socket(AF_UNIX, SOCK_STREAM, 0);
	if(fd_skt < 0) fail("fd_skt");

	if( bind(fd_skt, (struct sockaddr*)sap, sizeof(*sap)) < 0)
		fail("bind");

	if( listen(fd_skt, NUM_THREADS) < 0)
		fail("listen");

	while(work) {
		fd = accept(fd_skt, NULL, 0);
		if(fd < 0)
			fail("accept");
		
		new_thread(fd);
	}
}

void quit(int){
	printf("Exiting...\n");
	unlink(PATH);
	_exit(0);
}

int main(){

	signal(SIGINT, quit);
	signal(SIGQUIT, quit);
	signal(SIGTERM, quit);

	struct sockaddr_un sa;
	strcpy(sa.sun_path, PATH);
	sa.sun_family = AF_UNIX;

	if(!load_graph()){
		exit(1);
	}

	run_server(&sa);
}
