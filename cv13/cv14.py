"""
Functions for inverse code finding and fixing singular transport
mistake
"""
import math
import random
import time
import sys


mainPrimeList = []


def euklid_alg(prime1,prime2):
    """
    Function to calculate largest common divisor
    """
    numerator=max(prime1,prime2)
    denumerator=min(prime1,prime2)
    n=0
    while denumerator>0:
        tmp=numerator%denumerator
        numerator=denumerator
        denumerator=tmp
        n+=1
    return numerator

def generate_keys(primes):
    """
    Generates two arrays:
    private_key
        index 0 - n 
        index 1 - d
    public_key
        index 0 - n 
        index 1 - e
    """
    prime1 = primes[0]
    prime2= primes[1]
    eulerMax = (prime1-1)*(prime2-1)
    n=prime1*prime2
    primeList=[]
    if eulerMax<15000000:
        primeList=primes_method5(eulerMax,False)
    else:
        primeList=get_primes(0,eulerMax)
    #140s
    e=primeList[random.randint(1,len(primeList))]
    while euklid_alg(e,eulerMax)!=1:
        print("-")
        e=primeList[random.randint(1,len(primeList))]
    d=pow(e,-1,eulerMax)
    pub_key=[n,e]
    priv_key=[n,d]
    print("n =",n,"\ne =",e,"\nd =",d,"\ninput primes = ",primes)
    return [priv_key,pub_key]

def crypt(value,key):
    """
    Function to encrypt/decrypt
    """
    out = []
    if type(value)==int:
        return pow(value,key[1],key[0])
    for _,val in enumerate(value):
        out.append(pow(val,key[1],key[0]))
    return out
    #return value**key[1]%key[0]

def get_primes(lower,upper):
    """
    Function to get array of primes in interval
    """
    lst=[]
    #with open("primes.txt") as f:
    #    lst = [int(x) for x in f.read().split()]
    lst = [x for x in mainPrimeList if lower < x < upper]
    return lst

def load_from_stdin(message):
    """
    Loads and validates data from a line in stdin
    """
    print(message)
    tmp = sys.stdin.readline().strip()
    return tmp

def primes_method5(n,w):
    """
    https://stackoverflow.com/questions/11619942/print-series-of-prime-numbers-in-python
    """
    out = list()
    sieve = [True] * (n)
    for p in range(2, n):
        if (sieve[p] and sieve[p]%2==1):
            out.append(p)
            for i in range(p, n, p):
                sieve[i] = False
    if w:
        with open('primes.txt', 'a') as fid:
            for line in out:
                fid.write(f'{line}\n')
    return out




def string_to_int_array(in_string):
    """
    Function to turn string to array of ints
    """
    return [ord(char) for char in in_string]

def int_array_to_string(arr):
    """
    Function to turn array of ints to string
    """
    return ''.join([chr(x) for x in arr])

def get_core_primes(lower,upper):
    primeList=get_primes(lower,upper)
    primes = []
    primes.append(primeList[random.randint(1,len(primeList))])
    primes.append(primeList[random.randint(1,len(primeList))])
    while(primes[0]==primes[1]):
        primes[1]=primeList[random.randint(1,len(primeList))]
    return primes[0],primes[1]

def enc_dec(og_text, key1, key2, pub_to_priv):
    """
    Main printing function
    """
    type1 = ""
    type2 = ""
    if pub_to_priv:
        type1="=> public =>\n"
        type2="=> private =>\n"
    else:
        type1="=> private =>\n"
        type2="=> public =>\n"
    print("Original:",og_text)
    print(type1+"Encoded:",str(crypt(string_to_int_array(og_text),key1)))
    print(type2+"Decoded:",int_array_to_string(crypt(crypt(string_to_int_array(og_text),key1),key2)))


if __name__=="__main__":
    with open("data/primes.txt") as f:
        mainPrimeList = [int(x) for x in f.read().split()]
    private_key, public_key=generate_keys(get_core_primes(1000,10000))
    print("\nprivate:",private_key,"\npublic:",public_key,"\n")
    text=""
    while text not in ["exit","quit"]:
        text = load_from_stdin("Zadejte text pro zakódování:")
        st = time.time()
        enc_dec(text,private_key,public_key,False)
        print("")
        enc_dec(text,public_key,private_key,True)
        print("\nVýpočetní čas:",time.time()-st,"sekund\n\n")


#huff mtf aritm lzw bwt