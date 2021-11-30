import matplotlib.pyplot as plt
import base64
from io import BytesIO

#プロットしたグラフを画像データとして出力するための関数
def Output_Graph():
	buffer = BytesIO()                   #バイナリI/O(画像や音声データを取り扱う際に利用)
	plt.savefig(buffer, format="png")    #png形式の画像データを取り扱う
	buffer.seek(0)                       #ストリーム先頭のoffset byteに変更
	img   = buffer.getvalue()            #バッファの全内容を含むbytes
	graph = base64.b64encode(img)        #画像ファイルをbase64でエンコード
	graph = graph.decode("utf-8")        #デコードして文字列から画像に変換
	buffer.close()
	return graph

#グラフをプロットするための関数
#決定率
def Plot_Graph_attack(x,y):
	plt.switch_backend("AGG")          #スクリプトを出力させない
	plt.figure(figsize=(10,5))         #グラフサイズ
	plt.plot(x,y,marker='o')           #グラフ作成
	# plt.xticks(rotation=45)          #X軸値を45度傾けて表示
	plt.title("attackdecisionrate")    #グラフタイトル
	plt.xlabel("")                     #xラベル
	plt.ylabel("rate")                 #yラベル
	plt.xlim(0.5,10.5)                 #x軸範囲
	plt.ylim(0,1)             	       #y軸範囲
	plt.tick_params(labelbottom=False) #x軸ラベルを消す    
	plt.tight_layout()                 #レイアウト
	graph = Output_Graph()             #グラフプロット
	return graph

#グラフをプロットするための関数
#返球率
def Plot_Graph_receive(x,y):
	plt.switch_backend("AGG")          #スクリプトを出力させない
	plt.figure(figsize=(10,5))         #グラフサイズ
	plt.plot(x,y,marker='o')           #グラフ作成
	plt.title("receiverate")           #グラフタイトル
	plt.xlabel("")                     #xラベル
	plt.ylabel("rate")                 #yラベル
	plt.xlim(0.5,10.5)                 #x軸範囲
	plt.ylim(0,1)                      #y軸範囲
	plt.tick_params(labelbottom=False) #x軸ラベルを消す              
	plt.tight_layout()                 #レイアウト
	graph = Output_Graph()             #グラフプロット
	return graph

#グラフをプロットするための関数
#サーブ効果率
def Plot_Graph_effect(x,y):
	plt.switch_backend("AGG")          #スクリプトを出力させない
	plt.figure(figsize=(10,5))         #グラフサイズ
	plt.plot(x,y,marker='o')           #グラフ作成
	plt.title("effectrate")					   #グラフタイトル
	plt.xlabel("")                     #xラベル
	plt.ylabel("rate")                 #yラベル
	plt.xlim(0.5,10.5)                 #x軸範囲
	plt.ylim(0,100)                    #y軸範囲
	plt.tick_params(labelbottom=False) #x軸ラベルを消す          
	plt.tight_layout()               	 #レイアウト
	graph = Output_Graph()             #グラフプロット
	return graph