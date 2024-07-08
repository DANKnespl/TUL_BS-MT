import re

def koincidence(string_in):
    abec={}
    for _,val in enumerate(string_in):
        if val in abec:
            abec[val]=abec[val]+1
        else:
            abec[val]=1
    suma=0
    for _,val in enumerate(abec):
        suma+=abec[val]*(abec[val]-1)
    out=suma/(len(string_in)*(len(string_in)-1))
    if abs(0.06027-out)<abs(0.06689-out):
        return "CZ", "domov"
    return "EN", "roads"

def cz(string_in):
    potential = []
    for i in range(len(string_in)-4):
        current= string_in[i:i+5]
        if current[1]==current[3] and current[0]!=current[-1] and current[0]!=current[2] and current[1]!=current[2] :
            potential.append(current)
    return list(dict.fromkeys(potential))

def en(string_in):
    potential = []
    for i in range(len(string_in)-4):
        current= string_in[i:i+5]
        if len(list(dict.fromkeys(current)))==len(current):
            potential.append(current)
    return list(dict.fromkeys(potential))


if __name__=="__main__":
    #not finished me thinks
    print(koincidence("TEWFYWYNKUCOMOWOJTEWFYWYNKUCOMOWOJOWOJKXCKBUKDOTYDKNOVRYZKXYDTKBIUCWOJDOFUKBKTOCSFUCONKCFRMKXSVKUCYZSWECIBYLRMKXSMEVYZSMERKNYFTEWFYWYNONUTEWFYWYNONU"))
    print(koincidence("OMXOBOPPSNORDVVKONKWCKRDKRDNXKILNOVVOFKBDCCOVOXYORDUYYDSSNXKNYYGKXSNOQBOFSNCNKYBYGD"))
    print(cz("TEWFYWYNKUCOMOWOJTEWFYWYNKUCOMOWOJOWOJKXCKBUKDOTYDKNOVRYZKXYDTKBIUCWOJDOFUKBKTOCSFUCONKCFRMKXSVKUCYZSWECIBYLRMKXSMEVYZSMERKNYFTEWFYWYNONUTEWFYWYNONU"))
    print(en("OMXOBOPPSNORDVVKONKWCKRDKRDNXKILNOVVOFKBDCCOVOXYORDUYYDSSNXKNYYGKXSNOQBOFSNCNKYBYGD"))