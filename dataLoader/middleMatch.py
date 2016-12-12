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


class MiddleMatch:
    def clean_journal(self, article_number):
        article = self.dump(article_number)

        journal = article['journal'].lower()
        texts = article['ocr']

        new_texts = []

        count = 0

        for text in texts:
            text = text.lower()
            text, number = re.subn(r"\d* " + journal + "\s*\d*", '', text)
            count += number

            new_texts.append(text)

        return new_texts


    def rip_quotes(self, article_number):
        regex = r"\"(.+?)\" \(p.+?\)"

        data = self.dump(article_number)

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

    def dump(self, article_number):
        with open('../txt/JSTOR.json') as f:
            rawCriticism = f.readlines()

        # Parse the data.
        data = [json.loads(line) for line in rawCriticism]

        return data[0][article_number]


if __name__ == "__main__":
    arguments = docopt(__doc__, version='middleMatch')

    mm = MiddleMatch()

    if(arguments["dump"]):
        print(mm.dump(int(arguments["<article_number>"]))['ocr'])

    if(arguments["ripquotes"]):
        print(mm.rip_quotes(int(arguments["<article_number>"])))

    if(arguments["cleanjournal"]):
        print(mm.clean_journal(int(arguments["<article_number>"])))
