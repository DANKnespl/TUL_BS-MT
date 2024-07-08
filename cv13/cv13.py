"""
Functions for inverse code finding and fixing singular transport
mistake
"""
import math

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
    if binary!="":
        for expon,value in enumerate(binary[::-1]):
            dec+=int(value)*math.pow(2,expon)
        return int(dec)
    return "---"


def invert(binary):
    """
    Returns inverted binary number
    """
    binary_list = list(binary)
    output = ""
    for i,val in enumerate(binary_list):
        if val == "0":
            output+="1"
        else:
            output+="0"
    return output

def compare_seq(seq1,seq2):
    """
    Returns the number of same bits of two binary numbers
    """
    count=0
    for i,val in enumerate(seq1):
        if val == seq2[i]:
            count+=1
    return count

def compare_seq_array(seq1,seq2):
    """
    Returns mask of two binary numbers as NXOR
    """
    output=""
    for i,val in enumerate(seq1):
        if val == seq2[i]:
            output+="1"
        else:
            output+="0"
    return output

def is_even(seq):
    """
    Checks if the number of zeros in binary number is even
    """
    count=0
    for _,val in enumerate(seq):
        if val == "0":
            count+=1
    return count%2==0

def is_fixable(seq):
    """
    Checks if the number of mistakes in mask is smaller then one
    """
    count=0
    for _,val in enumerate(seq):
        if val == "0":
            if count>0:
                return False
            count+=1
    return True

def fixInput(input1,input2):
    """
    Returns most likely value that has been sent from two 
    received values
    """
    inverted2 = invert(input2)
    even_main = True
    second_value = input2
    if compare_seq(input1,input2)<compare_seq(input1,inverted2):
        even_main = False
        second_value = inverted2
    same_values = compare_seq_array(input1,second_value)
    if not is_fixable(same_values):
        return ""
    if is_even(input1)==even_main:
        return input1
    return second_value

def formating(bin, pos):
    match pos:
        case 1:
            return "first: %s (%d)" % (bin,bin2dec(bin))
        case 2:
            return "second: %s (%d)" % (bin,bin2dec(bin))
        case _:
            return "=> %s (%s)" % (bin, bin2dec(bin))


if __name__=="__main__":
    array = [160,223,64,65,128,126,130,126,13,13,14,256-15,14,12,14,256-13,128,128]
    bitArray = []
    for _,val in enumerate(array):
        bitArray.append(dec2bin(val,8))
    for i in range(math.floor(len(bitArray)/2)):
        print(formating(bitArray[i*2],1),formating(bitArray[i*2+1],2),
              formating(fixInput(bitArray[i*2],bitArray[i*2+1]),-1))

