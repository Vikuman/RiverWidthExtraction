import substring
import glob,os
sttr = "abcdefghijklmnop.1234561.txt"               #file name with extenstion
# for
def delete(file_to_delete){
    
    for f in glob.glob("sttr.*"):                   #delete file with sttr with any extension
	    os.remove(f)
    
}
s = substring.substringByChar(sttr, startChar=sttr[20], endChar=".")
a=s.split(".")[0]
print(a)

if ({{hello}}-a >= 10000000 ):                      #{{hello}} : passed value in script (i.e in first para of delete in home.html)
    delete(sttr)                                    #10000000 : limit of this much milliseconds