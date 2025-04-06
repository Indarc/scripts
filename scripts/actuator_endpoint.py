#!/usr/bin/python

import requests
import warnings
import argparse



def check_endpoint(url, endpoint, status_filter, status_match, size_filter, size_match, lines_filter, lines_match):
    full_url = url + endpoint.strip()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Host": full_url.split('/')[2],
        "Connection": "Keep-alive"
    }
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = requests.get(full_url, headers=headers, verify=False)
        status_code = response.status_code
        size = len(response.content)
        lines = len(response.text.splitlines())
        if status_code in status_match or len(status_match) == 0 or size in size_match or lines in lines_match:
            if status_code in status_filter or size in size_filter or lines in lines_filter:
                return
            print(f"{endpoint.strip():<50} [Status:  {response.status_code}, Size: {len(response.content)}, Lines: {len(response.text.splitlines())}]")
        else:
            return
    except Exception as e:
        return

def main():
    parser = argparse.ArgumentParser(description='Search actuator endpoints')
    parser.add_argument('-u', '--url', type=str, required=True, help="Target url")
    parser.add_argument('-w', '--wordlist', default='./scripts/src/wordlist.txt' , type=str, required=False, help="Path to wordlist, if not set use default wordlist")
    parser.add_argument('-fc', '--filter_code', nargs='*', default=[], type=int, required=False, help="Filter by status code, use SPACE to delimit")
    parser.add_argument('-fs', '--filter_size', nargs='*', default=[], type=int, required=False, help="Filter by response size in bytes, use SPACE to delimit")
    parser.add_argument('-fl', '--filter_lines', nargs='*', default=[], type=int, required=False, help="Filter by count of lines, use SPACE to delimit")
    parser.add_argument('-mc', '--match_code', nargs='*', default=[], type=int, required=False, help="Match status code, use SPACE to delimit")
    parser.add_argument('-ms', '--match_size', nargs='*', default=[], type=int, required=False, help="Match response size in bytes, use SPACE to delimit")
    parser.add_argument('-ml', '--match_lines', nargs='*', default=[], type=int, required=False, help="Match by count of lines, use SPACE to delimit")

    args = parser.parse_args()

    roots = [
        "/actuator/",
        "/api/actuator/",
        "/api/appname/actuator/",
        "/api/application/actuator/"
    ]

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    
    if args.wordlist:
        wordlist_file = args.wordlist

    try:
        with open(wordlist_file, 'r') as f:
          wordlist = f.readlines()
    except Exception as e:
        print(f"Error with open file {wordlist_file}")
        print(f"Error: {e}")
        return
    
    status_filter = args.filter_code
    status_match = args.match_code
    size_filter = args.filter_size
    size_match = args.match_size
    lines_filter = args.filter_lines
    lines_match = args.match_lines

    print("---------------------------------------")
    print("|        Filter: ", status_filter)
    print("|        Match:  ", status_match)
    print("---------------------------------------")

    # accessible_endpoints = []
    for root in roots:
        for word in wordlist:
            endpoint = root + word.strip()
            check_endpoint(url, endpoint, status_filter, status_match, size_filter, size_match, lines_filter, lines_match)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
