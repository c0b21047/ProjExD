# 第１回
## サザエさんクイズ(ex01/quiz.py)
### 遊び方
* コマンドラインでquiz.pyを実行すると,標準出力に問題が表示される。
* 標準入力から答えを入力する。
* 正解なら「正解！！！」と表示される。
* 不正解なら「出直してこい」と表示される。
* 正解でも不正解でも、１問のみ出題される。
### プログラム内の解説
* main関数：クイズプログラムの全体の流れを担当する。
* shutudai関数：ランダムに選んだ問題を出題し、正解を返す。
* kaitou関数：回答と正解をチェックし、結果を出力する。
## アルファベットゲーム
### 遊び方(ex01/alphabet.py)
* コマンドラインでalphabet.pyを実行すると,標準出力に問題が表示される。
* 対象文字と表示文字を比べ、欠損文字数と欠損文字を当てる。
* 標準入力から答えを入力する。
* 正解なら「正解！！！」と表示され、かかった時間が表示される。
* 不正解なら「不正解です。またチャレンジしてください」と表示される。
* 正解するまで、連続で3問出題される。
### プログラム内の解説
* main関数：プログラム全体の流れを担当する。
* shutudai関数：アルファベットのリストの中から対象文字をランダムで選び表示する。
* del_alp関数：対象文字の中から欠損文字を指定回数ランダムで選び、対象文字から削除する。欠損文字を表示することもできる。
* ans関数；回答と正解をチェックし、その結果をmain関数に返す。
### TODO
* 例外処理