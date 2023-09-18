import requests
import csv
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_post_request(url, token, data):
    try:
        response = requests.post(url, json=data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {token}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making POST request: {e}")
        return None

def process_tsv_file(file_path, token, locale):
    logger.info(f"{file_path}")
    with open(file_path, 'r', newline='', encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            sentence = row[0]
            source = row[1]
            logger.info(f"{row}")
            response = make_post_request("https://commonvoice.mozilla.org/api/v1/sentences", token, {"sentence":f"{sentence}","source":f"{source}","localeId":81129,"localeName":f"{locale}"})
            if response:
                logger.info(f"POST with sentence {sentence} request successful: {response}")
            else:
                logger.warning(f"Failed to make POST request for the following data: {row}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make POST requests using data from a TSV file")
    parser.add_argument("file_path", help="Path to the input TSV file")
    parser.add_argument("auth", help="Authorization token")
    parser.add_argument("locale", help="Locale name")
    args = parser.parse_args()
    try:
        process_tsv_file(args.file_path, args.auth, args.locale)
    except Exception as e:
        logger.error(f"An error occurred: {e}")