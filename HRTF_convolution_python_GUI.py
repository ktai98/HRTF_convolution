import numpy as np
import mylib_HRTF as myHRTF
import PySimpleGUI as sg
import os
import sys


exedir = os.path.dirname(sys.argv[0])

def main():
    #sg.theme('DarkAmber')
    paramframe_layout = [   [sg.Text('音声開始時の水平角度(0度で正面、90度で真右から回転が始まります)')],
                            [sg.Slider(range=(0,355), resolution=5, default_value=0, orientation='h',key='angle_h', expand_x=True)],
                            [sg.Text('')],
                            [sg.Text('回転スピード(0で静止します)')],
                            [sg.Slider(range=(0,100), default_value=50, orientation='h',key='turnspeed',expand_x=True)]
    ]

    button_column_layout = [[sg.Button('　出力　',key='output'), sg.Button('　終了　',key='exit')]]

    layout = [  [sg.Text("音源の方向を変えるファイルを選択してください")],
                [sg.Text("変換元ファイル名"), sg.Input(), sg.FileBrowse('ファイルを選択',key='inputFilePath')],
                [sg.Text("出力ファイル名　"), sg.InputText(default_text='output',key='outputFileName'),sg.Text('.wav')],
                [sg.Frame('パラメータ設定',layout=paramframe_layout)],
                [sg.Column(button_column_layout,element_justification='left',expand_x=True)]
    ]

    window = sg.Window('音声ぐるぐる変換アプリ',layout=layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'exit':

            break

        if event == 'output':
            input_path = values['inputFilePath']
            if input_path == '':
                sg.popup('変換元ファイルを指定してください')
            else:
                outputdir = exedir+'/output/'
                # outputディレクトリが存在しない場合、ディレクトリを作成する
                if not os.path.exists(outputdir):
                    os.makedirs(outputdir)
                output_path = outputdir+values['outputFileName']+'.wav'
                turn_speed = values['turnspeed']
                default_angle = values['angle_h']
                # HRTF音声生成＆保存
                result = save_conv_music(input_path, output_path, turn_speed, default_angle)
                if result==True:
                    sg.popup('出力が成功しました')
                elif result == -1:
                    sg.popup('入力音源は1chまたは2chの音源データにのみ対応しています')
                elif result == -2:
                    sg.popup('ファイルが正常に出力されませんでした')
                else:
                    sg.popup('不明なエラーが発生しました')

    window.close()



def save_conv_music(open_path, save_path, speed, default_angle_h):
    # 読みこみファイル #
    #HRTFpath ='./full/elev0/'
    HRTFpath = exedir+'/full/elev0/'
    default_angle_h = int(default_angle_h)
    late_speed = speed/50
    
    try:
        s, channels, sampwitdh, fs, frames = myHRTF.audioread(open_path)

        if channels == 1:
            s = s.squeeze()
        elif channels == 2:
            s = s[1][:].squeeze() #L-chだけにする
        else:
            #print("1chまたは2chの音源データにのみ対応しています")
            return -1
        
        ss = np.zeros(shape=(2, len(s)+512-1)) #これに畳みこんだ信号を入れていく
        
        flen = np.round(512) #フレーム長

        for n in range(int(np.round(len(s)/flen))):
            st = int(n*flen) #フレームの最初の点
            en = int((n+1)*flen) #フレームの最後の点
            s_cut = s[st:en] #信号をフレーム長だけ切る
            ang = (int(n*late_speed)*5 + default_angle_h) % 360
            fnam = HRTFpath+'L0e'+str(ang).zfill(3)+'a.wav'
            h, _, _, _, _ = myHRTF.audioread(fnam)
            h = h.squeeze()
            ss_cut = myHRTF.fftconv(s_cut, h)
            en2 = en+len(h)-1
            ss[0][st:en2] = ss[0][st:en2]+ss_cut

            fnam = HRTFpath+'R0e'+str(ang).zfill(3)+'a.wav' 
            h, _, _, _, _ = myHRTF.audioread(fnam)
            h = h.squeeze()
            ss_cut = myHRTF.fftconv(s_cut, h)
            en2 = en+len(h)-1
            ss[1][st:en2] = ss[1][st:en2]+ss_cut

        result = myHRTF.save_wav_float(save_path, ss, 2, sampwitdh, fs)
        return result
    except:
        #print("wavファイルの保存に失敗しました")
        return -2


if __name__ == "__main__":
    main()