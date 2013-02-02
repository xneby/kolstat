#ifndef HEAP_H
#define HEAP_H

#include <vector>

struct vbox {
	int v;
	int key;
	vbox(int key, int v): v(v), key(key) {}
	vbox(){}
};

class Heap {
	vbox* kop;
	int* wsk;
	int qnum;

	void heap_up(int x){
		while(x != 1){
			if(kop[x].key > kop[x/2].key)
				my_swap(x, x/2);
			else
				break;
			x /=2 ;
		}
	}

	void heap_down(int x){
		while(x <= size/2){
			if(kop[x].key < kop[2*x].key){
				my_swap(x, 2*x);
				x *= 2;
			} else if(2*x+1 <= size && kop[x].key < kop[2*x+1].key){
				my_swap(x, 2*x+1);
				x *= 2;
				x++;
			} else break;
		}
	}

	void my_swap(int i, int j){
		swap(wsk[kop[i].v], wsk[kop[j].v]);
		swap(kop[i], kop[j]);
	}

public:
	int size;
	Heap(vbox* kop, int* wsk): kop(kop), wsk(wsk){
		size = 0;
	}

	~Heap(){
		while(size) pop();
	}

	void push(const vbox& v){
		if(wsk[v.v]){
			if(kop[wsk[v.v]].key < v.key){
				kop[wsk[v.v]].key = v.key;
				heap_up(wsk[v.v]);
			}
		} else {
			kop[++size] = v;
			heap_up(size);
		}
	}

	bool empty(){
		return size == 0;
	}

	int pop(){
		int res = kop[1].v;
		my_swap(1, size);
		wsk[res] = 0;
		size --;
		heap_down(1);
		return res;
	}
};

#endif
