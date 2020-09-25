# SSBU GRAPH MAKER(試作版)
大乱闘スマッシュブラザーズの対戦動画からダメージ遷移のグラフを生成するものです。試作版で精度が良くないのは悪しからず。

## 使い方
```python main.py hoge_video.mp4```  
このように```main.py```の引数に1試合分の動画ファイルを与えることで動作します。  
  
また、リプレイから生成したい方はYouTube上の動画を保存することができます。  
```$ python download.py https://youtube.com/hoge_url```  
投稿したリプレイのURLを引数に与えることでディレクトリにmp4形式で保存します。