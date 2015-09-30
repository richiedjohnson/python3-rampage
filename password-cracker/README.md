# password cracker

there are 3 scripts in this folder which is used to crack leaked passwords of yahoo, linkedin and formspring. 

yahoo_cracker.py strips off password from clear text file
linkedin_cracker.py uses dictionary attack combined with sha1 hashing to find list of common passwords
formspring_cracker.py also uses dictionary attack combined with sha256 hashing with salt to crack passwords which were leaked

usage 
	python yahoo_cracker.py /input/Yahoo.txt
	python linkedin_cracker.py /input/Linkedin.txt /input/passwords1.txt,/input/passwords2.txt
	python lformspring_cracker.py /input/formspring.txt /input/passwords1.txt,/input/passwords2.txt

