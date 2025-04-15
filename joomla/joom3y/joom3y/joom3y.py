#!/usr/bin/python
import argparse
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup

dbarray = []
url = ""
useragentdesktop = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Accept-Language": "it",
}
timeoutconnection = 5
pool = None
swversion = "0.5beta"


def hello():
    print("-------------------------------------------")
    print("      	     Joomla Scan                  ")
    print("   Usage: python joomlascan.py <target>    ")
    print(
        "    Version " + swversion + " - Database Entries " + str(len(dbarray))
    )
    print("         created by Andrea Draghetti       ")
    print("-------------------------------------------")


def load_component():
    with open("comptotestdb.txt", "r") as f:
        for line in f:
            dbarray.append(line[:-1]) if line[-1] == "\n" else dbarray.append(
                line
            )


def check_url(url, path="/"):
    fullurl = url + path
    try:
        conn = requests.get(
            fullurl, headers=useragentdesktop, timeout=timeoutconnection
        )
        if conn.headers["content-length"] != "0":
            return conn.status_code
        else:
            return 404
    except Exception:
        return None


def check_url_head(url, path="/"):
    fullurl = url + path
    try:
        conn = requests.head(
            fullurl, headers=useragentdesktop, timeout=timeoutconnection
        )
        return conn.headers["content-length"]
    except Exception:
        return None


def check_and_print(url, component, paths, label):
    for path in paths:
        if check_url(url, path) == 200:
            print(f"\t {label} file found \t > {url}{path}")


def check_readme(url, component):
    paths = [
        "/components/" + component + "/README.txt",
        "/components/" + component + "/readme.txt",
        "/components/" + component + "/README.md",
        "/components/" + component + "/readme.md",
        "/administrator/components/" + component + "/README.txt",
        "/administrator/components/" + component + "/readme.txt",
        "/administrator/components/" + component + "/README.md",
        "/administrator/components/" + component + "/readme.md",
    ]
    check_and_print(url, component, paths, "README")


def check_license(url, component):
    paths = [
        "/components/" + component + "/LICENSE.txt",
        "/components/" + component + "/license.txt",
        "/administrator/components/" + component + "/LICENSE.txt",
        "/administrator/components/" + component + "/license.txt",
        "/components/" + component + "/" + component[4:] + ".xml",
        "/administrator/components/" + component + "/" + component[4:] + ".xml",
    ]
    check_and_print(url, component, paths, "LICENSE")


def check_changelog(url, component):
    paths = [
        "/components/" + component + "/CHANGELOG.txt",
        "/components/" + component + "/changelog.txt",
        "/administrator/components/" + component + "/CHANGELOG.txt",
        "/administrator/components/" + component + "/changelog.txt",
    ]
    check_and_print(url, component, paths, "CHANGELOG")


def check_mainfest(url, component):
    paths = [
        "/components/" + component + "/MANIFEST.xml",
        "/components/" + component + "/manifest.xml",
        "/administrator/components/" + component + "/MANIFEST.xml",
        "/administrator/components/" + component + "/manifest.xml",
    ]
    check_and_print(url, component, paths, "MANIFEST")


def check_index(url, component):
    paths = [
        "/components/" + component + "/index.htm",
        "/components/" + component + "/index.html",
        "/administrator/components/" + component + "/INDEX.htm",
        "/administrator/components/" + component + "/INDEX.html",
    ]
    for path in paths:
        if check_url(url, path) == 200 and check_url_head(url, path) > 1000:
            print(f"\t INDEX file descriptive found \t > {url}{path}")


def index_of(url, path="/"):
    fullurl = url + path
    try:
        page = requests.get(
            fullurl, headers=useragentdesktop, timeout=timeoutconnection
        )
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.title:
            titlepage = soup.title.string
            if titlepage and "Index of /" in titlepage:
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def scanner(url, component):
    if check_url(url, "/index.php?option=" + component) == 200:
        print(
            "Component found: "
            + component
            + "\t > "
            + url
            + "/index.php?option="
            + component
        )

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/components/"
                + component
                + "/"
            )

        if index_of(url, "/administrator/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/administrator/components/"
                + component
                + "/"
            )

    elif check_url(url, "/components/" + component + "/") == 200:
        print(
            "Component found: "
            + component
            + "\t > "
            + url
            + "/index.php?option="
            + component
        )
        print("\t But possibly it is not active or protected")

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/components/"
                + component
                + "/"
            )

        if index_of(url, "/administrator/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/administrator/components/"
                + component
                + "/"
            )

    elif check_url(url, "/administrator/components/" + component + "/") == 200:
        print(
            "Component found: "
            + component
            + "\t > "
            + url
            + "/index.php?option="
            + component
        )
        print("\t On the administrator components")

        check_readme(url, component)

        check_license(url, component)

        check_changelog(url, component)

        check_mainfest(url, component)

        check_index(url, component)

        if index_of(url, "/administrator/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/components/"
                + component
                + "/"
            )

        if index_of(url, "/administrator/components/" + component + "/"):
            print(
                "\t Explorable Directory \t > "
                + url
                + "/administrator/components/"
                + component
                + "/"
            )

    pool.release()


def main(argv):
    # Carico il database di tutti i compomenti di Joomla
    load_component()

    # Visualizzo il banner di benvenuto
    hello()

    # Analizzo gli argomenti passati sul terminale
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-u",
            "--url",
            action="store",
            dest="url",
            help="The Joomla URL/domain to scan.",
        )
        parser.add_argument(
            "-t",
            "--threads",
            action="store",
            dest="threads",
            help="The number of threads to use when multi-threading requests (default: 10).",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s " + swversion,
        )

        arguments = parser.parse_args()
    except:
        sys.exit(1)

    if arguments.url:
        url = arguments.url
        if url[:8] != "https://" and url[:7] != "http://":
            print("You must insert http:// or https:// procotol\n")
            sys.exit(1)

        # Rimuovo un eventuale barra alla fine del url
        if url.endswith("/"):
            url = url[:-1]
    else:
        print("")
        parser.parse_args(["-h"])
        sys.exit(1)

    concurrentthreads = 10
    global pool
    # Imposto il numero di thread concorrenti
    if arguments.threads and arguments.threads.isdigit():
        # Limit the number of threads.
        concurrentthreads = int(arguments.threads)
        pool = threading.BoundedSemaphore(concurrentthreads)
    else:
        # Default value for limit the number of threads.
        pool = threading.BoundedSemaphore(concurrentthreads)

    # Analizzo la disponibilita del sito indicato
    if check_url(url) != 404:
        if check_url(url, "/robots.txt") == 200:
            print("Robots file found: \t \t > " + url + "/robots.txt")
        else:
            print("No Robots file found")

        if check_url(url, "/error_log") == 200:
            print("Error log found: \t \t > " + url + "/error_log")
        else:
            print("No Error Log found")

        # Inizio la scansione dei componenti

        print("\nStart scan...with %d concurrent threads!" % concurrentthreads)

        for component in dbarray:
            # Thread Pool
            pool.acquire(blocking=True)

            t = threading.Thread(
                target=scanner,
                args=(
                    url,
                    component,
                ),
            )
            t.start()

        while threading.active_count() > 1:
            time.sleep(0.1)

        print("End Scanner")

    else:
        print("Site Down, check url please...")


if __name__ == "__main__":
    main(sys.argv[1:])
