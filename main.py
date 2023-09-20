import argparse
import csv
import logging
import time

import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_post_request(url, data):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json; charset=utf-8',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as request_error:
        logger.error('Error making POST request: %s', request_error)
        logger.error('Response: %s', response.json())
        return None

def process_tsv_file(file_path, locale, locale_id, interval):
    with open(file_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            sentence, source = row
            response = make_post_request('https://commonvoice.mozilla.org/api/v1/sentences',
                                         {
                                             'sentence': sentence,
                                             'source': source,
                                             'localeId': locale_id,
                                             'localeName': locale
                                         })
            if response:
                logger.info('POST with sentence %s request successful: %s',
                            sentence,
                            response.json())
            else:
                logger.warning(
                    'Failed to make POST request for the following data: %s', sentence)
            time.sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send sentences to common voice api using data from a TSV file')
    parser.add_argument('file_path', help='path to the input TSV file')
    parser.add_argument('-l', '--locale', help='locale name')
    parser.add_argument('-li', '--locale_id', type=int, help='locale id')
    parser.add_argument('-i', '--interval', type=int,
                        default=0, help='interval between requests')
    args = parser.parse_args()
    try:
        process_tsv_file(args.file_path,
                         args.locale,
                         args.locale_id, 
                         args.interval)
    except Exception as error:
        logger.error('An error occurred: %s', error)
