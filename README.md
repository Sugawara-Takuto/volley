# MyScore
バレーボール専用の選手成績記録アプリです。

テストアカウント<br>
ユーザー名 : test
パスワード : test

# 環境
使用言語 : Python 3.8.0, HTML, CSS
フレームワーク : Django
使用OS : Ubuntu 18.04

# 機能
<li>login,logout,signup機能</li>
<li>CRUD機能</li>
<li>成績のグラフ化</li>

# 工夫した点
<h2>入力のリルタイム化</h2>
成績の入力は後からやるのではなく試合中に試合を見ながら入力した方が便利です。<br>
よって、できるだけ便利に成績の入力が行えるよう工夫いたしました。<br>
<br>
1つはは選手入力の方法です。<br>
djangoでのfieldをPositiveIntegerFieldにすることで、入力欄の右側にボタンが表示されます。<br>
これにより数字を書き直す手間がなくボタンをクリックするだけでカウントできます。<br>
更に各確率を出す際、成功数と総数が必要となりますが、 入力では成功数と失敗数のみ入力させ、総数は内部で計算しています。<br>
これにより、各プレーに必要な入力が１回ずつとなります。<br>
<img src="https://user-images.githubusercontent.com/86762993/144860816-d353db3b-d1f0-49fe-aa48-d4fd5cae3b94.png" width="40%"><br>
<br>
２つ目は入力する選手の選択です。<br>
試合に出ていない選手は入力欄に出す必要がなく邪魔になるため、必要な選手のみ表示させる事ができます。<br>
コードリンク<br>
https://github.com/Sugawara-Takuto/volley/blob/29aa64b22996a65d0f8dcecc80abe286597d82bc/volleyapp/views.py#L280-L316
<br>
コード内では、選手選択のviewではsessionでデータベースに選手のプライマリキーのリストを渡し、成績入力のviewで受け取っています。<br>
クエリセットを渡す方が効率的ですが、クエリセットはjsonシリアライズできないため、データベースの性質上クエリセットは渡せませんでした。<br>
<img src="https://user-images.githubusercontent.com/86762993/144865696-be6eccb2-af06-4864-939d-d55e3cf04767.png" width="40%">
<br><br>

<h2>各成績計算＆グラフ化</h2>
入力された成績をview内で計算することにより、スパイク決定率、レシーブ返却率、サーブ効果率を算出しています。<br>
コードリンク<br>
https://github.com/Sugawara-Takuto/volley/blob/29aa64b22996a65d0f8dcecc80abe286597d82bc/volleyapp/views.py#L98-L172
<img src="https://user-images.githubusercontent.com/86762993/144865696-be6eccb2-af06-4864-939d-d55e3cf04767.png" width="40%">
<br>
更に計算された値を元にグラフ化しています。<br>
グラフ化するために、pythonのオープンソースライブラリである、「 matplotlib 」を使用しています。<br>
viewのコードリンク<br>
https://github.com/Sugawara-Takuto/volley/blob/29aa64b22996a65d0f8dcecc80abe286597d82bc/volleyapp/views.py#L141-L157
<br>
graph.pyリンク<br>
https://github.com/Sugawara-Takuto/volley/blob/8b764b16ab9e0e59a56ea318827cfa02d92ce1a7/volleyapp/graph.py#L5-L63
<br>
# 動作
まず、アカウント登録、ログインをします。（テストアカウントはそのままログイン）<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144855500-4ba4d36f-3a54-4d9a-8493-e22f30e862a8.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144854848-927156a8-4258-4c55-bfef-7bf582fdd2d6.png" width="40%">
<br>
<br>
先に、チームをクリックしたあと、createをクリックし、チーム名作成します。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144858670-4b11aa68-cdec-48f5-8146-e6fee2ea2f7d.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144859074-27334c0f-33b9-418a-8732-1d9e36bac2d0.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144859302-d8bedddb-8060-476e-8606-64b715b74226.png" width="40%">
<br><br>
次にチーム名をクリックした後、選手名を作成します。行程はチーム作成と同じです。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144860816-d353db3b-d1f0-49fe-aa48-d4fd5cae3b94.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144860895-00b97c55-b098-47d3-ad4a-a530783da87e.png" width="40%">
<br><br>
これで、選手が作成できたので、Homeに戻ります。
<br>
記録記入から、作ったチームを選択します。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144861206-41ffe454-0565-45bd-a7d9-0f2650f41cc6.png" width="40%">
<br><br>
その後、記録記入したい選手を選択し、決定をクリックします。（複数可）<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144861401-4b67b1a1-9fd7-4a9c-97b8-7f4a1ced5569.png" width="40%">
<br><br>
成績記録欄では、Opponentのみ空欄可能です。<br>
その他で記録がない場合は0を入力してください。<br>
入力したら、送信を押します。<br>
下のスコア確認をクリックすると、一番最初に作った選手一覧のページに移動します。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144862013-9880710c-69b5-453f-a4e0-fe244e6d62a0.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144861886-f39cdcd9-efda-4c29-8195-4040975f03ff.png" width="40%">
<br><br>
そのページで、選手名をクリックすると、成績の表とグラフを見れます。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144860816-d353db3b-d1f0-49fe-aa48-d4fd5cae3b94.png" width="40%">
<img src="https://user-images.githubusercontent.com/86762993/144862442-98075d68-63f2-4781-bbfc-d3e2c6709213.png" width="40%">
<br><br>
全成績をクリックすると、その選手のすべての過去の成績を見ることができます。<br>
更に、各スコアの上にある「消去」をクリックすることで間違って入力したスコアを消去することもできます。<br>
<br>
<img src="https://user-images.githubusercontent.com/86762993/144862721-73d64c6b-c44a-4e52-a9d3-d51b9803e9e9.png" width="40%">
<br><br>
