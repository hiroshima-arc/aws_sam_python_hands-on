AWS SAM Python Hands-on
===================
# 目的 #
AWS サーバーレスアプリケーションモデル (AWS SAM) ハンズオン(Python)

# 前提 #
| ソフトウェア   | バージョン   | 備考        |
|:---------------|:-------------|:------------|
| python         |3.6.0    |             |
| sam            |0.6.0  |             |
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

### ドキュメント環境構築
```bash
cd /vagrant
curl -s api.sdkman.io | bash
source "/home/vagrant/.sdkman/bin/sdkman-init.sh"
sdk list maven
sdk use maven 3.5.4
sdk list java
sdk use java 8.0.181-zulu
sdk list gradle
sdk use gradle 4.9
```
ドキュメントのセットアップ
```
cd /vagrant/
touch build.gradle
```
`build.gradle`を作成して以下のコマンドを実行
```
gradle build
```
ドキュメントの生成
```bash
gradle asciidoctor
gradle livereload
```
[http://192.168.33.10:35729/](http://192.168.33.10:35729/)に接続して確認する

### パイプラインの構築
```
cd /vagrant/ops/code_pipline
./create_stack.sh 
```

**[⬆ back to top](#構成)**

## 配置
### AWS認証設定
```bash
cd /vagrant/sam-app
cat <<EOF > .env
#!/usr/bin/env bash
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxx
export AWS_DEFAULT_REGION=us-east-1
EOF
```
アクセスキーを設定したら以下の操作をする
```bash
source .env
aws ec2 describe-regions
```

### デプロイ
デプロイ用のS3バケットを用意する
```bash
aws s3 mb s3://python-hands-on
```
デプロイを実行する
````bash
cd /vagrant/sam-app
sam validate
pip install -r requirements.txt -t hello_world/build/
cp hello_world/*.py hello_world/build/
sam package --template-file template.yaml --s3-bucket python-hands-on --output-template-file packaged.yaml
sam deploy --template-file packaged.yaml --stack-name python-hands-on-development --capabilities CAPABILITY_IAM
````
デプロイが成功したら動作を確認する
```bash
aws cloudformation describe-stacks --stack-name python-hands-on-development --query 'Stacks[].Outputs[1]'
```

**[⬆ back to top](#構成)**

## 運用
### スタックの削除
```bash
aws cloudformation delete-stack --stack-name python-hands-on-development
aws cloudformation delete-stack --stack-name python-hands-on-production
aws cloudformation delete-stack --stack-name python-hands-on-pipeline
```
### S３バケットの削除
```bash
aws s3 rb s3://python-hands-on --force
```

### git-secretsの設定
インストール
```bash
cd /home/vagrant
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets/
make install
cd ..
rm -rf git-secrets/
```
既存プロジェクトにフックを設定
```bash
cd /vagrant
git secrets --install
```
拒否条件を設定
```bash
git secrets --register-aws --global
```
レポジトリをスキャンする
```bash
cd /vagrant
git secrets --scan -r 
```
許可ルールを追加する
```bash
git config --add secrets.allowed sam-app/tests/hello_world/event_file.json
git config --add secrets.allowed sam-app/tests/unit/hello_world/test_handler.py
git config --add secrets.allowed docs/hello_world.html
git config --add secrets.allowed sam-app/tests/fizz_buzz/generate_event_file.json
git config --add secrets.allowed sam-app/tests/fizz_buzz/iterate_event_file.json
git config --add secrets.allowed docs/fizz_buzz.html
```

**[⬆ back to top](#構成)**

## 開発
### アプリケーションの作成
```bash
cd /vagrant
sam init --runtime python
cd sam-app
```

### ローカルでテストする
#### HelloWorld
```bash
cd /vagrant/sam-app
pip install pytest requests
python -m pytest tests/ -v
rm -rf hello_world/build
pip install -r requirements.txt -t hello_world/build/
cp hello_world/*.py hello_world/build/
mkdir tests/hello_world
sam local generate-event api > tests/hello_world/event_file.json
sam local generate-event apigateway aws-proxy > tests/hello_world/event_file.json
sam local invoke HelloWorldFunction --event tests/hello_world/event_file.json
sam local start-api --host 0.0.0.0
```

#### FizzBuzz
```bash
cd /vagrant/sam-app
python -m pytest tests/ -v
rm -rf fizz_buzz/build
pip install -r requirements.txt -t fizz_buzz/build/
cp fizz_buzz/*.py fizz_buzz/build/
mkdir tests/fizz_buzz
sam local invoke FizzBuzzGenerateFunction --event tests/fizz_buzz/generate_event_file.json
sam local invoke FizzBuzzIterateFunction --event tests/fizz_buzz/iterate_event_file.json
sam local start-api --host 0.0.0.0
```
[http://192.168.33.10:3000/hello](http://192.168.33.10:3000/hello)に接続して確認する

### コードチェッカーのセットアップ
```bash
cd /vagrant/sam-app
pip install pycodestyle
python -m pycodestyle sam-app/*/*.py
```

### コードカバレッジのセットアップ
```bash
cd /vagrant/sam-app
pip install pytest-cov
python -m pytest --cov tests/
```


**[⬆ back to top](#構成)**

# 参照 #
+ [Amazon Linux2にDockerをインストールする](https://qiita.com/reoring/items/0d1f556064d363f0ccb8) 
+ [Pythonのパッケージ管理システムpipのインストールと使い方](https://uxmilk.jp/12691)
+ [aws-sam-local 改め aws-sam-cli の新機能 sam init を試す](https://qiita.com/hayao_k/items/841026f9675d163b58d5)
+ [Simple Python Version Management: pyenv](https://github.com/pyenv/pyenv)
+ [pyenv installer](https://github.com/pyenv/pyenv-installer)
+ [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
+ [図入りのAsciiDoc記述からPDFを生成する環境をGradleで簡単に用意する](https://qiita.com/tokumoto/items/d37ab3de5bdbee307769)
+ [クラウド破産しないように git-secrets を使う](https://qiita.com/pottava/items/4c602c97aacf10c058f1)   