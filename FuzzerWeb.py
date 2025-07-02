import sys
import requests
import time

from threading import Thread, Lock
from queue import Queue
from termcolor import colored

global_count = 1
urls = []
#Pour éviter de laisser passer les redirections vers la même page
#Dictionaire avec comme clé les codes de statut et comme valeur une liste de taille des pages
codes = {}  #Permet d'associer un code avec plusieurs tailles reçues
padlock = Lock()



#Retrieve parameters
domain = sys.argv[1]
path = sys.argv[2]

#Open file
file = open(path,'r',encoding="latin-1")
lines = file.readlines()
file_size = len(lines)


class Fuzzer(Thread):


    def __init__(self,tail):
        Thread.__init__(self)
        self.tail = tail
        

    def run(self):
        global global_count
        while True:
            try:
                url = self.tail.get()
                response = requests.get(url,timeout=5)
                size = len(response.content)
                if str(response.status_code) not in codes:
                    codes[str(response.status_code)] = []
                with padlock:
                    if((199 < response.status_code < 400 or response.status_code == 403 or response.status_code == 401) and not(isInDico(response.status_code,size))):
                        output = "[" + colored(str(global_count),'green') + "/" + str(file_size) + "] : " + str(response.status_code) + " - url: " + url + " size: " + colored(str(size),'blue')
                        sys.stdout.write("\033[K" + output + "\r") #Le \033[K est la séquence d’échappement pour effacer jusqu’à la fin de la ligne.
                        sys.stdout.flush()
                        urls.append(output)
                        codes[str(response.status_code)].append(size)
                    else:
                        output = "[" + colored(str(global_count),'red') + "/" + str(file_size) + "] : " + str(response.status_code) + " - url: " + url + " size: " + colored(str(size),'blue')
                        sys.stdout.write("\033[K" + output + "\r")
                        sys.stdout.flush()
                    global_count += 1
                    #print(codes)
            except Exception as e:
                #print(f"Erreur : {e}")
                continue
            time.sleep(0.1)
            self.tail.task_done()


def main():

    try:

        start_time = time.time()

        #Number of Threads
        thread_count = int(sys.argv[3])

        print("[" + colored('-','yellow') + "] : Fuzzing through " + domain + "...\n")  

        tail = Queue()

        for i in range(thread_count):
            fuzzer = Fuzzer(tail)
            fuzzer.daemon = True
            fuzzer.start()

        for line in lines:
            url = "http://" + domain + "/" + line.strip()
            tail.put(url)

        tail.join()

        print("\nPossible url(s) : \n")
        for url in urls:
            print(url + "\n")
        
        end_time = time.time()
        execution_time = int(end_time) - int(start_time)
        print(f"Execution time : {execution_time} seconds")

        pass

    except KeyboardInterrupt:
        print("\n[" + str(global_count) + "/" + str(file_size) + "] - " + str(file_size - global_count) + " left")
        print("\nPossible url(s) : \n")
        for url in urls:
            print(url)
        sys.exit(0)
    

def get_request_size(response):
    method_len = len(response.request.method)
    url_len = len(response.request.url)
    headers_len = len('\r\n'.join(f'{k}: {v}' for k, v in response.request.headers.items()))
    body_len = len(response.request.body if response.request.body else '')
    return method_len + url_len + headers_len + body_len

def isInDico(inCode,inSize):
    for size in codes[str(inCode)]:
        if(size == inSize):
            return True
    return False


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("""
This script will fuzz over a domain name given.
Usage: script.py example.com path_file_word nb_thread    
Ex: script.py example.com /usr/share/wordlists/dirb/common.txt 30          
              """)
        sys.exit(0)
    else:
        main()
