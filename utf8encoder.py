import sys
import binascii


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

outputFile = open("utf8encoder_out.txt", 'ab')
utf16File = open(sys.argv[1],'rb')

deleteContent(outputFile)

def strToBin(twoBytes):
    return ''.join((bin(ord(byte))[2:].zfill(8) for byte in twoBytes))

def getUtf8Format(twoBytesHex):    
    
    
    if int(twoBytesHex,16) <= 127:
        utf8Format="0vvvvvvv"
    elif int(twoBytesHex,16) <= 2047:
        utf8Format="110vvvvv10vvvvvv"
    elif int(twoBytesHex,16) <= 65535:
        utf8Format="1110vvvv10vvvvvv10vvvvvv"
        
    return utf8Format
 
def getUtf8String(utf8Format,twoBytesBin):
    index=0
    utf8String=""
    length=len(utf8Format)-1
        
    while length > -1:        
        if utf8Format[length] == 'v':       
            utf8String += getbit(int(twoBytesBin,2),index)
            index=index+1
        else:
            utf8String += utf8Format[length]
        length=length-1   
        
    utf8String = utf8String[::-1]
    return utf8String
    
def getbit(bit,index):
    if bit & (1 << index) > 0:
        return "1"
    else:
        return "0"
 
def writeToFile(utf8String):
    if len(utf8String) == 8:
        outputFile.write(chr(int(utf8String,2)))
         
    elif len(utf8String) == 16:
        string1=utf8String[0:8]           
        outputFile.write(chr(int(string1,2)))
        string2=utf8String[8:16]           
        outputFile.write(chr(int(string2,2)))
           
    elif len(utf8String) == 24:
        string1=utf8String[0:8]           
        outputFile.write(chr(int(string1,2)))
        string2=utf8String[8:16]           
        outputFile.write(chr(int(string2,2)))
        string3=utf8String[16:]           
        outputFile.write(chr(int(string3,2)))    
         
try:    
    while True:
        twoBytes = utf16File.read(2)

        if twoBytes == '':
            break

        twoBytesHex = binascii.hexlify(twoBytes)    
        twoBytesBin = strToBin(twoBytes)   
        utf8Format = getUtf8Format(twoBytesHex)
        utf8String = getUtf8String(utf8Format,twoBytesBin)
        writeToFile(utf8String)    
        
finally:        
    utf16File.close()
