AWS SAM Python Hands-on
===================
# 目的 #
AWS サーバーレスアプリケーションモデル (AWS SAM) ハンズオン(Python)

# 前提 #
| ソフトウェア   | バージョン   | 備考        |
|:---------------|:-------------|:------------|
| python         |3.6.0    |             |
| sam            |0.3.0  |             |
| docker         |17.06.2  |             |
| docker-compose |1.21.0  |             |
| vagrant        |2.0.3  |             |

# 構成 #
1. [構築](#構築 )
1. [配置](#配置 )
1. [運用](#運用 )
1. [開発](#開発 )

## 構築
### 開発用仮想マシンの起動・プロビジョニング
+ Dockerのインストール
+ docker-composeのインストール
+ pipのインストール
```bash
vagrant up
vagrant ssh
```

### 開発パッケージのインストール
+ aws-sam-cliのインストール
+ pyenvのインストール
+ Pythonのインストール

```bash
pip install --user aws-sam-cli
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash 
```

`~/.bashrc`に以下を追加するして`source ~/.bashrc`
```
export PATH="/home/vagrant/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

利用するPythonのバージョンをインストールする
```
cd /vagrant
sudo yum install gcc gcc-c++ make git openssl-devel bzip2-devel zlib-devel readline-devel sqlite-devel -y
pyenv install -l
pyenv install 3.6.0
pyenv local 3.6.0
```

**[⬆ back to top](#構成)**

## 配置
**[⬆ back to top](#構成)**

## 運用
**[⬆ back to top](#構成)**

## 開発
### アプリケーションの作成
```bash
cd /vagrant
sam init --runtime python
cd sam-app
```

### ローカルでテストする
```bash
cd /vagrant/sam-app
pip install pytest requests
python -m pytest tests/ -v
pip install -r requirements.txt -t hello_world/build/
cp hello_world/*.py hello_world/build/
sam local generate-event api > event_file.json
sam local invoke HelloWorldFunction --event event_file.json
sam local start-api --host 0.0.0.0
```
[http://192.168.33.10:3000/hello](http://192.168.33.10:3000/hello)に接続して確認する

### コードチェッカーのセットアップ
```bash
cd /vagrant/sam-app
pip install pycodestyle
```


**[⬆ back to top](#構成)**

# 参照 #
+ [Amazon Linux2にDockerをインストールする](https://qiita.com/reoring/items/0d1f556064d363f0ccb8) 
+ [Pythonのパッケージ管理システムpipのインストールと使い方](https://uxmilk.jp/12691)
+ [aws-sam-local 改め aws-sam-cli の新機能 sam init を試す](https://qiita.com/hayao_k/items/841026f9675d163b58d5)
+ [Simple Python Version Management: pyenv](https://github.com/pyenv/pyenv)
+ [pyenv installer](https://github.com/pyenv/pyenv-installer)
+ [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)