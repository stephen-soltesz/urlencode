#!/usr/bin/python
"""Bananas """

import argparse
import csv
import json
import logging
import sys
import urllib
import urllib2


class DictWriter(csv.DictWriter):
    """Write header using fields from first writerow."""
    
    def __init__(self, output, with_header):
        self._output = output
        self._write_header = with_header
        self._csv = None

    def writerow(self, row):
        """Writes the row."""
        if self._csv is None:
            self._csv = csv.DictWriter(self._output, sorted(row.keys()))
        if self._write_header:
            self._csv.writeheader()
            self._write_header = False
        self._csv.writerow(row)


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
    parser.add_argument(
        '--header', default=False, action='store_true',
        help='Write the header.')
    return parser.parse_args(args)


def query(server, query):
    query = urllib.urlencode({'query': query})
    url = 'http://%s/api/v1/query?%s' % (server, query)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data


def main():
    args = parse_args(sys.argv[1:])
    response = query(args.server, args.query)
    if 'status' not in response:
        logging.error('Results have no "status": %s', response)
        sys.exit(1)

    if response['status'] not in ['success', 'error']:
        logging.error('Results have unsupported "status": %s', response)
        sys.exit(1)

    if response['status'] == 'error':
        print response
        sys.exit(1)

    # Response status is success.
    output = DictWriter(sys.stdout, args.header)
    if 'data' not in response:
        logging.error('Results are missing "data": %s', response)
        sys.exit(1)

    if 'result' not in response['data']:
        logging.error('Results are missing "data->result": %s', response)
        sys.exit(1)

    results = response['data']['result']
    for result in [result for result in results if 'metric' in result]:
        metrics = result['metric']
        if args.label and args.label in metrics:
            output.writerow({args.label: metrics[args.label]})
        else:
            output.writerow(metrics)



if __name__ == '__main__':  # pragma: no cover
    main()
