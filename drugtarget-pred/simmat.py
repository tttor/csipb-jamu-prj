# simmat.py

import urllib2

def main():
	response = urllib2.urlopen('http://www.genome.jp/dbget-bin/www_bget?-f+k+compound+C00032')
	html = response.read()
	print(html)
	response.close()

if __name__ == '__main__':
	main()