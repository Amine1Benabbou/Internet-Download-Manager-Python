import click 
import requests 
import threading

def Handler(start, end, url, filename): 
     
    headers = {'Range': 'bytes=%d-%d' % (start, end)} 
   
    r = requests.get(url, headers=headers, stream=True) 
  
    with open(filename, "r+b") as f: 
      
        f.seek(start)
        var = f.tell() 
        f.write(r.content)

def download_file(ctx,url_of_file,name,number_of_threads): 
   r = requests.head(url_of_file) 
   if name: 
     file_name = name
   else: 
     file_name = url_of_file.split('/')[-1] 
   
   try: 
     file_size = int(r.headers['content-length']) 
   except: 
    print ("Invalid URL")
    return

for i in range(4): 
     start = part * i 
     end = start + part 
  
          # create a Thread with start and end locations 
     t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url_of_file, 'filename': file_name})
     t.setDaemon(True) 
     t.start()

main_thread = threading.current_thread() 
for t in threading.enumerate(): 
     if t is main_thread: 
        continue
     t.join() 
print(" %s downloaded " % file_name )
  
if __name__ == '__main__': 
       download_file(obj={})