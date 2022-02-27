
import wave
import numpy as np


def binary2float(binary, sampwidth, ch_num):
    if sampwidth==1: #8-bit uint (1サンプル当たり1バイト)
        data=np.frombuffer(binary, dtype=np.uint8)
        data = data - 128 #8bit=255, unsignedをsignedに変換
    elif sampwidth==2: #16bit int (1サンプル当たり2バイト)
        data=np.frombuffer(binary, dtype=np.int16)
    elif sampwidth==4: #32bit int (1サンプル当たり4バイト)
        data=np.frombuffer(binary, dtype=np.int32)
    else:
        print("Not availavle \'24-bit int\' sampring width.")
        return 0
    # 各サンプルを-1～1の範囲に収まるよう調整
    data = data.astype(np.float32)/(2**(8*sampwidth-1))

    #全チャンネルが1配列に格納されているため、各チャンネルに分離
    sample_len = data.shape[0] // ch_num
    data_ch = np.zeros((ch_num, sample_len), dtype=np.float32)
    for i in range(ch_num):
        data_ch[i] = data[i::ch_num] #チャンネル数分飛ばしながらサンプルを取得

    return data_ch


def float2binary(data_ch, sampwidth):
    ch_num = data_ch.shape[0]
    #チャンネル別の信号を1次元(交互)に並べる
    data_1D = np.zeros((1,len(data_ch[0])*ch_num)).flatten()
    for i in range(ch_num):
        data_1D[i::ch_num] = data_ch[i]

    data_1D = data_1D*(2**(8*sampwidth-1)-1) #floatからintに変換

    #バイナリに変換
    if sampwidth==1:
        data_1D = data_1D+128
        #binary = data_1D.astype(np.float32).tobytes()
        binary = data_1D.astype(np.uint8).tobytes()
    elif sampwidth==2:
        #binary = data_1D.astype(np.float32).tobytes()
        binary = data_1D.astype(np.int16).tobytes()
        #print(len(binary))
    elif sampwidth ==4:
        #binary = data_1D.astype(np.float32).tobytes()
        binary = data_1D.astype(np.int32).tobytes()
    else:
        print("not support data type.")

    return binary

    
def open_wav(open_path):
    '''
    wavファイルを開き、ストリームと各種パラメータを返します
    
    return stream, channels, saplwidth, rate, frames
    '''
    try:
        wf = wave.open(open_path,'r')
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        rate = wf.getframerate()
        frames = wf.getnframes()
        #params = wf.getparams()
        return wf, channels, sampwidth, rate, frames

    except:
        print("wav fileが開けませんでした:"+open_path)
        return None


def audioread(open_path):
    '''
    wavファイルをMATLABライクに読みこみます。ただし、データの形は(チャンネル数, サンプル数)になります

    return float_data, channels, sampwidth, framerate, framelength
    '''
    wf, channels, sampwidth, rate, frames = open_wav(open_path)
    binary_data = wf.readframes(frames)
    float_data = binary2float(binary_data, sampwidth, channels)

    return float_data, channels, sampwidth, rate, frames


def save_wav_bi(save_path, binary_data, channels, sampwitdth, rate) -> bool:
    try:
        if len(binary_data) == 0:
            return False
        with wave.open(save_path, "wb") as ww:
            params = (channels, sampwitdth, rate, len(binary_data), 'NONE', 'not compressed')
            ww.setparams(params)
            ww.writeframes(binary_data)
        return True
    except:
        return False


def save_wav_float(save_path, float_data, channels, sampwitdth, rate) -> bool:
    try:
        binary_data = float2binary(data_ch=float_data, sampwidth=sampwitdth)
        result = save_wav_bi(save_path, binary_data, channels, sampwitdth, rate)
        return result
    except:
        return False


def fftconv(s1, s2):
    length = s1.shape[0]+s2.shape[0]
    #print(s2.shape)
    fftres = np.fft.rfft(s1, n=length ,axis=0) * np.fft.rfft(s2, n=length, axis=0)
    res = np.fft.irfft(fftres) * 0.5
    if np.amax(res) > 1.0:
        print(np.amax(res))
    if np.amin(res) < -1.0:
        print(np.amin(res))
    l = len(res)
    return res[:l-1] #なぜか畳み込み後の長さがlen(s1)+len(s2)-1にならないのでここで修正


def conv_2sig(frame, hL, hR):
    flen = len(frame)
    #frame = frame * np.hamming(512)
    #print(frame.shape)
    #print(hL.shape)
    #Lsig = np.convolve(frame,hL, mode='full')
    Lsig = fftconv(frame, hL)
    Lsig_frame = Lsig[:flen]
    #Lsig_remain = Lsig[flen:]

    #Rsig = np.convolve(frame,hR, mode='full')
    Rsig = fftconv(frame, hR)
    Rsig_frame = Rsig[:flen]
    #Rsig_remain = Rsig[flen:]
    
    #Lsig_frame = np.clip(Lsig_frame,-0.01,0.01)
    #Rsig_frame = np.clip(Rsig_frame,-0.01,0.01)
    sig = np.stack([Lsig_frame, Rsig_frame])
    #sig = np.stack([Lsig, Rsig])
    return sig