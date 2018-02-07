from pyfiglet import Figlet
from threading import Thread
from tqdm import tqdm
import argparse
import atexit
import datetime
import fileinput
import itertools, string
import os
import sys
import time
import zipfile


VERSION = '1.0'
AUTHOR = "Fofight"
APP = ""

def argOptions():
	'''
    Parse command line options.
    @returns the arguments
    '''
    mepath = unicode(os.path.abspath(sys.argv[0]))
    mebase = '{0}'.format(os.path.basename(mepath))
    description = '''Zip cracker.'''
    desc = argparse.RawDescriptionHelpFormatter
    
    parser = argparse.ArgumentParser(
    	prog=mebase,
    	description=description,
    	formatter_class=desc,)

    parser.add_argument(
    	'--file',
    	action='store',
    	dest='zname',
    	help='specify zip file',
    	required=True)
    parser.add_argument(
    	'--dict',
    	action='store',
    	help='specify dictionary',
    	required=True)
    parser.add_argument(
    	"--output",
    	action='store',
    	)
    parser.add_argument(
    	"--output", 
    	action="store", 
    	type="string", 
    	dest="output", 
    	help="Specify Path for Extracting", 
    	default='.')
	parser.add_argument(
		"--result", 
		action="store", 
		type="string", 
		dest="result", 
		help="Specify Path if You Want to Save Result", 
		default=None)
	parser.add_argument(
		"--crunch", 
		action="store", 
		type="string", 
		dest="crunch", 
		help="For Using Passwords Directly from crunch use this arguments: -c True or --crunch True",
		default=None)
    parser.add_argument(
    	'-V', '--version',
    	action='version',
    	version='%(prog)s v' + VERSION + " by " + AUTHOR)
    
    args = parser.parse_args()
    
    return args

class ZipCrack():
	def __init__(self,args):
		self.args = args
		self.check_input_conditions()
		self.start_cracking_engine()

	def time_management(self):
		print("[*]	Starting Time ",self.starttime)
		print("[*]	Closing  Time ",self.closetime)
		print("[*]	Password Try  ",self.pwdtries)
		print("[*]	Average Speed ",self.pwdtries/(self.closetime-self.starttime))
		return

	def extractFile(zFile, password):
		print("[+]	Loading Zipfile...  ")
		try:
			zFile.extractall(pwd=password.encode('utf-8'))
			print('[+] Password Found: { ' + passwd +' }')
			endtime = datetime.datetime.now()
			print('PASSWORD: ' + password + '\nTIME: ' +
			      str((endtime - starttime).seconds) + ' SECONDS.')
			exit_handler()
			os._exit(0)
		except RuntimeError:
		    pass
		except zipfile.BadZipFile:
		    print("Please check the file's path. It doesn't seem to be a zip file.")
	        sys.exit(1)	
		except:
			pass

	def start_cracking_engine(self):
		print "[+]	Loading Zipfile...  ",
		fileload=zipfile.ZipFile(self.filename)
		print "OK"
		if self.dictionery:
			print "[+]	Using Dictonery Option.... OK"
			print "[+]	Loading Dictonery File...  OK"
			print "[+]	Brute Force Started ..."
			for i in fileinput.input(self.dictionery):
				pwd=i.strip('\n')
				self.extracting_engine(fileload,pwd)
		if self.crunch:
			print "[+] Connection Stablished as Pipe... OK"
			print "[+]	Brute Force Started ..."
			for i in sys.stdin:
				pwd=i.strip('\n')
				self.extracting_engine(fileload,pwd)
		self.show_info_message()

		return



	def extracting_engine(self,file,pwd):
		self.pwdresult=None
		try:
			file.extractall(self.output,pwd=str(pwd))
			self.show_info_message(pwd=pwd)
			self.pwdresult=True
		except Exception as e:
			if str(e).find('Permission')!=-1:
				self.show_info_message(pwd=pwd)
				self.pwdresult=True
			else:
				self.pwdresult=None
		self.pwdtries=self.pwdtries+1

		return 

		

	def show_info_message(self,pwd=None):
		if pwd:
			data="\n\t !-Congratulation-! \n\t\tPassword Found = "+pwd+'\n'
		else:
			data="\n\t Sorry! Password Not Found \n\n"
		print data
		if self.result:
			print "[+] Saving Output in ",self.result
			f=open(self.result,'a')
			f.write(data)
			f.close()
		self.closetime=time.time()
		self.time_management()
		if pwd:
			print "[+] Exiting..."
			sys.exit(0)
		return


def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def exit_handler():
	print('\n[\033[1;31;40m~\033[1;37;40m] Exiting...\n')

def intro():
	cls()
	f = Figlet(font='graffiti')
	print(f.renderText('NoRKSEC'))
	print('\033[1;32;40mzipCrack.py - (c) 2016 NORKSEC - No rights reserved\033[1;37;40m'+'\n')

def createpassfile(min_len, max_len):
	passfile = open('passFile.txt', 'w')
	chars = string.printable.replace(' \t\n\r\x0b\x0c', '')
	print('[*] Creating passFile...')

	for x in xrange(int(min_len), int(max_len)+ 1):
		for i in itertools.product(chars, repeat=x):
			s = ''.join(i)
			passfile.write("%s\n" % s)
	passfile.close()

def crack(zfile, passfile):
	zfile = zipfile.ZipFile(zfile)
	with open(passfile) as p:
		for line in p.readlines():
			passwd = line.strip('\n')
			if extract(zfile, passwd):
				break

def fileLen(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1





def main():
	"""make the program run
	两个模式：
		1.交互模式
		2.命令行参数模式

	"""
	argopts = argOptions()
	if sys.args < 2:
		atexit.register(exit_handler)
		pirnt("the app have another mode by args,more type python {0} -h".format(APP))
		print('[*] Please choose the options:\n 1. Get Password with passFile\n 2. Get Password with Brute Force.')
		option = raw_input('[*] Enter Option: ')
		if option == '1':
			zfile = raw_input('[*] Enter zip Filename: ')
			passfile = raw_input('[*] Enter *.txt passFile: ')
			print '[*] Getting Password...'
			crack(zfile, passfile)

		elif option == '2':
			passfile = 'passFile.txt'
			zfile = raw_input('[*] Enter zip Filename: ')
			min_len = raw_input('[*] Enter the Min-Length of Password: ')
			max_len = raw_input('[*] Enter the Max-Length of Password: ')
			if min_len > max_len:
				print('[-] Wrong.. Min-length must be smaller or same as Max-length.')
				exit()
			createpassfile(min_len, max_len)
			print '[*] Getting Password...'
			crack(zfile, passfile)
	else:
		password = None
	    i = 0
	    c_t = time()

	    try:
	        max_lines = sum(1 for line in open(args.word_list, 'r'))
	    except Exception:
	        print "Error: wordlist not found!"
	        sys.exit(1)
	    with open(args.word_list, "r") as f:
	        passes = f.readlines()
	        for x in passes:
	            i += 1
	            password = x.split("\n")[0]
	            try:
	                zip_.extractall(pwd=password)
	                t_t = time() - c_t
	                print "\n\nPassword cracked: %s\n" % password
	                print "Took %f seconds to crack the password. That is, "\
	                      "%i attempts per second." % (t_t, i / t_t)
	                sys.exit(1)
	            except Exception:
	                pass
	            output = "%*d / %d | %6.2f%% -> %s\r" % (len(str(max_lines)),
	                                                     i,
	                                                     max_lines,
	                                                     100 * i / max_lines,
	                                                     password
	                                                     )
	            sys.stdout.write(output)
	            sys.stdout.flush()

		
		    if (options.zname is None) | (options.dname is None):
		        parser.print_help()
		        exit(0)
		    else:
		        zname = options.zname
		        dname = options.dname
		    if not os.path.isfile(zname):
		    	print('[\033[1;31;40m-\033[1;37;40m] Zip file \033[1;31;40m' + zname + '\033[1;37;40m does not exist.')
		    	exit(0)
		    if not os.path.isfile(dname):
		    	print('[\033[1;31;40m-\033[1;37;40m] Dictionary file \033[1;31;40m' + dname + '\033[1;37;40m does not exist.')
		    	exit(0)
		    print('[\033[1;31;40m+\033[1;37;40m] Cracking zip file \033[1;31;40m' + zname + '\033[1;37;40m using dictionary file \033[1;31;40m' + dname + '\033[1;37;40m.\n')
		    zfile = zipfile.ZipFile(zname)
		    passfile = open(dname)
		    lineMax = fileLen(dname)
		    print('[\033[1;31;40m+\033[1;37;40m] Testing \033[1;31;40m' + str(lineMax) + '\033[1;37;40m passwords from dictionary file.\n')
		    starttime = datetime.datetime.now()
		    for line in tqdm(passfile.readlines(),total=lineMax):
		        password = line.strip('\n')
		        t = Thread(target=extractFile, args=(zFile, password))
				try:
					t.start()
				except (KeyboardInterrupt, SystemExit):
					os._exit(1)
				time.sleep(2)
			print('\n[\033[1;31;40m-\033[1;37;40m] Password not found in \033[1;31;40m' + dname + '\033[1;37;40m.\n')
			sys.exit(1)
			if not self.args.filename:
				print "[ Error ] Please Provide Zip File Path "
				sys.exit(0)
			print "[+]	Checking Zip File Condition ...",
			if not zipfile.is_zipfile(self.filename):
				print "[ Error ] Bad Zip file"
				sys.exit(0)
			print "	Ok"

			if not self.dictionery and not self.crunch:
				print "[ Error ] Please Provide Dictonery Or Crunch Or Password Option"
				sys.exit(0)
			if self.dictionery and self.crunch:
				print "[ Error ] Please Choose Any One Option From Dict or Crunch"
				sys.exit(0)
			return


	

if __name__ == '__main__':	
	try :
		main()
	except KeyboardInterrupt:
		print("\nExit....")
		sys.exit(1)
