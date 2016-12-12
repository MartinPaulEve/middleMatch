import json
import unittest
from dataLoader.middleMatch import MiddleMatch
from TextMatcher import Text, Matcher


class TestDocumentZero(unittest.TestCase):
    article = None
    novel = None
    verification_errors = []

    matches = ["And how should Dorothea not marry?","A young lady of some birth and fortune, who knelt suddenly down on a brick floor by the side of a sick labourer and prayed fervidly","Your sister is given to self-mortification, is she not?","Her mind was theoretic, and yearned by its nature after some lofty conception of the world which might frankly include the parish of Tipton and her own rule of conduct there; she was enamoured of intensity and greatness, and rash in embracing whatever seemed to her to have those aspects; likely to seek martyrdom, to make retractations, and then to incur martyrdom after all in a quarter where she had not sought it.", "I think she is.... She likes giving up","I think we deserve to be beaten out of our beautiful houses with a scourge of small cords,","It is not a sin to make yourself poor in performing experiments for the good of all","I wish her joy of her hair shirt","she might not dread the corrosiveness of Celia\'s pretty carnally-minded prose","Her whole soul was possessed by the fact that a fuller life was opening before her: she was a neophyte about to enter on a higher grade of ini- tiation","is something like the ghost of an ancient,","seemed like a specimen from a mine, or the inscription on the door of a museum","some one quite young,","\'Der Neffe als Onkel\' in a tragic sense-ungeheuer!","It had once or twice crossed his mind that possibly there was some deficiency in Dorothea to account for the moderation of his abandonment","the stream of feeling","Mark my words: in a year from this time that girl will hate him","some discouragement, some faintness of heart at the new real future which replaces the imaginary, is not unusual","against any absolute conclusion,","at present this caution against a too hasty judgment interests me more in relation to Mr. Casaubon than to his young cousin","Dear me, what a very animated con- versation Miss Brooke seems to be having with this Mr. Lydgate!","She is talking cottages and hospitals with him,","the moment of vocation had come","the world was made new to him by.... the growth of an intellectual passion.","his scientific interest soon took the form of a professional enthusi- asm","meanness of opportunity","about 1829 the dark territories of Pathology were a fine America for a spirited young adventurer","believing that illu- sions were at an end for him.... He had more reason than ever for trusting his judgment, now that it was so experienced","spiritual grandeur","retarding friction","you and me,","coherent social faith and order.","a title to everlasting fame","some long-recognisable deed,","small temptations and sordid cares","a life of mistakes","dispersed among hindrances.","henceforth he would take a strictly scientific view of woman....","There was another attraction in [Lydgate\'s] profession: it wanted reform....","... to shape their own deeds and alter the world a little.","But the moment of vocation had come, and . .. the world was made new to him by a pre- sentiment of endless processes filling the vast spaces planked out of his sight by that wordy ignorance which he had sup- posed to be knowledge.","This great seer [Bichat] did not go beyond the consideration of the tissues as ultimate facts in the living organism, marking the limit of anatomical analysis....","... the social lot of women might be treated with scientific certitude.","[Saint Theresa] found her epos in the reform of a religious order.","... to shape their thought and deed in noble agreement....","Theresa\'s passionate, ideal na- ture.... soared after some il- limitable satisfaction, some object which would never jus- tify weariness, which would reconcile self-despair with the rapturous consciousness of life beyond self.","... so much subtler is a human mind than the outside tissues which make a sort of blazonry or clock-face for it.","Even with a microscope directed on a water-drop we find ourselves making interpretations which turn out to be rather coarse; for whereas under a weak lens you may seem to see a creature ex- hibiting an active voracity into which other smaller creatures ac- tively play as if they were so many animated tax-pennies, a stronger lens reveals to you certain tiniest hairlets which make vortices for these victims while the swallower waits passively at his receipt of custom. In this way, metaphorically speaking, a strong lens applied to Mrs. Cadwallader\'s match-making will show a play of minute causes producing what may be called thought and speech vortices to bring her the sort of food she needed."]

    def setUp(self):
        # Load the data (in this case, document 0)
        mm = MiddleMatch()

        # Parse the data.
        article_data = mm.dump(0)
        self.article = Text(article_data['ocr'], 'Document 0', removeStopwords=False)

        # Load Middlemarch itself
        with open('../txt/middlemarch.txt') as f:
        #with open('../public_texts/section.txt') as f:
            rawMM = f.read()

        self.novel = Text(rawMM, 'Middlemarch', removeStopwords=False)

        self.maxDiff = None

    def tearDown(self):
        self.assertEqual([], self.verification_errors)

    def test_matcher(self):
        num_matches, locations_a, locations_b = Matcher(self.novel, self.article, ngramSize=3, threshold=5).match()

        text = self.novel.get_text().replace("\n", " ")

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
