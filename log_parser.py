import argparse
import re
import json
from collections import defaultdict
from collections import Counter


def main(file):
    dict_ip = defaultdict(
        lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0, "OPTIONS": 0}
    )

    ips_count = defaultdict(int)
    total_stat = defaultdict(int)
    total_requests = 0

    array = [-1, -1, -1]

    with open(file) as f:
        idx = 0
        for line in f:
            if idx > 99:
                break

            # 109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263
            # "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" 7269
            match = re.search(r"(?:(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s-\s(?:[-\w]+)\s(?P<time>\[\s*("
                              r"\d+/\D+/.*?)\])\s\"(?P<method>POST|GET|PUT|DELETE|HEAD|OPTIONS)\s("
                              r"?P<url_path>\S+)\s+?HTTP/\d\.\d\"\s(?P<response_code>\d+?)\s(?P<duration>\d+?|-)\s\"("
                              r"?P<url>[^\"]*))\"", line)

            #ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if match:
                ip = match.group("ip")
                ips_count[ip] += 1
                total_requests += 1
                #method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
                method = match.group("method")
                dict_ip[ip][method] += 1
                total_stat[method] += 1
                idx += 1
                duration = match.group("duration")
                if duration != "-":
                    duration = int(duration)
                    # TBD

            else:
                print(line)

    #total_requests
    print(total_requests)
    #top_ips
    print(Counter(ips_count).most_common(3))
    #total_stat
    print(total_stat)
    #print(json.dumps(dict_ip, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process access.log')
    # https://docs.python.org/3/library/argparse.html
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
    args = parser.parse_args()

    main(args.file)