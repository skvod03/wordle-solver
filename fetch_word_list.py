import re
import requests

def fetch_word_list():
    print('Fetching word list...')
    # get list of five-letter words from meaningpedia.com
    meaningpedia_resp = requests.get(
        "https://meaningpedia.com/5-letter-words?show=all"
    )

    # compile regex to extract words from the HTML
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    word_list = pattern.findall(meaningpedia_resp.text)
    return word_list

if __name__ == "__main__":
    words = fetch_word_list()
    print(f"Fetched {len(words)} words.")
    # You can save it to a file or process further
    with open('five_letter_words.txt', 'w') as f:
        for word in words:
            f.write(word + '\n')