#!/usr/bin/env python2
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'kolstat.settings'
sys.path.extend(('../../..', '../../../..'))

from django.contrib.auth.models import User

x = input('Podaj login ').strip()

try:
	u = User.objects.get(username = x)
except User.DoesNotExist:
	print("Brak użytkownika")
	sys.exit(1)

print(u.get_full_name())
if u.is_superuser:
	print("Jest superuserem")

u.is_superuser = True
u.is_staff = True
u.save()
