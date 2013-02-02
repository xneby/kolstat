from django.conf import settings

#cache_dir = settings.CACHE_DIR

import os
import pickle

def in_cache(cid):
	return os.access(os.path.join(cache_dir, cid), os.R_OK)

def save(c, cid):
	with open(os.path.join(cache_dir, cid), 'wb') as f:
		pickle.dump(c, f, 2)

def load(cid):
	with open(os.path.join(cache_dir, cid)) as f:
		return pickle.load(f)

def link(cid, oid):
	os.symlink(os.path.join(cache_dir, oid),os.path.join(cache_dir, cid))

def delete(cid):
	os.remove(os.path.join(cache_dir, cid))
