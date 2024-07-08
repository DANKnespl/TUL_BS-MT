'''Wav header parser'''

import struct
import numpy as np
import matplotlib.pyplot as plt

class InconsistentException(Exception):
    """
    Inconsistent header exception
    """
    def __init__(self,message):
        self.message = "Nekonzistentní hlavička("+str(message)+")"
        super().__init__(self.message)

class HeaderValueException(Exception):
    """
    Inconsistent header exception
    """
    def __init__(self,message):
        self.message = "Porušena struktura hlavičky("+str(message)+")"
        super().__init__(self.message)


S0="data/cv01_dobryden.wav"
S1="data/cv02_wav_01.wav"
S2="data/cv02_wav_02.wav"
S3="data/cv02_wav_03.wav"
S4="data/cv02_wav_04.wav" #WAVE error
S5="data/cv02_wav_05.wav" #RIFF error
S6="data/cv02_wav_06.wav" #cut error
S7="data/cv02_wav_07.wav" #length error

def main(file):
    """
    Function to parse *.wav
    """
    with open(file, 'rb') as f:
        #head
        #kontrola formátu hlavičky
        if str(f.read(4))!= "b'RIFF'":
            raise HeaderValueException("RIFF")
        a1_length = struct.unpack('i', f.read(4))[0]
        if str(f.read(4))!= "b'WAVE'":
            raise HeaderValueException("WAVE")
        if str(f.read(4))!= "b'fmt '":
            raise HeaderValueException("fmt ")
        
        #kontrola validity dat v hlavičce
        af_length = struct.unpack('i', f.read(4))[0]
        if (af_length<16 or af_length> pow(256,4)):
            raise Exception("Velikost hlavičky mimo hranice *.wav")
        k_wave_format = struct.unpack('h', f.read(2))[0]
        channels = struct.unpack('h', f.read(2))[0]
        sample_freq = struct.unpack('i', f.read(4))[0]
        average_bps = struct.unpack('i', f.read(4))[0]

        block_size = struct.unpack('h', f.read(2))[0]
        if average_bps/sample_freq!=block_size:
            raise InconsistentException("průměrné B/s")

        sample_size = struct.unpack('h', f.read(2))[0]
        if block_size*8/channels != sample_size:
            raise InconsistentException("velikost bloku vzorků")
        
        #posun v souboru v případě hlavičky > 44B
        f.read(af_length-16)
        #kontrola formátu hlavičky
        if str(f.read(4))!= "b'data'":
            raise HeaderValueException("data")
        #kontrola konzistentních dat v hlavičce
        a2_length = struct.unpack('i', f.read(4))[0]
        if (a1_length-af_length-20)!= a2_length:
            raise InconsistentException("délka souboru")

        signal = np.zeros(int(a2_length/(sample_size/8)))
        print(len(signal))
        try:
            for i, _ in enumerate(signal):
                if sample_size==8:
                    signal[i] = struct.unpack('B', f.read(1))[0]
                elif sample_size==16:
                    signal[i] = struct.unpack('h', f.read(2))[0]
                elif sample_size==32:
                    signal[i] = struct.unpack('i', f.read(4))[0]
                elif sample_size==64:
                    signal[i] = struct.unpack('d', f.read(8))[0]
                else:
                    raise Exception("Nevalidní velikost vzorku")
        except Exception as exc:
            raise Exception("Chybějící data v datové části") from exc
            #raise Exception("Fuckers stole my data, cant have shit in WAV") from exc
    output(a1_length,af_length,k_wave_format,channels,sample_freq,average_bps,block_size,sample_size,a2_length,signal)


def output(a1_length,af_length,k_wave_format,channels,sample_freq,average_bps,block_size,sample_size,a2_length,signal):
    """
    HID output
    """
    fig = plt.figure(figsize=(9,5))
    match k_wave_format:
        case 0:
            k_format = "WAVE_FORMAT_UNKNOWN"
        case 1:
            k_format = "WAVE_FORMAT_PCM"
        case 2:
            k_format = "WAVE_FORMAT_ADPCM"
        case 5:
            k_format = "WAVE_FORMAT_IBM_CVSD"
        case 6:
            k_format = "WAVE_FORMAT_ALAW"
        case 7:
            k_format = "WAVE_FORMAT_MULAW"
        case _:
            k_format = k_wave_format

    time_slices = np.arange(len(signal)/channels).astype(float)/(sample_freq)
    if channels==1:
        channel_plots = fig.subplots(1,1)
    else:
        channel_plots = fig.subplots(int(channels/2),2)
    for n in range(0,channels):
        sig = signal[n::channels]
        if channels == 1:
            channel_plots.plot(time_slices, sig)
            channel_plots.set_title("Channel "+str(n+1))
            channel_plots.set_xlabel('t[s]')
            channel_plots.set_ylabel('A[-]')
        else:
            if channels==2:
                channel_plots[n].plot(time_slices, sig)
                channel_plots[n].set_title("Channel "+str(n+1))
            else:    
                channel_plots[int(n/2)][n%2].plot(time_slices, sig)
                channel_plots[int(n/2)][n%2].set_title("Channel "+str(n+1))
            for chan in channel_plots.flat:
                #if chan == channel_plots.flat[0]:
                chan.set(ylabel='A[-]')
                chan.set(xlabel='t[s]')

    #output
    print("A1 = "+str(a1_length)+"B do konce souboru")
    print("AF = "+str(af_length)+"B do konce Format části hlavičky")
    print("formát = "+k_format)
    print("počet kanálů = "+str(channels))
    print("Vzorkovací frekvence = "+str(sample_freq)+"Hz")
    print("Průměrný počet bytů/s = "+str(average_bps))
    print("Velikost bloků vzorků = "+str(block_size)+"B")
    print("Velikost vzorků = "+str(sample_size)+"b")
    print("A2 = "+str(a2_length)+"B do konce souboru")
    plt.show()

if __name__ == '__main__':
    main(S1)
