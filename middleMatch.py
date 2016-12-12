"""
middleMatch

Usage:
  middleMatch.py dump <article_number>
  middleMatch.py ripquotes <article_number>
  middleMatch.py cleanjournal <article_number>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
import json
import re


def dump(article_number):
    with open('txt/JSTOR.json') as f:
        rawCriticism = f.readlines()

    # Parse the data.
    data = [json.loads(line) for line in rawCriticism]

    return data[0][article_number]


def clean_journal(article_number):
    article = dump(article_number)

    journal = article['journal'].lower()
    texts = article['ocr']

    new_texts = []

    for text in texts:
        text = text.lower()
        text = re.sub(r"\d* " + journal + "\s*\d*", '', text)

        new_texts.append(text)

    return new_texts

def rip_quotes(article_number):
    regex = r"\"(.+?)\" \(p.+?\)"

    data = dump(article_number)

    matches = re.finditer(regex, data['ocr'][0])

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                            end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                            start=match.start(groupNum),
                                                                            end=match.end(groupNum),
                                                                            group=match.group(groupNum)))


if __name__ == "__main__":
    arguments = docopt(__doc__, version='middleMatch')

    if(arguments["dump"]):
        print(dump(int(arguments["<article_number>"]))['ocr'])

    if(arguments["ripquotes"]):
        print(rip_quotes(int(arguments["<article_number>"])))

    if(arguments["cleanjournal"]):
        print(clean_journal(int(arguments["<article_number>"])))
