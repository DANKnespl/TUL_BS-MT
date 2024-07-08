"""
cv12
"""
import math
import sys

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N",\
                "O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]

def load_from_stdin(message):
    """
    Loads and validates data from a line in stdin
    """
    print(message)
    tmp = sys.stdin.readline().strip().upper()
    for _,value in enumerate(tmp):
        if value not in alphabet:
            return ""
    return tmp

def dec2bin(dec,size):
    """
    Function to get string representation of binary number
    """
    binary = ""
    tmp = dec
    for _ in range(size):
        binary+=str(tmp%2)
        tmp=math.floor(tmp/2)
    binary = binary[::-1]
    return binary

def bin2dec(binary):
    """
    Function to get integer representation of binary number from string
    """
    dec=0
    for expon,value in enumerate(binary[::-1]):
        dec+=int(value)*math.pow(2,expon)
    return int(dec)

def bcd2gray(binary):
    """
    Function to transform BCD string to Gray string
    """
    last_value = 0
    gray=""
    for _,value in enumerate(binary):
        if bool(last_value)^bool(int(value)):
            gray+="1"
        else:
            gray+="0"
        last_value=int(value)
    return gray

def gray2bcd(gray):
    """
    Function to transform Gray string to BCD string
    """
    last_value = False
    binary=""
    for _,value in enumerate(gray):
        if bool(last_value)^bool(int(value)):
            binary+="1"
            last_value=True
        else:
            binary+="0"
            last_value=False
    return binary

def mtf(input_string):
    """
    Function to transform male string to female string
    """
    code = []
    mtf_queue = alphabet.copy()
    for _,value in enumerate(input_string):
        index_value=mtf_queue.index(value)
        mtf_queue.insert(0,mtf_queue.pop(index_value))
        code.append(index_value+1)
    return code

def ftm(code):
    """
    Function to transform female string to male string
    """
    output_string = ""
    ftm_queue = alphabet.copy()
    for _,index_value in enumerate(code):
        output_string+=ftm_queue[index_value-1]
        ftm_queue.insert(0,ftm_queue.pop(index_value-1))
    return output_string

def bwt(input_string):
    """
    Function to transform string to [string + position]
    """
    array = []
    for i,_ in enumerate(input_string):
        array.append(input_string[-i:]+input_string[:-i])
    array.sort()
    output_string = ""
    for _,value in enumerate(array):
        output_string+=value[-1]
    position=array.index(input_string)+1
    return output_string, position

def inverse_bwt(input_string, position):
    """
    Function to transform [string + position] to string
    """
    tmp_arr1 = list(input_string)
    tmp_arr2 = tmp_arr1.copy()
    tmp_arr2.sort()
    for i,_ in enumerate(input_string):
        if i == len(input_string)-1:
            break
        for j,value in enumerate(tmp_arr1):
            tmp_arr1[j]=value+tmp_arr2[j][-1]
        tmp_arr2 = tmp_arr1.copy()
        tmp_arr2.sort()
    return tmp_arr2[position-1]

def main_gray(value_range,width):
    """
    Uloha 1
    """
    print("BCD > Gray")
    for i in range(value_range):
        binary_val = dec2bin(i,width)
        gray = bcd2gray(binary_val)
        dec = bin2dec(gray)
        print(str(i).rjust(5),"=",binary_val,"=>",gray,"=", str(dec).ljust(5))

def main_bcd(value_range,width):
    """
    Uloha 1
    """
    print("Gray > BCD")
    for i in range(value_range):
        binary_val = dec2bin(i,width)
        bcd =gray2bcd(binary_val)
        dec = bin2dec(bcd)
        print(str(i).rjust(5),"=",binary_val,"=>",bcd,"=", str(dec).ljust(5))




def main_mtf():
    """
    Uloha 2
    """
    original_string = load_from_stdin("Zadejte text pro MTF:")
    if original_string!="":
        encoded=mtf(original_string)
        decoded = ftm(encoded)
        print(original_string, "=>", encoded, "=>", decoded)
    else:
        print("Nečitelný text")
    print("\n")
def main_bwt():
    """
    Uloha 3
    """
    original_string = load_from_stdin("Zadejte text pro BWT:")
    if original_string!="": 
        encoded=bwt(original_string)
        decoded=inverse_bwt(encoded[0],encoded[1])
        print(original_string, "=>", encoded[0],f" {encoded[1]}.Řádek", "=>", decoded)
    else:
        print("Nečitelný text")
    print("\n")

if __name__=="__main__":
    #main_bcd(8,8)
    main_gray(8,8)
    main_mtf()
    main_bwt()
