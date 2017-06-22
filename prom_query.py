#!/usr/bin/python
"""Bananas """

import argparse
import csv
import json
import sys
import urllib
import urllib2


def parse_args(args):
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument(
        '--server', default='status-mlab-oti.measurementlab.net:9090',
        help='Prometheus server to query.')
    parser.add_argument(
        '--query', default='',
        help='Prometheus query.')
    parser.add_argument(
        '--label', default='',
        help='Lable to extract from query results.')
    return parser.parse_args(args)


def query(server, query):
    query = urllib.urlencode({'query': query})
    url = 'http://%s/api/v1/query?%s' % (server, query)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data


def main():
    args = parse_args(sys.argv[1:])
    results = query(args.server, args.query)
    if results['status'] == "success":
        output = csv.DictWriter(sys.stdout, fieldnames=results['data']['result'][0]['metric'].keys())
        output.writeheader()
        for result in results['data']['result']:
            if args.label and args.label in result['metric']:
                print result['metric'][args.label]
            else:
                output.writerow(result['metric'])

    elif results['status'] == "error":
        print results
    else:
        print 'error'


if __name__ == '__main__':  # pragma: no cover
    main()
