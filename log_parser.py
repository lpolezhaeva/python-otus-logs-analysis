import argparse
import glob
import re
import json
import os
from collections import defaultdict
from collections import Counter


def get_log_files(paths):
    files = []

    for path in paths:
        if os.path.isfile(path):
            base_name, extension = os.path.splitext(path)
            if extension[1:] == 'log':
                files.append(path)
            else:
                print(f"Skipped file (without .log extensions): {path}")
        else:
            log_files = glob.glob(os.path.join(path, '**/*.log'), recursive=True)
            for file in log_files:
                if os.path.isfile(file):
                    files.append(file)

    return files


def main(paths):

    log_files = get_log_files(paths)

    for findex, file in enumerate(log_files, start=1):
        print(f"Processing file: {file}")

        requests = []
        ips_count = defaultdict(int)
        total_stat = defaultdict(int)
        total_requests = 0

        with open(file) as f:
            idx = 0
            for line in f:

                match = re.search(r"(?:(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s-\s(?:[-\w\"\.@]+)\s(?P<time>\[\s*("
                                  r"\d+/\D+/.*?)\])\s\"(?P<method>POST|GET|PUT|DELETE|HEAD|OPTIONS)\s("
                                  r"?P<url_path>\S+)\s+?HTTP/\d\.\d\"\s(?P<response_code>\d+?)\s(?P<number_of_bytes>\d+?|-)\s\"("
                                  r"?P<url>[^\"]*))\".+?(?P<duration>\d*)$", line)

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
                    requests.append({
                        "ip": ip,
                        "date": date,
                        "method": method,
                        "url": url,
                        "duration": int(duration)
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

        print(json.dumps(data, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process access.log')
    parser.add_argument('--paths', dest='paths', action='store', help='Path to directory or logfile', nargs='+')
    args = parser.parse_args()

    main(args.paths)
