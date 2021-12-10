# Finding an old enough java version

This exploit only works with very old versions java 8. For the purposes o the exploit we will be using java-8u20.

This can be downloaded from Oracle's website at:
[https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/8u20-b26/jre-8u20-linux-x64.tar.gz](https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/8u20-b26/jre-8u20-linux-x64.tar.gz).

**Note:** You do need to make an account to be able to download the package.


Once you have downloaded, extract the archive and run you can run java by executing the java binary in `jre1.8.0_20/bin`.

```
❯ tar -xf jre-8u20-linux-x64.tar.gz

❯ ./jre1.8.0_20/bin/java -version
java version "1.8.0_20"
Java(TM) SE Runtime Environment (build 1.8.0_20-b26)
Java HotSpot(TM) 64-Bit Server VM (build 25.20-b23, mixed mode)
```
