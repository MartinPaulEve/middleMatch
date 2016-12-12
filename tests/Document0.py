import json
import unittest
from dataLoader.middleMatch import MiddleMatch
from TextMatcher import Text, Matcher

class TestDocumentZero(unittest.TestCase):
    article = None
    novel = None
    verification_errors = []

    matches = ["And how should Dorothea not marry?","A young lady of some birth and fortune, who knelt suddenly down on a brick floor by the side of a sick labourer and prayed fervidly","Your sister is given to self-mortification, is she not?", "I think she is.... She likes giving up","I think we deserve to be beaten out of our beautiful houses with a scourge of small cords,","It is not a sin to make yourself poor in performing experiments for the good of all","I wish her joy of her hair shirt","she might not dread the corrosiveness of Celia\'s pretty carnally-minded prose","Her whole soul was possessed by the fact that a fuller life was opening before her: she was a neophyte about to enter on a higher grade of ini- tiation","is something like the ghost of an ancient,","seemed like a specimen from a mine, or the inscription on the door of a museum","some one quite young,","\'Der Neffe als Onkel\' in a tragic sense-ungeheuer!","It had once or twice crossed his mind that possibly there was some deficiency in Dorothea to account for the moderation of his abandonment"]

    def setUp(self):
        # Load the data (in this case, document 0)
        mm = MiddleMatch()

        # Parse the data.
        article_data = mm.dump(0)
        self.article = Text(article_data['ocr'], 'Document 0', removeStopwords=False)

        # Load Middlemarch itself
        with open('../txt/middlemarch.txt') as f:
            rawMM = f.read()

        self.novel = Text(rawMM, 'Middlemarch', removeStopwords=False)

        self.maxDiff = None

    def tearDown(self):
        self.assertEqual([], self.verification_errors)

    def test_matcher(self):
        num_matches, locations_a, locations_b = Matcher(self.novel, self.article, ngramSize=2, threshold=5).match()

        text = self.novel.get_text()

        for match in self.matches:
            found = False

            for loc_a in locations_a:
                if match.lower() == text[int(loc_a[0]): int(loc_a[1])].lower():
                    found = True

            try:
                # test if this is a straight match
                match_location = text.find(match)

                if match_location > 0:
                    msg = "Unable to find '{0}' but it occurs in the text at position {1}".format(match, match_location)
                else:
                    msg = "Unable to find '{0}'".format(match)

                self.assertEqual(found, True, msg=msg)
            except AssertionError as e:
                self.verification_errors.append(str(e))



if __name__ == '__main__':
    unittest.main()
