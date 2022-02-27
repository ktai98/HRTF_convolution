#####################################
音声ぐるぐる変換アプリ 説明書

作成者：紺野大樹
初版作成日：2022/01/09
#####################################


◆説明
本ソフトウェアは、入力された音声ファイル(.wav)を「頭の周りをぐるぐると回っているような音声」に変換するソフトウェアです。
現在、設定可能なパラメータとして「回転開始時の水平角度」と「回転スピード」を指定できます。
回転スピードを0にすることにより、出力音声が聞こえてくる方向を一方向に固定することも可能です。
音源方向の変換原理として、HTRF(Head Related Transfer Function, 頭部伝達関数)を用いているため、音源方向の聞こえ方には比較的大きな個人差があります。
イヤホンまたはヘッドフォン推奨です。


◆使い方
・「HRTF_convolution.exe」を起動してください。
・「変換元ファイル名」に変換したい音声ファイルのパスを入力してください。「ファイルを選択」から直接選択することもできます。
・「出力ファイル名」に、出力されるファイルの名前を指定してください。デフォルトでは「output.wav」となっています。拡張子.wavは自動的に追加されますので入力の必要はありません。
・「パラメータ設定」より、出力される音声のパラメータを設定できます。とりあえず試すだけならデフォルト設定で問題ありません。
・パラメータの設定が終わったら、ウィンドウ左下の「出力」ボタンをクリックします。
・「HRTF_convolution.exe」と同じフォルダに「output」フォルダが作成され、その中に変換後の音声ファイルが出力されます。


◆注意点
・出力音声はヘッドフォンまたはイヤホンで聞くことをお勧めいたします。
・出力音声に「ぷつぷつ」あるいは「ぶーん」といったノイズが入ることがあります。（原因として、畳み込み時にオーバーラップ処理をしていない、残響波形の一部が切り捨てられている、などが考えられますが、はっきりした原因は不明です）
・出力音声の形式は入力音声と同じですが、入力音声が1ch(モノラル)の場合のみ、チャンネル数が2ch(ステレオ)に変換されます。
・入力音声がステレオの場合、L-ch(左耳から聞こえる音声)のみを使用するため、元の音声と聞こえ方が変わってしまう場合があります。


◆音声の出力が上手くいかない場合
・「HRTF_convolution.exe」と同じ階層にHTRF波形のフォルダ「full」が存在している必要があります。
・入力音声の形式は「wavファイルである」「1ch(モノラル)または2ch(ステレオ)である」「量子化ビット数(サンプリングビット数)が8bit/16bit/32bitのいずれかである」のすべてを満たしている必要があります。「24bitサンプリング」のwavファイルには現在対応しておりません。


◆判明している問題点＆改善点
・設定可能なパラメータとして「垂直方向の回転角度」が追加可能
・24bitサンプリング等、非対応音声への対応
・ぷつぷつノイズの改善、除去
・リアルタイムで音声を聞きながら出力音声の角度を変更できる機能の追加(本来こちらをメイン機能として目指し、音源角度変更までは実装できたが、ぷつぷつノイズが大きくなりすぎて耳障りであったため断念)


◆使用素材
利用規約・サイトを熟読し、利用可能であると判断した上で使用しています。
提供してくださった方々に深く感謝いたします。

・HRTF音声
引用:Bill, Gardner. "Hrtf measurements of a kemar dummy-head microphone." MIT Media Lab. Perceptual Computing-Technical Report 280 (1994): 1-7.
使用音源:full.zip
URL:https://sound.media.mit.edu/resources/KEMAR.html

・入力音声サンプル
サイト名:フリーBGM　Music with myuu
使用音源:loop2.wav
URL:https://www.ne.jp/asahi/music/myuu/wave/wave.htm


◆更新履歴
2022/01/09 .exeファイル化、本ファイル(readme)作成

2022/02/27 ソースコードのみgithubに公開
