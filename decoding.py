# -*- coding: utf-8 -*-
import subprocess
def qrdecode():
   subprocess.call('zbarimg ./encrypt.jpg >result.txt',shell=True)
   f=open('result.txt','r')
   a=f.read().decode('utf8')
   a=a[8:]  	
   b=[]
   for i in range(len(a)-1):
       b.append(ord(a[i]))
   for i in range(len(b)):
       b[i]=b[i]^65535
       b[i]=b[i]-23    
   b=b[::-1]
   for i in b:
      print i,
   return 1
#print a

