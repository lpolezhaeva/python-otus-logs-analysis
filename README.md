# Access Log Analyzer

This is a Python script for analyzing access log files in the following format:

```
%h %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i" %D
```

The script analyzes the log files and provides the following statistics:

- Total number of requests
- Number of requests by HTTP methods (GET, POST, PUT, HEAD, OPTIONS, DELETE)
- Top 3 IP addresses that made requests
- Top 3 longest requests, including method, URL, IP, duration, and request date and time

The script can analyze a single log file or all log files in a directory.

## Usage

To use the script, run the following command:

```
python log_parser.py [log_file_or_directory]
```

Replace `[log_file_or_directory]` with the path to the log file or directory you want to analyze. If you don't specify a log file or directory, the script will analyze the `access.log` file in the current directory.

The script will generate a JSON file with the statistics for each log file analyzed, and print the statistics to the terminal in the following format:

```
{
    "top_ips": [
        {
            "192.168.1.1": 50,
            "192.168.1.2": 30,
            "192.168.1.3": 20
        }
    ],
    "top_longest": [
        {
            "ip": "192.168.1.1",
            "date": "[06/Jan/2016:12:00:02 +0100]",
            "method": "GET",
            "url": "/some/long/url",
            "duration": 500
        },
        {
            "ip": "192.168.1.2",
            "date": "[06/Jan/2016:18:47:57 +0100]",
            "method": "POST",
            "url": "/another/long/url",
            "duration": 400
        },
        {
            "ip": "192.168.1.3",
            "date": "[23/Dec/2015:07:27:57 +0100]",
            "method": "GET",
            "url": "/yet/another/long/url",
            "duration": 300
        }
    ],
    "total_stat": {
        "GET": 70,
        "POST": 20,
        "HEAD": 3,
        "PUT": 5,
        "OPTIONS": 1,
        "DELETE": 1
    },
    "total_requests": 100
}
``` 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.