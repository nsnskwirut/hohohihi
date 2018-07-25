import os
import re
import time
from datetime import datetime as dt

"""
A programme that prevents user's distraction and enhance their's productivity.
In other words - simply blocking websites specified in to_block file (fb, yt, kanonierzy.com, etc.)
---
Needs addidtional configuration in /etc/crontab or Windows Task Scheduler
---
(c) Szymix Szimi 2018
"""

def determine_host_path():
    if os.name == 'nt':
        return "hosts" # C:\Windows\System32\drivers\etc
    elif os.name == 'posix':
        return "/etc/hosts"


def get_domains_list(domains_file):
    """May be hosts or to_block. Lines commented using # are being omitted."""
    with open(domains_file, 'r') as f:
        content = f.read().splitlines()
    return [domain for domain in content if '#' not in domain and domain != '']


def write_to_hosts(hosts_path, message, mode):
    with open(hosts_path, mode) as f:
        f.writelines(message)


def trim_line(domains):
    """Removes localhost redirection ip from line in /hosts for later comparisons."""
    trimmed = []
    for domain in domains:
        domain = domain.replace(re.findall(r"^[127.0.0.1]+\s+", domain)[0], "")
        trimmed.append(domain)
    return trimmed


if __name__ == '__main__':
    hosts_path = determine_host_path()
    to_block = 'to_block.txt'

    while True:
        if dt.now().minute % 2 == 0: # Trolololo statement to lock viewing during 
            print("Locking access to the pages...")
            for domain in get_domains_list(to_block):
                if domain not in trim_line(get_domains_list(hosts_path)):
                    write_to_hosts(hosts_path, "{} {}\n".format("127.0.0.1", domain), mode='a')
        else:
            print("Removing access lock...")
            with open(hosts_path, 'r+') as f:
                content = f.readlines()
                f.seek(0)
                for line in content:
                    if not any(domain in line for domain in get_domains_list(to_block)):
                        f.write(line)
                f.truncate()

        time.sleep(10)