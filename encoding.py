# -*- coding: utf-8 -*-
import qrcode

def qrencode(text):
     
      
     a=[]
     for i in text:
        a.append(ord(i)+23)  
     c=a[::-1]
     for i in range(len(c)):
           c[i]=c[i]^65535
     d=[]
     for i in c:
         if i<256:
             d.append(chr(i))
         else:
            d.append(unichr(i))

     strs=''
     for i in d:
       strs+=i
     img=qrcode.make(strs)
     img.save('encryptedmsg.jpg')
     return 1

