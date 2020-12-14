# ドローン実験

## ソースコード

easyTelloに依存します。

- easytello.patch: [easyTello](https://github.com/Virodroid/easyTello)に適用するパッチ（後述）
- util.py: デバッグ・操作用の関数
- cam.py: カメラテスト
- color_recog.py: 色の検知
- contour_follow.py: 色で表現した領域に輪郭をつけて追跡
- control.py: ジョイスティックコントローラで操作
- land.py: land（着陸）コマンドを送信

- tello_lib(_sample).py: nagataaaas作ライブラリ

## easyTelloにあてるパッチ

easyTelloの応答性を改善するために、独自の変更をしています。

```bash
$ pip3 show easytello 
```

でインストールパスを確認してから、

```bash
$ patch (インストールパス)/easytello/tello.py easytello.patch 
```

とすると（たぶん）適用できます。一応、適用済のを easytello_modified.py に置いてあります。
