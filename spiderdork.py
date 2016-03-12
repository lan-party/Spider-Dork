#!/usr/bin/python
import urllib2
import thread
import sys


def usage():
        print("./script [conf string]\n")
        print(" -D path/to/dork/list/file.txt")
        print(" -S path/to/subdomain/list/file.txt\n")
        
        print(" -l target limit")
        print(" -t Thread number")
        print(" -X path/to/extension/list/file.txt")
        print(" -c character list qwertyuiopasdfghjklzxcvbnm")
        print(" -O output file location")
        print(" -lod load save location")

def baseN(num, b, numerals="0123456789qwertyuiopasdfghjklzxcvbnm"):
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def scan(dork, subd, tlim, tnum, xlia, clis, ofil, conf, load):
        while True:
                address = ""
                for a in range(0, len(dork)):
                        for b in range(0, len(subd)):
                                for c in range(0, len(xlis)):
                                        try:
                                                address = subd[b] + baseN(load, len(clis), clis) + xlis[c] + dork[a]
                                                page = urllib2.urlopen("http://" + address).read()
                                                if conf in page:
                                                        open(ofil, "a").write(address + "\n")
                                                        print(address + " - Found one!")
                                                else:
                                                        print(address + " - No Confirmation.")
                                        except Exception, e:
                                                print(address + " - Not Found.")
                load += tnum
                
#  Required        sltxc
# url dork or subdomain list, confirmation string
#  Optional non-defaulting
# subdomain list, target limit, number of threads
#  Optional defaulting
# domain extensions list, character list,


dork = [""]
subd = [""]
xlis = [""]
clis = ""
conf = ""
ofil = ""
tlim = 0
tnum = 0
save = 0

if len(sys.argv) < 4:
        usage()
else:
        conf = sys.argv[1]
        for a in range(2, len(sys.argv), +2):
                if sys.argv[a] == "-D":
                        dork = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-S":
                        subd = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-l":
                        tlim = int(sys.argv[a+1])
                elif sys.argv[a] == "-t":
                        tnum = int(sys.argv[a+1])
                elif sys.argv[a] == "-X":
                        xlis = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-c":
                        clis = str(sys.argv[a+1])
                elif sys.argv[a] == "-O":
                        ofil = str(sys.argv[a+1])
                elif sys.argv[a] == "-lod":
                        save = int(sys.argv[a+1])
                else:
                        usage()
                        break
        for b in range(save, save+tnum):
                thread.start_new_thread(scan, (dork, subd, tlim, tnum, xlis, clis, ofil, conf, b))

        while True:
                pass
