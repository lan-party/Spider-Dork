import random
import socket
import requests
import hashlib
import json
import time
import threading
import datetime

# Netblock queues
unscanned_netblocks_file = open("unscanned_netblocks.txt", "r")
unscanned_netblocks = unscanned_netblocks_file.read().splitlines()
unscanned_netblocks_file.close()
scanned_netblocks_file = open("scanned_netblocks.txt", "r")
scanned_netblocks = scanned_netblocks_file.read().splitlines()
scanned_netblocks_file.close()

dorklist = open("dorks.txt", "r").read().splitlines()
thread_count = 60
delay_between_threads = 10

# Functions

def random_netblock(thread_id):
    global unscanned_netblocks
    global scanned_netblocks

    byte1 = random.randint(1, 255)
    byte2 = random.randint(1, 255)
    byte3 = random.randint(0, 255)
    netblock = str(byte1)+"."+str(byte2)+"."+str(byte3)+"."

    # Edit this to force a specific search mode
    if (int(thread_id) % 2 == 0 or len(unscanned_netblocks) == 0):
    # if True:
    # if False:
        
        while (byte1 == 10) or (byte1 == 127 and byte2 >= 16 and byte2 <= 31) or (byte1 == 192 and byte2 == 168) or (netblock in scanned_netblocks):
            byte1 = random.randint(1, 255)
            byte2 = random.randint(1, 255)
            byte3 = random.randint(0, 255)
            netblock = str(byte1)+"."+str(byte2)+"."+str(byte3)+"."
    else:
        if len(unscanned_netblocks) <= 0:
            return False
        random.shuffle(unscanned_netblocks)
        netblock = unscanned_netblocks.pop(0)
    
    scanned_netblocks.append(netblock)

    return netblock

def http_scan(netblock, thread_id):
    ips = []
    for a in range(0, 255):
        ip = netblock+str(a)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)
        if sock.connect_ex((ip,80)) == 0:
            ips.append("http://" + ip)
            if len(ips) == 1:
                print(thread_id.ljust(3) + " | HTTP (port 80) found in netblock.")
        elif sock.connect_ex((ip,8080)) == 0:
            ips.append("http://" + ip + "8080")
            if len(ips) == 1:
                print(thread_id.ljust(3) + " | HTTP (port 8080) found in netblock.")
        elif sock.connect_ex((ip,443)) == 0:
            ips.append("https://" + ip)
            if len(ips) == 1:
                print(thread_id.ljust(3) + " | HTTPS (port 443) found in netblock.")
        elif sock.connect_ex((ip,8443)) == 0:
            ips.append("https://" + ip + "8443")
            if len(ips) == 1:
                print(thread_id.ljust(3) + " | HTTPS (port 8443) found in netblock.")
        sock.close()

    return ips

def dorklist_check(ips, thread_id):
    matching_addresses = []
    if len(ips) > 0:
        for ip in ips:
            try:
                resp = requests.get(ip).text.lower()
                matching_dorks = []
                for dork in dorklist:
                    if dork.lower() in resp:
                        matching_dorks.append(dork)
                if len(matching_dorks) > 0:
                    matching_addresses.append([ip, resp, matching_dorks])
                    if len(matching_addresses) == 1:
                        print(thread_id.ljust(3) + " | Dork found in netblock.")
            except Exception:
                pass
    return matching_addresses

def save_addresses(addresses):
    append_content = ""
    for address in addresses:
        # Get page title
        title = ""
        try:
            title = address[1].replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "").split("<title")[1]
            title = title.split(">")[1]
            title = title.split("</title")[0]
        except Exception:
            pass
        # Generate page hash
        page_hash = ""
        try:
            page_hash = hashlib.md5(address[1].encode('utf-8')).hexdigest()
        except Exception:
            pass
        # Get geographic data
        resp = json.loads(requests.get("http://ip-api.com/json/"+address[0].split("//")[1]).text)
        country = resp['country']
        region = resp['region']
        city = resp['city']
        isp = resp['isp']

        append_content += "\n" + address[0] + "\t" + str(title.encode("utf-8"))[2:-1] + "\t" + page_hash + "\t" + country + "\t" + region + "\t" + str(city.encode("utf-8"))[2:-1] + "\t" + str(isp.encode("utf-8"))[2:-1] + "\t" + json.dumps(address[2]) + "\t" + datetime.datetime.now().strftime("%m/%d/%Y")
    # Append to file
    save_file = open("found_targets.tsv", "a")
    save_file.write(append_content)
    save_file.close()

def update_queue(addresses, netblock):
    global unscanned_netblocks
    global scanned_netblocks

    if len(addresses) > 0:
        netblock = netblock.split(".")
        netblock_start = netblock[0] + "." + netblock[1] + "."

        if int(netblock[2]) > 0:
            new_netblock = netblock_start + str(int(netblock[2])-1) + "."
            if new_netblock not in unscanned_netblocks and new_netblock not in scanned_netblocks:
                unscanned_netblocks.append(new_netblock)

        if int(netblock[2]) < 255:
            new_netblock = netblock_start + str(int(netblock[2])+1) + "."
            if new_netblock not in unscanned_netblocks and new_netblock not in scanned_netblocks:
                unscanned_netblocks.append(new_netblock)


# Thread function

def scan(thread_id):
    while True:
        # Random /24 netblock generation
        nb = random_netblock(thread_id)
        print(thread_id.ljust(3) + " | block: " + nb + "0/24")

        # Return a list of ips with port 80 open
        http_addresses = http_scan(nb, thread_id)
        total = str(len(http_addresses))
        if len(http_addresses) > 0:
            total = '\033[96m' + total + '\033[0m'
        print(thread_id.ljust(3) + " | block: " + (nb + "0/24").ljust(16) + " | total: " + total)

        # Search each index for word list matches
        matching_addresses = dorklist_check(http_addresses, thread_id)
        matches = str(len(matching_addresses))
        if (len(matching_addresses)) > 0:
            matches = '\033[92m' + matches + '\033[0m'
        print(thread_id.ljust(3) + " | block: " + (nb + "0/24").ljust(16) + " | total: " + total.ljust(3) + " | matches: " + matches)

        # Save ip and collected info
        save_addresses(matching_addresses)

        # Add nearby netblocks to the unscanned queue
        update_queue(matching_addresses, nb)

def sync_queues():
    global unscanned_netblocks
    global scanned_netblocks

    while True:
        time.sleep(60)
        unscanned_netblocks_file = open("unscanned_netblocks.txt", "w")
        unscanned_netblocks_file.write("\n".join(unscanned_netblocks))
        unscanned_netblocks_file.close()

        scanned_netblocks_file = open("scanned_netblocks.txt", "w")
        scanned_netblocks_file.write("\n".join(scanned_netblocks))
        scanned_netblocks_file.close()
        print("S   | Queues synced.")


# Start threads

sync_thread = threading.Thread(target=sync_queues)
sync_thread.start()

threads = []
for a in range(0, thread_count):
    threads.append(threading.Thread(target=scan, args=(str(a),)))
    threads[a].start()
    time.sleep(delay_between_threads)
