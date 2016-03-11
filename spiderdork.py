#!/usr/bin/python
import urllib2
import thread
import sys


def usage():
        print("./script [conf string]\n")
        print(" -d url dork string or list [\"/aaa\", \"/aab\", \"/aac\"]\n -D path/to/dork/list/file.txt")
        print(" -s subdomain string or list [\"aaa.\", \"aab.\", \"aac.\"]\n -S path/to/subdomain/list/file.txt\n")
        
        print(" -l target limit")
        print(" -t Thread number")
        print(" -x extension list [\".com\", \".org\", \".net\"]\n -X path/to/extension/list/file.txt")
        print(" -c character list qwertyuiopasdfghjklzxcvbnm")

def baseN(num, b, numerals="0123456789qwertyuiopasdfghjklzxcvbnm"):
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def scan(dork, subd, tlim, tnum, xlia, clis):
        pass

#  Required        sltxc
# url dork or subdomain list, confirmation string
#  Optional non-defaulting
# subdomain list, target limit, number of threads
#  Optional defaulting
# domain extensions list, character list,


dork = [""]
subd = [""]
tlim = 0
tnum = 0
xlis = [""]
clis = [""]

if len(sys.argv) < 4:
        usage()
else:
        for a in range(2, len(sys.argv)/2, +2):
                if sys.argv[a] == "-d":
                        dork = list(sys.argv[a+1])
                elif sys.argv[a] == "-D":
                        dork = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-s":
                        subd = list(sys.argv[a+1])
                elif sys.argv[a] == "-S":
                        subd = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-l":
                        subd = list(sys.argv[a+1])
                elif sys.argv[a] == "-t":
                        subd = list(sys.argv[a+1])
                elif sys.argv[a] == "-x":
                        subd = list(sys.argv[a+1])
                elif sys.argv[a] == "-X":
                        subd = open(str(sys.argv[a+1])).read().splitlines()
                elif sys.argv[a] == "-c":
                        subd = list(sys.argv[a+1])
                else:
                        usage()
                        break
        for b in range(0, thread_num):
                thread.start_new_thread(scan, (dork, subd, tlim, tnum, xlia, clis))

        while True:
                pass





'''
ext = [".com", ".net", ".org", ".edu", ".gov"]
lst = "0123456789abcdefghijklmnopqrstuvwxyz"
a = 47182
b = 0
thread_num = 40
dork = "/wp-login.php"
conf = "Powered by WordPress"

def scan(ext, lst, a, b, add, dork, conf):
	while True:
		for b in range(0, len(ext)):
			try:
				address = baseN(a, len(lst), lst) + ext[b]
				sh.ping(address, "-c 1", _out="/dev/null")
				page = urllib2.urlopen("http://" + address + dork).read()
				if conf in page:
					open("index.html", "a").write(address + "<br>\n")
					open("targets.txt", "a").write(address + "\n")
					print(address + " - Found one!")
			except sh.ErrorReturnCode_1:
				print(address + " - Failed No Responce")
			except sh.ErrorReturnCode_2:
				print(address + " - Failed No Responce")
			except Exception:
				print(address + " - Failed WP Check")
		a += add

for c in range(a, a+thread_num):
	thread.start_new_thread(scan, (ext, lst, c, b, thread_num, dork, conf))

while True:
	pass
'''
