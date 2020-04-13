import sqlite3, hashlib, sys, time, pyfiglet, os.path
from sqlite3 import Error

def ascii_banner():
	# ascii_banner = pyfiglet.figlet_format("HashPy")
	print('''
	 _   _           _     ____        
	| | | | __ _ ___| |__ |  _ \ _   _ 
	| |_| |/ _` / __| '_ \| |_) | | | |
	|  _  | (_| \__ \ | | |  __/| |_| |
	|_| |_|\__,_|___/_| |_|_|    \__, |
	HashPy V1.0.0                |___/ 
	Author: Shamem Ahmad (05.04.2020)
	''')

def banner():
	ascii_banner()
	print('\n')
	print('Hashing started\n')

def ending_banner():
	print('\n')	
	print('Hashing Finished     \n')
	print('')

def total_pass(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        sys.exit(1)

    return conn

def make_hash(raw):
    rawpass = str(raw.strip())
    md5 = hashlib.md5(rawpass.encode())
    md5 = md5.hexdigest()
    sha1 = hashlib.sha1(rawpass.encode())
    sha1 = sha1.hexdigest()
    return (md5,sha1,rawpass)

def insert_hash(conn,value):
	try:
		sql = 'INSERT INTO hash_1 (md5_hash, sha1_hash, raw_text) VALUES (?, ?, ?)'
		cur = conn.cursor()
		cur.execute(sql, value)
		return cur.lastrowid
	except sqlite3.IntegrityError as e:
		print('Error: password already exists.\n')
		pass
	except sqlite3.OperationalError as e:
		print('Error: ' + str(e))
		pass
	except KeyboardInterrupt as e:
		print('Keyboard Interrupt')
		time.sleep(0.5)
		pass
	finally:
		conn.commit()

def main(password_list):
    database = "hashpy_database.sqlite"
    conn = create_connection(database)
    file = open(password_list, "r", encoding="utf8")
    try:
    	with conn:
	        for rawpass in file:
	            hash_dict = make_hash(rawpass)
	            returnid = insert_hash(conn, hash_dict)
	            if returnid:
	            	sys.stdout.write('\rLast ID : '+str(returnid) + ' password : ' + hash_dict[2])
	        ending_banner()

    except KeyboardInterrupt as e:
    	print('Keyboard Interrupt (main)')
    	sys.exit(1)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if(sys.argv[1]) == '-h':
			ascii_banner()
			print('Usage: file.py wordlist.txt')
			sys.exit(1)
		else:
			banner()
			main(sys.argv[1])
	else:
		print('Usage: file.py wordlist.txt')
		pass
