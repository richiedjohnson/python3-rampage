import sys
import requests
import simplejson as json
import datetime
import time
from enum import Enum
import threading
from collections import Counter

Method = Enum('Method', 'GET POST PUT DELETE')
current_milli_time = lambda: int(round(time.time() * 1000))
time_capture_lock = threading.Lock()
times_captured = []
status_captured = []
threads = []

def log_std(msg):
	now = datetime.datetime.now()
	std_time = now.isoformat()
	print(std_time, ' ', msg)

class RESTClient:
	def __init__(self, url, method=Method.GET, log=None):
		self.url = url
		self.method = method
		if log is None:
			self.log = log_std
		else:
			self.log = log
		
	def processGET(self, thread_name):
		start = current_milli_time()
		response_json = requests.get(self.url)
		#print("Thread Name : ", thread_name)
		#print("Response message:",response_json.json())
		res = json.loads(response_json.text)
		if res['status'] == 'success' and res['message'].startswith("Hello "):
			status_captured.append("Validated")
			#print("Response : Validated")
		else:
			status_captured.append("Pling!!!!")
			#print("Pling!!!!")
		duration = current_milli_time()-start
		#print("Request took "+str(duration)+"ms to complete")
		with time_capture_lock : 
			times_captured.append(duration)

class LoadTester:
	def __init__(self,url,method=Method.GET,no_of_threads=10):
		self.client = RESTClient(url, method)
		self.no_of_threads = no_of_threads
	
	def process(self):
		print("processing..", self.no_of_threads,"threads")
		
		for counter in range(self.no_of_threads):
			thread = threading.Thread(target = self.client.processGET,args=(str(counter),))
			threads.append(thread)
		
		#starts all threads in the pool
		for thread in threads:
			thread.start()
		
		#causes main thread to wait until all threads in the pool finish execution		
		for thread in threads:
			thread.join()
			
	def find_average_time(self):
		print("Average : ",sum(times_captured)/float(len(times_captured)),"ms")
		
	def find_max_time(self):
		print("Max Time : ",max(times_captured),"ms")
		
	def find_min_time(self):
		print("Min Time : ",min(times_captured),"ms")
		
	def find_response_status(self):
		counter = Counter(status_captured)
		print("Validated responses : "+str(counter['Validated']))
		print("Error responses : "+str(counter['Pling!!!!']))

if __name__ == '__main__':
	url = sys.argv[1]
	thread_no = sys.argv[2]
	tester = LoadTester(url, Method.GET, int(thread_no))
	tester.process()
	print(times_captured)
	tester.find_average_time()
	tester.find_max_time()
	tester.find_min_time()
	tester.find_response_status()