#!/usr/bin/env python

import hashlib
import random
import os, sys, time
from optparse import OptionParser
from subprocess import *




def hashf1(i, strh):
	i = i%10
	if i == 0:
		return hashlib.sha1(strh).hexdigest()
	elif i == 1:
		return hashlib.sha224(strh).hexdigest()
	elif i == 2:
		return hashlib.sha256(strh).hexdigest()
	elif i == 3:
		return hashlib.sha384(strh).hexdigest()
	elif i == 4:
		return hashlib.sha512(strh).hexdigest()
	elif i == 5:
		h = hashlib.new("ripemd160")
		h.update(strh)
		return h.hexdigest()
	elif i == 6:
		h = hashlib.new("dss1")
		h.update(strh)
		return h.hexdigest()
	elif i == 6:
		h = hashlib.new("mdc2")
		h.update(strh)
		return h.hexdigest()
	elif i == 7:
		return hashlib.md5(strh).hexdigest()
	elif i == 8:
		h = hashlib.new("md4")
		h.update(strh)
		return h.hexdigest()
	elif i == 9:
		return hashlib.sha256(hashlib.sha512(strh).hexdigest()).hexdigest()

def hashf2(i, strh):
	return len64(hashf1(i, strh))

def len64(string):
	l = len(string)
	if l == 32:
		string = string[12:32] + string + string[0:12]
	elif l == 40:
		string = hashlib.sha1(string).hexdigest()[12:36] + string
	elif l == 56:
		string = hashlib.sha256(string).hexdigest()[25:33] + string
	elif l == 64:
		string = string[35:48] + string[1:27] + string[29:31] + string[0] + string[31:35] + string[27:29] + string[48:64]
	elif l == 96:
		string = string[3:27] + string[40:80]
	elif l == 128:
		string = string[45:82] + string[90:113] + string[3:7]
	return string


def pat(hlist, slist, rand):
	if rand == -1:
		p = random.randrange(0, 700, 1)
	else:
		p = rand

	if p < 700:
		mot1 = ""
		for i in range(7):
			mot1 = mot1 + hashf2(int(p/10)%10, hashf2(hlist[i], slist[i]))
			if i == int(p/100):
				mot1 = mot1 + hashf2(int(p/10)%10, hashf2(hlist[i], slist[i]))
		mot1 = hashf2(p%10, mot1)

		for i in range(128):
			mot1 = hashf2(i, mot1)
		ret = hashf2(p%10, mot1)


	return [p, ret]

def main():
	parser = OptionParser(usage="%prog [options]", version="%prog 1.0")

	parser.add_option("--passphrase", dest="pp",
		help="passphrase")

	parser.add_option("--code", dest="code",
		help="code")

	parser.add_option("--keynumber", dest="keynumber",
		help="keynumber")

	parser.add_option("--size", dest="size",
		help="number of displayed keys",
		default="10")

	parser.add_option("-p", "--pwpath", dest="pwpath", 
		help="pywallet.py directory (default = ./)",
		default="./")

	(options, args) = parser.parse_args()

	passphrase = options.pp


	slist = []
	for i in range(7):
		slist.append(random.randrange(0, 10, 1))

	if options.code is not None:
		code = options.code
		for i in range(0, 11-len(code)):
			code = "0" + code
		rand = int(code[0:4])
		for i in range(7):
			slist[i] = int(code[i+4])
	else:
		rand = random.randrange(0, 700)


	for j in range(int(options.size)):
		if options.keynumber is not None:
			j = int(options.keynumber)
		print("Key %d"%j)

		passphrase = options.pp + "%d"%(j)

		lm = passphrase.split(" ")
		nm = len(lm)
		if nm < 7 or len(passphrase) < 40:
			print("Passphrase MUST be at least 7 words and 40 characters long")
			exit(0)


		for i in range(7, nm):
			lm[i%7]=lm[i%7]+lm[i]
		lm = lm[0:7]



		result = pat(slist, lm, rand)

		code = "%.4d"%result[0]
		seckey = result[1]
		for i in range(7):
			code = code + "%d"%slist[i]
		print("Code:    " + code)
		print("Secrkey: " + seckey)

		a=Popen(options.pwpath + "pywallet.py --info --importhex --importprivkey " + seckey, shell=True, bufsize=-1, stdout=PIPE).stdout
		print(a.read())
		a.close()

		if options.keynumber is not None:
			break


if __name__ == '__main__':
	main()

