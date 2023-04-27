import argparse
import re
import json
from collections import defaultdict
from collections import Counter


def main(files):
    findex = 0

    for file in files:
        findex += 1

        requests = []
        ips_count = defaultdict(int)
        total_stat = defaultdict(int)
        total_requests = 0

        with open(file) as f:
            idx = 0
            for line in f:

                match = re.search(r"(?:(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s-\s(?:[-\w\"\.@]+)\s(?P<time>\[\s*("
                                  r"\d+/\D+/.*?)\])\s\"(?P<method>POST|GET|PUT|DELETE|HEAD|OPTIONS)\s("
                                  r"?P<url_path>\S+)\s+?HTTP/\d\.\d\"\s(?P<response_code>\d+?)\s(?P<duration>\d+?|-)\s\"("
                                  r"?P<url>[^\"]*))\"", line)

                if match:
                    ip = match.group("ip")
                    date = match.group("time")
                    if match.group("url") and match.group("url") != "-":
                        url = match.group("url") + match.group("url_path")[1:]
                    else:
                        url = match.group("url_path")
                    ips_count[ip] += 1
                    total_requests += 1
                    method = match.group("method")
                    total_stat[method] += 1
                    idx += 1
                    duration = match.group("duration")
                    if duration != "-":
                        duration = int(duration)
                        requests.append({
                            "ip": ip,
                            "date": date,
                            "method": method,
                            "url": url,
                            "duration": duration
                        })
                else:
                    print(line)

        requests = sorted(requests, key=lambda x: -x["duration"])
        most_common = Counter(ips_count).most_common(3)

        data = {"top_ips":
            {
                ip: count for ip, count in most_common
            },
            "top_longest": requests[0:3],
            "total_stat": dict(total_stat),
            "total_requests": total_requests
        }

        with open(f'result{findex}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process access.log')
    parser.add_argument('--file', dest='files', action='store', help='Path to logfile', nargs='+')
    args = parser.parse_args()

    main(args.files)
