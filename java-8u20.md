# Getting an old enough version of java.

The exploit only works with very old versions of java 8. We are unsure of exactly which java versions work and which don't so we have chosen to work with one of the earliest versions of java 8: `java-8u20`.

Oracle thankfully provides an archive for all previous java versions:<br>
[https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html).<br>
Scroll down to `8u20` and download the appropriate files for your operating system and hardware.
![Screenshot from 2021-12-11 00-09-25](https://user-images.githubusercontent.com/46561460/145655967-b5808b9f-d919-476f-9cbc-ed9eaff51585.png)

**Note:** You do need to make an account to be able to download the package.

Once you have downloaded and extracted the archive, you can find `java` and a few related binaries in `jdk1.8.0_20/bin`.

```
❯ tar -xf jdk-8u20-linux-x64.tar.gz

❯ ./jdk1.8.0_20/bin/java -version
java version "1.8.0_20"
Java(TM) SE Runtime Environment (build 1.8.0_20-b26)
Java HotSpot(TM) 64-Bit Server VM (build 25.20-b23, mixed mode)
```
