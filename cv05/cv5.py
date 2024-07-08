"""
LZW encode/decode
"""
import struct
from difflib import SequenceMatcher
from pathlib import Path
import math
import numpy as np
#Obecné funkce

def open_file(input_file_path):
    """
    opens file, reads by bytes as int, returns string
    doesnt generate minimal alphabet
    """
    file_path = Path(input_file_path)
    file_stats = file_path.stat()
    output=""
    with open(input_file_path, 'rb') as f:
        for _ in range(file_stats.st_size):
            output=output+str(struct.unpack('B', f.read(1))[0])
    return output

def generate_alphabet(input_string):
    """
    Generates alphabet of given string, stores frquencies of chars
    """
    alphabet={}
    for char in input_string:
        if char in alphabet:
            alphabet[char]+=1
        else:
            alphabet[char]=1
    return alphabet

def generate_frequency(input_string,al):
    """
    Generates frequency of chars in string.
    """
    alphabet=generate_alphabet(input_string)
    for letter in al:
        alphabet[letter]=0
    return alphabet

def generic_output(input_string,encoded, decoded):
    """
    Prints string to be encoded, encoded data to be written to file and decoded text
    """
    print("     Vstupní text:       ",input_string)
    print("     Dekomprimovaný text:", decoded)
    print("     Komprimovaná data:  ", encoded)

def different_value_index(fl1,fl2):
    """
    Compares decimal part of two floats and returns the position of the first different 
    """
    sm=SequenceMatcher()
    SequenceMatcher.set_seqs(sm,str(fl1-math.floor(fl1)),str(fl2-math.floor(fl2)))
    return SequenceMatcher.find_longest_match(sm).size-1

#LZW------------------------------------------------------------------------------------------------
def lzw_encode(input_string,al):
    """
    Encodes text using LZW, min value = 0
    """
    alphabet=[]
    if al ==[]:
        alph=generate_alphabet(input_string)
    else:
        alph=generate_frequency(input_string,al)

    for key,_ in alph.items():
        alphabet.append(key)
        alphabet.sort()
    phrases = np.copy(alphabet).tolist()
    output=[]
    while len(input_string)>0:
        found_index=len(phrases)
        for i in range(len(phrases)-1,-1,-1):
            if input_string.find(phrases[i]) == 0:
                if input_string[:len(phrases[i])+1] not in phrases:
                    phrases.append(input_string[:len(phrases[i])+1])
                found_index=i
                output.append(i)
                break
        try:
            input_string = input_string[len(phrases[found_index]):]
        except IndexError:
            input_string=""
    return output, phrases, alphabet

def lzw_decode(input_array,alphabet):
    """
    Decodes int array using LZW, min value = 0
    """
    phrases = dict(enumerate(map(str, alphabet)))
    previous=input_array[0]
    lowest_new=len(phrases)
    for i in range(1,len(input_array)):
        if input_array[i] in phrases:
            phrases[lowest_new] = phrases[previous]+phrases[input_array[i]][0:1]
        else:
            phrases[input_array[i]] = phrases[previous]+phrases[previous][0:1]
        previous=input_array[i]
        lowest_new+=1
    output=""
    for _, phrase in enumerate(input_array):
        output+=phrases[phrase]
    return output, phrases

def lzw_full(input_string, alphabet, show_phrases):
    """
    Encodes and decodes input_string using lzw, writes out input_string,
     encoded data as array to be written to file, decoded string. Can writeout phrases.
    """
    encoded, encoded_phrases, new_alphabet = lzw_encode(input_string, alphabet)
    decoded, decoded_phrases = lzw_decode(encoded, new_alphabet)
    print("\nLZW Algoritmus")
    generic_output(input_string,encoded,decoded)
    if show_phrases:
        print("Fráze při komprimaci: ")
        for i, phrase in enumerate(encoded_phrases):
            print("     ",i,"=",phrase)
        print("\nFráze při dekomprimaci: ")
        for key,value in decoded_phrases.items():
            print("     ",key,"=",value)

#RLE------------------------------------------------------------------------------------------------
def rle_encode(input_string):
    """
    Encodes text using RLE
    """
    output = []
    last = [0,""]
    for char in input_string:
        if char==last[1]:
            last[0]+=1
        else:
            if last[0]!=0:
                output.extend(last)
            last=[1,char]
    output.extend(last)
    return output

def rle_decode(input_string):
    """
    Decodes input_string array using RLE.
    """
    if len(input_string)%2 !=0:
        return "invalid input"
    output=""
    for i in range(0,len(input_string),2):
        for _ in range(input_string[i]):
            output+=str(input_string[i+1])
    return output

def rle_full(input_string):
    """
    Encodes and decodes input_string using rle, writes out input_string,
     encoded data as array to be written to file, decoded string.
    """
    encoded=rle_encode(input_string)
    decoded=rle_decode(encoded)
    print("\nRLE Algoritmus")
    generic_output(input_string, encoded, decoded)

#Huffman--------------------------------------------------------------------------------------------

def huffman_encode(input_string,al):
    """
    Encodes text using Huffman
    """
    table=[]
    codes={}
    if al ==[]:
        alphabet=generate_alphabet(input_string)
    else:
        alphabet=generate_frequency(input_string,al)
    for key,value in alphabet.items():
        alphabet[key]=value/len(input_string)
        codes[key]=""
    alphabet=sorted(alphabet.items(), key=lambda x:x[1],reverse=True)

    table.append(alphabet)
    while len(table[len(table)-1])>2:
        alph=dict(table[len(table)-1])
        tmp1=alph.popitem()
        tmp2=alph.popitem()
        k=tmp1[0]+tmp2[0]
        v=tmp1[1]+tmp2[1]
        alph[k]=v
        alph=sorted(alph.items(), key=lambda x:x[1],reverse=True)
        table.append(alph)

    for i in range(len(table)-1,-1,-1):
        alph=dict(table[i])
        tmp1=alph.popitem()
        tmp2=alph.popitem()
        for letter in codes:
            if tmp1[0].find(letter)!=-1:
                codes[letter]+="0"
            if tmp2[0].find(letter)!=-1:
                codes[letter]+="1"
    output=""
    delimited_output=[]
    for letter in input_string:
        delimited_output.append(codes[letter])
        output+=codes[letter]
    return output, codes, delimited_output, table


def huffman_decode(input_string,codes):
    """
    Decodes input_string using huffman, needs codes used in encoding.
    """
    tmp=input_string
    output=""
    while len(tmp)>0:
        for key,value in codes.items():
            if tmp.find(value)==0:
                tmp=tmp[len(value):]
                output+=str(key)
    return output

def huffman_full(input_string, alphabet, show_table):
    """
    Encodes and decodes input_string using huffman, writes out input_string,
     encoded data as array to be written to file, decoded string.
     Can writeout table used in compression.
    """
    encoded, codes, delimited_output, table = huffman_encode(input_string,alphabet)
    decoded=huffman_decode(encoded,codes)
    print("\nHuffmanův Algoritmus")
    generic_output(input_string, delimited_output, decoded)
    print("     Seznam kódů:")
    for key,value in codes.items():
        print("        ",key,"=",value)
    if show_table:

        table_print = "        "
        print("     Komprimační tabulka:")
        for row in range(len(table[0])):
            for column_id,column in enumerate(table):
                if len(table[column_id])>row:
                    column_offset=len(sorted(column,key=lambda x: len(x[0]),reverse=True)[0][0])
                    table_cell=table[column_id][row]
                    table_print+="| "+table_cell[0].ljust(column_offset+2)
                    table_print+=" "+str(format(table_cell[1],".4f"))
            table_print+="\n        "
        print(table_print)

#Arithmetic-----------------------------------------------------------------------------------------
def arithmetic_encode(input_string,al):
    """
    Encodes text using Arithmetic
    """
    codes={}
    if al ==[]:
        alphabet=generate_alphabet(input_string)
    else:
        alphabet=generate_frequency(input_string,al)
    for key,value in alphabet.items():
        alphabet[key]=value/len(input_string)
        codes[key]=""
    alphabet=dict(sorted(alphabet.items()))
    last_letter=0
    for key,value in alphabet.items():
        new_letter=last_letter+value
        alphabet[key]=last_letter,new_letter
        last_letter=new_letter
    interval=[0,1]
    for character in input_string:
        character_lower_boundry=alphabet[character][0]
        character_higher_boundry=alphabet[character][1]
        next_interval_lower_boundry=interval[0]+character_lower_boundry*(interval[1]-interval[0])
        next_interval_higher_boundry=interval[0]+character_higher_boundry*(interval[1]-interval[0])

        interval = [next_interval_lower_boundry, next_interval_higher_boundry]
    difference_pointer=different_value_index(interval[0],interval[1])
    output=math.ceil(interval[0]*pow(10,difference_pointer))/pow(10,difference_pointer)
    return output, alphabet, interval, len(input_string)


def arithmetic_decode(input_value, alphabet, string_length):
    """
    Decodes input_string using arithmetic, needs codes used in encoding.
    """
    output=""
    status=0
    interval=[0,1]
    for _ in range(string_length):
        current_character= (input_value-interval[0])/(interval[1]-interval[0])
        for key,value in alphabet.items():
            if current_character>= value[0] and current_character< value[1]:
                character_lower_boundry=value[0]
                character_higher_boundry=value[1]
                output+=key
                break
        next_interval_lower_boundry=interval[0]+character_lower_boundry*(interval[1]-interval[0])
        next_interval_higher_boundry=interval[0]+character_higher_boundry*(interval[1]-interval[0])
        interval=[next_interval_lower_boundry,next_interval_higher_boundry]
        #print(interval)
        try:
            1/(next_interval_higher_boundry-next_interval_lower_boundry)
        except ZeroDivisionError:
            status=1
            break
    return output,status

def arithmetic_full(input_string, al, show_alphabet):
    """
    Encodes and decodes input_string using arithmetic, writes out input_string,
     encoded data as array to be written to file, decoded string.
     Can writeout table used in compression.
    """
    print("\nAritmetické kódování")
    encoded, alphabet, interval, string_length=arithmetic_encode(input_string,al)
    decoded,status=arithmetic_decode(encoded,alphabet,string_length)
    if status==1:
        generic_output(input_string,encoded,decoded+"\n     Chyba při dekódování - nedostatečná přesnost\n")
    else:
        generic_output(input_string,encoded,decoded)
    print("     Konečný komprimační interval", interval)
    if show_alphabet is True:
        print("     Intervaly hodnot")
        for key,value in alphabet.items():
            print("        ",key,"=",f"<{value[0]:.2f}, {value[1]:.2f})")

if __name__ == '__main__':
    LZW_IN_STRING=open_file("data/Cv05_LZW_data.bin")
    RLE_IN_STRING=open_file("data/Cv06_RLE_data.bin")
    ARITHMETIC_IN_STRING=open_file("data/Cv07_Aritm_data.bin")
    TEST_STRING="papaja"
    #TEST_STRING="pana"
    #rle_full(TEST_STRING)
    huffman_full(TEST_STRING, [], True)
    #arithmetic_full(TEST_STRING, [], True)

    lzw_full(LZW_IN_STRING, [], False)
    #rle_full(RLE_IN_STRING)
    #huffman_full(TEST_STRING, [], True)
    #huffman_full(LZW_IN_STRING, [], True)
    #arithmetic_full(ARITHMETIC_IN_STRING, [], True)
    #lzw_full("popokatepetl", [], True)
    #huffman_full("popokatepetl",[],True)
    
