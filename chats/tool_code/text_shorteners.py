import tiktoken
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain
from readability import Readability
from nltk.tokenize import RegexpTokenizer
from readability.exceptions import ReadabilityException


def convert_md_to_text(md_data: str) -> str:
    parser = MarkdownIt(renderer_cls=RendererPlain)
    return parser.render(md_data)

def count_tokens(text:str)->int:
    """Count the number of tokens in a string."""
    # gpt3 turbo - cl100k_base
    # gpt2 (or r50k_base) 	Most GPT-3 models
    # p50k_base 	Code models, text-davinci-002, text-davinci-003
    # cl100k_base 	text-embedding-ada-002
    # enc = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    token_count = len(tokens)
    return token_count


def word_count(text:str)->int:
    """Count the number of tokens in a string."""
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def readability_scores(text:str)->dict[str, float]:
    """Calculate readability scores for a string."""
    r = Readability(text)
    try:
        flesch_kincaid = round(r.flesch_kincaid().score,1)
    except ReadabilityException:
        flesch_kincaid = "N/A - low word count"

    try:
        gunning_fog = round(r.gunning_fog().score,1)
    except ReadabilityException:
        gunning_fog = "N/A - low word count"

    try:
        coleman_liau = round(r.coleman_liau().score,1)
    except ReadabilityException:
        coleman_liau = "N/A - low word count"

    return {
        "flesch_kincaid": flesch_kincaid,
        # "flesch": r.flesch(),
        "gunning_fog": gunning_fog,
        "coleman_liau": coleman_liau
    }
    # r.coleman_liau()
    # r.dale_chall()
    # r.ari()
    # r.linsear_write()
    # r.smog()
    # r.spache()


LOTS_OF_TEXT = """
Main menu

WikipediaThe Free Encyclopedia
Search Wikipedia
Search
Create account
Log in

Personal tools
Banner logo	
Participate in the 2023 international science photo competition!

[ Help with translations! ]Hide
Contents hide
(Top)
History
Flesch reading ease
Flesch–Kincaid grade level
Limitations
See also
References
Further reading
External links
Flesch–Kincaid readability tests

Article
Talk
Read
Edit
View history

Tools
From Wikipedia, the free encyclopedia

Graphs of Flesch-Kincaid reading ease (red) and grade level (gray) scores against average syllables per word and average words per sentence
The Flesch–Kincaid readability tests are readability tests designed to indicate how difficult a passage in English is to understand. There are two tests: the Flesch Reading-Ease, and the Flesch–Kincaid Grade Level. Although they use the same core measures (word length and sentence length), they have different weighting factors.

The results of the two tests correlate approximately inversely: a text with a comparatively high score on the Reading Ease test should have a lower score on the Grade-Level test. Rudolf Flesch devised the Reading Ease evaluation; somewhat later, he and J. Peter Kincaid developed the Grade Level evaluation for the United States Navy.

History
"The Flesch–Kincaid" (F–K) reading grade level was developed under contract to the U.S. Navy in 1975 by J. Peter Kincaid and his team.[1] Related U.S. Navy research directed by Kincaid delved into high-tech education (for example, the electronic authoring and delivery of technical information),[2] usefulness of the Flesch–Kincaid readability formula,[3] computer aids for editing tests,[4] illustrated formats to teach procedures,[5] and the Computer Readability Editing System (CRES).[6]

The F–K formula was first used by the Army for assessing the difficulty of technical manuals in 1978 and soon after became a United States Military Standard. Pennsylvania was the first U.S. state to require that automobile insurance policies be written at no higher than a ninth-grade level (14–15 years of age) of reading difficulty, as measured by the F–K formula. This is now a common requirement in many other states and for other legal documents such as insurance policies.[3]

Flesch reading ease
In the Flesch reading-ease test, higher scores indicate material that is easier to read; lower numbers mark passages that are more difficult to read. The formula for the Flesch reading-ease score (FRES) test is:[7]

206.835
−
1.015
(
total words
total sentences
)
−
84.6
(
total syllables
total words
)

Scores can be interpreted as shown in the table below.[7]

Score	School level (US)	Notes
100.00–90.00	5th grade	Very easy to read. Easily understood by an average 11-year-old student.
90.0–80.0	6th grade	Easy to read. Conversational English for consumers.
80.0–70.0	7th grade	Fairly easy to read.
70.0–60.0	8th & 9th grade	Plain English. Easily understood by 13- to 15-year-old students.
60.0–50.0	10th to 12th grade	Fairly difficult to read.
50.0–30.0	College	Difficult to read.
30.0–10.0	College graduate	Very difficult to read. Best understood by university graduates.
10.0–0.0	Professional	Extremely difficult to read. Best understood by university graduates.
Reader's Digest magazine has a readability index of about 65, Time magazine scores about 52, an average grade six student's written assignment (age of 12) has a readability index of 60–70 (and a reading grade level of six to seven), and the Harvard Law Review has a general readability score in the low 30s. The highest (easiest) readability score possible is 121.22, but only if every sentence consists of only one-syllable words. "The cat sat on the mat." scores 116. The score does not have a theoretical lower bound; therefore, it is possible to make the score as low as wanted by arbitrarily including words with many syllables. The sentence "This sentence, taken as a reading passage unto itself, is being used to prove a point." has a readability of 69. The sentence "The Australian platypus is seemingly a hybrid of a mammal and reptilian creature." scores 37.5 as it has 24 syllables and 13 words. While Amazon calculates the text of Moby-Dick as 57.9,[8] one particularly long sentence about sharks in chapter 64 has a readability score of −146.77.[9] One sentence in the beginning of Scott Moncrieff's English translation of Swann's Way, by Marcel Proust, has a score of −515.1.[10]

The U.S. Department of Defense uses the reading ease test as the standard test of readability for its documents and forms.[11] Florida requires that insurance policies have a Flesch reading ease score of 45 or greater.[12][13]

Use of this scale is so ubiquitous that it is bundled with popular word processing programs and services such as KWord, IBM Lotus Symphony, Microsoft Office Word, WordPerfect, WordPro, and Grammarly.

Polysyllabic words affect this score significantly more than they do the grade-level score.

Flesch–Kincaid grade level
These readability tests are used extensively in the field of education. The "Flesch–Kincaid Grade Level Formula" presents a score as a U.S. grade level, making it easier for teachers, parents, librarians, and others to judge the readability level of various books and texts. It can also mean the number of years of education generally required to understand this text, relevant when the formula results in a number greater than 10. The grade level is calculated with the following formula:[14]

0.39
(
total words
total sentences
)
+
11.8
(
total syllables
total words
)
−
15.59

The result is a number that corresponds with a U.S. grade level. The sentence, "The Australian platypus is seemingly a hybrid of a mammal and reptilian creature" is an 11.3 as it has 24 syllables and 13 words. The different weighting factors for words per sentence and syllables per word in each scoring system mean that the two schemes are not directly comparable and cannot be converted. The grade level formula emphasizes sentence length over word length. By creating one-word strings with hundreds of random characters, grade levels may be attained that are hundreds of times larger than high school completion in the United States. Due to the formula's construction, the score does not have an upper bound.

The lowest grade level score in theory is −3.40, but there are few real passages in which every sentence consists of a single one-syllable word. Green Eggs and Ham by Dr. Seuss comes close, averaging 5.7 words per sentence and 1.02 syllables per word, with a grade level of −1.3. (Most of the 50 used words are monosyllabic; "anywhere", which occurs eight times, is the only exception.)

Limitations
As readability formulas were developed for school books, they demonstrate weaknesses compared to directly testing usability with typical readers. They neglect between-reader differences and effects of content, layout and retrieval aids.[15] For example, the pangram "Cwm fjord-bank glyphs vext quiz." has a reading ease score of 100 and grade level score of 0.52 despite its obscure words.

See also
Readability
References
 Kincaid, J.P., Fishburne, R.P., Rogers, R.L., & Chissom, B.S. (1975). Derivation of new readability formulas (automated readability index, fog count, and flesch reading ease formula) for Navy enlisted personnel. Research Branch Report 8–75. Chief of Naval Technical Training: Naval Air Station Memphis.
 Kincaid JP, Braby R, Mears J (1988). "Electronic authoring and delivery of technical information". Journal of Instructional Development. 11 (2): 8–13. doi:10.1007/bf02904998. S2CID 62551107.
 McClure G (1987). "Readability formulas: Useful or useless. (an interview with J. Peter Kincaid.)". IEEE Transactions on Professional Communication. 30: 12–15. doi:10.1109/TPC.1987.6449109. S2CID 13157772.
 Kincaid JP, Braby R, Wulfeck WH II (1983). "Computer aids for editing tests". Educational Technology. 23: 29–33.
 Braby R, Kincaid JP, Scott P, McDaniel W (1982). "Illustrated formats to teach procedures". IEEE Transactions on Professional Communication. 25 (2): 61–66. doi:10.1109/TPC.1982.6447756. S2CID 30615819.
 Kincaid JP, Aagard JA, O'Hara JW, Cottrell LK (1981). "Computer Readability Editing System". IEEE Transactions on Professional Communication. 24 (1): 38–42. doi:10.1109/TPC.1981.6447821. S2CID 39045053. (also reported in Aviation Week and Space Technology, January 11, 1982, pp. 106–107.)
 Flesch, Rudolf. "How to Write Plain English". University of Canterbury. Archived from the original on July 12, 2016. Retrieved July 12, 2016.
 Gabe Habash (July 20, 2011). "Book Lies: Readability is Impossible to Measure". Archived from the original on May 21, 2014.
 Melville, Herman. "Chapter 64: Stubb's Supper." Moby-Dick. Lit2Go Edition. 1851. Web. <http://etc.usf.edu/lit2go/42/moby-dick/745/chapter-64-stubbs-supper/>. August 16, 2013.

"Though amid all the smoking horror and diabolism of a sea-fight, sharks will be seen longingly gazing up to the ship’s decks, like hungry dogs round a table where red meat is being carved, ready to bolt down every killed man that is tossed to them; and though, while the valiant butchers over the deck-table are thus cannibally carving each other’s live meat with carving-knives all gilded and tasselled, the sharks, also, with their jewel-hilted mouths, are quarrelsomely carving away under the table at the dead meat; and though, were you to turn the whole affair upside down, it would still be pretty much the same thing, that is to say, a shocking sharkish business enough for all parties; and though sharks also are the invariable outriders of all slave ships crossing the Atlantic, systematically trotting alongside, to be handy in case a parcel is to be carried anywhere, or a dead slave to be decently buried; and though one or two other like instances might be set down, touching the set terms, places, and occasions, when sharks do most socially congregate, and most hilariously feast; yet is there no conceivable time or occasion when you will find them in such countless numbers, and in gayer or more jovial spirits, than around a dead sperm whale, moored by night to a whaleship at sea."
 Proust, Marcel. "Swann's Way." In Search of Lost Time. 2004. Translated by C.K. Scott Moncrieff (1922). web. March 21, 2014.

"But I had seen first one and then another of the rooms in which I had slept during my life, and in the end I would revisit them all in the long course of my waking dream: rooms in winter, where on going to bed I would at once bury my head in a nest, built up out of the most diverse materials, the corner of my pillow, the top of my blankets, a piece of a shawl, the edge of my bed, and a copy of an evening paper, all of which things I would contrive, with the infinite patience of birds building their nests, to cement into one whole; rooms where, in a keen frost, I would feel the satisfaction of being shut in from the outer world (like the sea-swallow which builds at the end of a dark tunnel and is kept warm by the surrounding earth), and where, the fire keeping in all night, I would sleep wrapped up, as it were, in a great cloak of snug and savoury air, shot with the glow of the logs which would break out again in flame: in a sort of alcove without walls, a cave of warmth dug out of the heart of the room itself, a zone of heat whose boundaries were constantly shifting and altering in temperature as gusts of air ran across them to strike freshly upon my face, from the corners of the room, or from parts near the window or far from the fireplace which had therefore remained cold—or rooms in summer, where I would delight to feel myself a part of the warm evening, where the moonlight striking upon the half-opened shutters would throw down to the foot of my bed its enchanted ladder; where I would fall asleep, as it might be in the open air, like a titmouse which the breeze keeps poised in the focus of a sunbeam—or sometimes the Louis XVI room, so cheerful that I could never feel really unhappy, even on my first night in it: that room where the slender columns which lightly supported its ceiling would part, ever so gracefully, to indicate where the bed was and to keep it separate; sometimes again that little room with the high ceiling, hollowed in the form of a pyramid out of two separate storeys, and partly walled with mahogany, in which from the first moment my mind was drugged by the unfamiliar scent of flowering grasses, convinced of the hostility of the violet curtains and of the insolent indifference of a clock that chattered on at the top of its voice as though I were not there; while a strange and pitiless mirror with square feet, which stood across one corner of the room, cleared for itself a site I had not looked to find tenanted in the quiet surroundings of my normal field of vision: that room in which my mind, forcing itself for hours on end to leave its moorings, to elongate itself upwards so as to take on the exact shape of the room, and to reach to the summit of that monstrous funnel, had passed so many anxious nights while my body lay stretched out in bed, my eyes staring upwards, my ears straining, my nostrils sniffing uneasily, and my heart beating; until custom had changed the colour of the curtains, made the clock keep quiet, brought an expression of pity to the cruel, slanting face of the glass, disguised or even completely dispelled the scent of flowering grasses, and distinctly reduced the apparent loftiness of the ceiling."
 Luo Si; et al. (November 5–10, 2001). A statistical model for scientific readability. Atlanta, GA, USA: CIKM '01.
 "Florida Statute § 627.4145". Retrieved March 20, 2020.
 "Readable Language in Insurance Policies"
 Kincaid JP, Fishburne RP Jr, Rogers RL, Chissom BS (February 1975). "Derivation of new readability formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy enlisted personnel" (PDF). Research Branch Report 8-75, Millington, TN: Naval Technical Training, U. S. Naval Air Station, Memphis, TN. Archived (PDF) from the original on December 10, 2020.
 J. Redish, Readability formulas have even more limitations than Klare discusses, August 2000, ACM Journal of Computer Documentation 24(3):132-137, DOI:10.1145/344599.344637
Further reading
Flesch R (1948). "A new readability yardstick". Journal of Applied Psychology. 32 (3): 221–233. doi:10.1037/h0057532. PMID 18867058.
Farr JN, Jenkins JJ, Paterson DG (October 1951). "Simplification of Flesch Reading Ease Formula". Journal of Applied Psychology. 35 (5): 333–337. doi:10.1037/h0062427.
External links
readability.mackayst.com, lists Flesch–Kincaid scores of Project Gutenberg books
vte
Readability tests for English
Tests and formulas that measure the readability of a text
Automated readability index (1967)ATOSColeman–Liau index (1975)Dale–Chall readability formula (1948)Flesch–Kincaid readability tests Flesch reading ease [1975]Flesch–Kincaid grade level [1975]FORCAST (1973)Fry readability formula (1968)Gunning fog index (1952)Lexile (1989)Linsear WriteRaygor readability estimate (1977)SMOG (1969)Spache readability formula (1952)
Categories: Readability tests1975 introductions
This page was last edited on 30 November 2023, at 11:39 (UTC).
Text is available under the Creative Commons Attribution-ShareAlike License 4.0; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.
Privacy policyAbout WikipediaDisclaimersContact WikipediaCode of ConductDevelopersStatisticsCookie statementMobile viewWikimedia FoundationPowered by MediaWiki
"""
LOTS_OF_TEXT = """Project description
Faker is a Python package that generates fake data for you. Whether you need to bootstrap your database, create good-looking XML documents, fill-in your persistence to stress test it, or anonymize data taken from a production service, Faker is for you.

Faker is heavily inspired by PHP Faker, Perl Faker, and by Ruby Faker.

_|_|_|_|          _|
_|        _|_|_|  _|  _|      _|_|    _|  _|_|
_|_|_|  _|    _|  _|_|      _|_|_|_|  _|_|
_|      _|    _|  _|  _|    _|        _|
_|        _|_|_|  _|    _|    _|_|_|  _|
Latest version released on PyPI Build status of the master branch Test coverage Package license

Compatibility
Starting from version 4.0.0, Faker dropped support for Python 2 and from version 5.0.0 only supports Python 3.7 and above. If you still need Python 2 compatibility, please install version 3.0.1 in the meantime, and please consider updating your codebase to support Python 3 so you can enjoy the latest features Faker has to offer. Please see the extended docs for more details, especially if you are upgrading from version 2.0.4 and below as there might be breaking changes.

This package was also previously called fake-factory which was already deprecated by the end of 2016, and much has changed since then, so please ensure that your project and its dependencies do not depend on the old package.

Basic Usage
Install with pip:

pip install Faker
Use faker.Faker() to create and initialize a faker generator, which can generate data by accessing properties named after the type of data you want.

from faker import Faker
fake = Faker()

fake.name()
# 'Lucy Cechtelar'

fake.address()
# '426 Jordy Lodge
#  Cartwrightshire, SC 88120-6700'

fake.text()
# 'Sint velit eveniet. Rerum atque repellat voluptatem quia rerum. Numquam excepturi
#  beatae sint laudantium consequatur. Magni occaecati itaque sint et sit tempore. Nesciunt
#  amet quidem. Iusto deleniti cum autem ad quia aperiam.
#  A consectetur quos aliquam. In iste aliquid et aut similique suscipit. Consequatur qui
#  quaerat iste minus hic expedita. Consequuntur error magni et laboriosam. Aut aspernatur
#  voluptatem sit aliquam. Dolores voluptatum est.
#  Aut molestias et maxime. Fugit autem facilis quos vero. Eius quibusdam possimus est.
#  Ea quaerat et quisquam. Deleniti sunt quam. Adipisci consequatur id in occaecati.
#  Et sint et. Ut ducimus quod nemo ab voluptatum.'
Each call to method fake.name() yields a different (random) result. This is because faker forwards faker.Generator.method_name() calls to faker.Generator.format(method_name).

for _ in range(10):
  print(fake.name())

# 'Adaline Reichel'
# 'Dr. Santa Prosacco DVM'
# 'Noemy Vandervort V'
# 'Lexi O'Conner'
# 'Gracie Weber'
# 'Roscoe Johns'
# 'Emmett Lebsack'
# 'Keegan Thiel'
# 'Wellington Koelpin II'
# 'Ms. Karley Kiehn V'
Pytest fixtures
Faker also has its own pytest plugin which provides a faker fixture you can use in your tests. Please check out the pytest fixture docs to learn more.

Providers
Each of the generator properties (like name, address, and lorem) are called “fake”. A faker generator has many of them, packaged in “providers”.

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)

print(fake.ipv4_private())
Check the extended docs for a list of bundled providers and a list of community providers.

Localization
faker.Faker can take a locale as an argument, to return localized data. If no localized provider is found, the factory falls back to the default LCID string for US english, ie: en_US.

from faker import Faker
fake = Faker('it_IT')
for _ in range(10):
    print(fake.name())

# 'Elda Palumbo'
# 'Pacifico Giordano'
# 'Sig. Avide Guerra'
# 'Yago Amato'
# 'Eustachio Messina'
# 'Dott. Violante Lombardo'
# 'Sig. Alighieri Monti'
# 'Costanzo Costa'
# 'Nazzareno Barbieri'
# 'Max Coppola'
faker.Faker also supports multiple locales. New in v3.0.0.

from faker import Faker
fake = Faker(['it_IT', 'en_US', 'ja_JP'])
for _ in range(10):
    print(fake.name())

# 鈴木 陽一
# Leslie Moreno
# Emma Williams
# 渡辺 裕美子
# Marcantonio Galuppi
# Martha Davis
# Kristen Turner
# 中津川 春香
# Ashley Castillo
# 山田 桃子
You can check available Faker locales in the source code, under the providers package. The localization of Faker is an ongoing process, for which we need your help. Please don’t hesitate to create a localized provider for your own locale and submit a Pull Request (PR).

Optimizations
The Faker constructor takes a performance-related argument called use_weighting. It specifies whether to attempt to have the frequency of values match real-world frequencies (e.g. the English name Gary would be much more frequent than the name Lorimer). If use_weighting is False, then all items have an equal chance of being selected, and the selection process is much faster. The default is True.

Command line usage
When installed, you can invoke faker from the command-line:

faker [-h] [--version] [-o output]
      [-l {bg_BG,cs_CZ,...,zh_CN,zh_TW}]
      [-r REPEAT] [-s SEP]
      [-i {package.containing.custom_provider otherpkg.containing.custom_provider}]
      [fake] [fake argument [fake argument ...]]
Where:

faker: is the script when installed in your environment, in development you could use python -m faker instead

-h, --help: shows a help message

--version: shows the program’s version number

-o FILENAME: redirects the output to the specified filename

-l {bg_BG,cs_CZ,...,zh_CN,zh_TW}: allows use of a localized provider

-r REPEAT: will generate a specified number of outputs

-s SEP: will generate the specified separator after each generated output

-i {my.custom_provider other.custom_provider} list of additional custom providers to use. Note that is the import path of the package containing your Provider class, not the custom Provider class itself.

fake: is the name of the fake to generate an output for, such as name, address, or text

[fake argument ...]: optional arguments to pass to the fake (e.g. the profile fake takes an optional list of comma separated field names as the first argument)

Examples:

$ faker address
968 Bahringer Garden Apt. 722
Kristinaland, NJ 09890

$ faker -l de_DE address
Samira-Niemeier-Allee 56
94812 Biedenkopf

$ faker profile ssn,birthdate
{'ssn': '628-10-1085', 'birthdate': '2008-03-29'}

$ faker -r=3 -s=";" name
Willam Kertzmann;
Josiah Maggio;
Gayla Schmitt;
How to create a Provider
from faker import Faker
fake = Faker()

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class MyProvider(BaseProvider):
    def foo(self) -> str:
        return 'bar'

# then add new provider to faker instance
fake.add_provider(MyProvider)

# now you can use:
fake.foo()
# 'bar'
How to create a Dynamic Provider
Dynamic providers can read elements from an external source.

from faker import Faker
from faker.providers import DynamicProvider

medical_professions_provider = DynamicProvider(
     provider_name="medical_profession",
     elements=["dr.", "doctor", "nurse", "surgeon", "clerk"],
)

fake = Faker()

# then add new provider to faker instance
fake.add_provider(medical_professions_provider)

# now you can use:
fake.medical_profession()
# 'dr.'
How to customize the Lorem Provider
You can provide your own sets of words if you don’t want to use the default lorem ipsum one. The following example shows how to do it with a list of words picked from cakeipsum :

from faker import Faker
fake = Faker()

my_word_list = [
'danish','cheesecake','sugar',
'Lollipop','wafer','Gummies',
'sesame','Jelly','beans',
'pie','bar','Ice','oat' ]

fake.sentence()
# 'Expedita at beatae voluptatibus nulla omnis.'

fake.sentence(ext_word_list=my_word_list)
# 'Oat beans oat Lollipop bar cheesecake.'
How to use with Factory Boy
Factory Boy already ships with integration with Faker. Simply use the factory.Faker method of factory_boy:

import factory
from myapp.models import Book

class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author_name = factory.Faker('name')
Accessing the random instance
The .random property on the generator returns the instance of random.Random used to generate the values:

from faker import Faker
fake = Faker()
fake.random
fake.random.getstate()
By default all generators share the same instance of random.Random, which can be accessed with from faker.generator import random. Using this may be useful for plugins that want to affect all faker instances.

Unique values
Through use of the .unique property on the generator, you can guarantee that any generated values are unique for this specific instance.

from faker import Faker
fake = Faker()
names = [fake.unique.first_name() for i in range(500)]
assert len(set(names)) == len(names)
Calling fake.unique.clear() clears the already seen values. Note, to avoid infinite loops, after a number of attempts to find a unique value, Faker will throw a UniquenessException. Beware of the birthday paradox, collisions are more likely than you’d think.

from faker import Faker

fake = Faker()
for i in range(3):
     # Raises a UniquenessException
     fake.unique.boolean()
In addition, only hashable arguments and return values can be used with .unique.

Seeding the Generator
When using Faker for unit testing, you will often want to generate the same data set. For convenience, the generator also provide a seed() method, which seeds the shared random number generator. Seed produces the same result when the same methods with the same version of faker are called.

from faker import Faker
fake = Faker()
Faker.seed(4321)

print(fake.name())
# 'Margaret Boehm'
Each generator can also be switched to its own instance of random.Random, separate to the shared one, by using the seed_instance() method, which acts the same way. For example:

from faker import Faker
fake = Faker()
fake.seed_instance(4321)

print(fake.name())
# 'Margaret Boehm'
Please note that as we keep updating datasets, results are not guaranteed to be consistent across patch versions. If you hardcode results in your test, make sure you pinned the version of Faker down to the patch number.

If you are using pytest, you can seed the faker fixture by defining a faker_seed fixture. Please check out the pytest fixture docs to learn more.

Tests
Run tests:

$ tox
Write documentation for the providers of the default locale:

$ python -m faker > docs.txt
Write documentation for the providers of a specific locale:

$ python -m faker --lang=de_DE > docs_de.txt
Contribute
Please see CONTRIBUTING.

License
Faker is released under the MIT License. See the bundled LICENSE file for details.

Credits
FZaninotto / PHP Faker

Distribute

Buildout

modern-package-template"""

LOTS_OF_TEXT = """Yasmeen Lari spent a four-decade career designing award-winning structures out of concrete, glass and steel before stumbling into her ideal material.

It was at a camp for refugees from military conflict in Pakistan’s northwestern Swat Valley. Residents there were struggling to secure bricks and wood to build communal kitchens — until she spotted a nearby bamboo grove.

“Let’s use it,” recalls Lari, who by that time had shuttered her architecture practice to focus on humanitarian work. “I’d never thought of using bamboo in my life.”

The material worked so well that over the last decade, Heritage Foundation of Pakistan, the group Lari started in 1980 to preserve the country’s traditional architecture, has built some 85,000 structures for displaced Pakistanis, including victims of last year’s devastating monsoon rains.

That disaster, the worst flooding in Pakistani history, left a third of the country underwater and destroyed more than 2.1 million homes. The thousands of bamboo structures Lari’s group had erected “all survived,” she said.

(Saiyna Bashir for The Washington Post)
How to rebuild quickly, cheaply and well is becoming an increasingly pressing question as climate change intensifies natural disasters. More extreme fires and floods are destroying communities around the world. But so far, most of the emergency shelters that pop up in their aftermath tend to be expensive and inefficient.


Priya spreads a quilt inside her bamboo home in Mirpur Khas, Pakistan. (Saiyna Bashir for The Washington Post)

Dhani received training on how to build flood-resistant sustainable bamboo homes after last year's catastrophic floods in Pakistan. She then trained others in her village. (Saiyna Bashir for The Washington Post)

Raheela cooks in an outdoor kitchen, a tenet of the new sustainable bamboo villages. (Saiyna Bashir for The Washington Post)
These makeshift structures are not built to last, but many disaster victims end up living in temporary encampments for years as they wait for more permanent dwellings to materialize.

Rebuilding is a particularly tough challenge in poorer countries, such as Pakistan, that face the most severe effects of climate change despite emitting a fraction of the world’s carbon.


Yasmeen Lari, a guest lecturer at Jesus College at the University of Cambridge, leads an initiative to build bamboo homes in Pakistan. (Tori Ferenc for The Washington Post)
So Lari is building more bamboo homes. One million more.

These are not disaster relief shelters, she insists, but disaster-resistant homes.

“This country can’t afford the luxury of obsolescence,” said Lari, who earlier this year won an award from the Royal Institute of British Architects. “Whatever we build must be long lasting.”

‘A marvelous material’
When Lari won a 2016 Fukuoka Prize, which celebrated her contributions to the preservation of Asian culture, event organizers asked her where in Japan she’d like to visit. She suggested Kumamoto, in southern Japan, which had just suffered intense earthquakes.

As she walked through its streets, she could spot the bare edges of buildings that plaster had once covered, “but the bamboo was still standing inside,” she said. “And the city is 400 years old.”

(Saiyna Bashir for The Washington Post)
Many species of bamboo have been used as a building material in Asia for thousands of years and they are among the world’s fastest-growing plants. A type of grass, bamboo can be ready for harvest in as little as three years, a fraction of the time needed for timber wood to grow. Like manufactured timber, bamboo products can store carbon, and bamboo forests perform well as carbon sinks, meaning they absorb more carbon than they release.


The Vasram village in Mirpur Khas is part of Yasmeen Lari’s bamboo homes initiative. (Saiyna Bashir for The Washington Post)

Residents carry bamboo leaves to add them to their homes. (Saiyna Bashir for The Washington Post)

The ceiling of a bamboo home, viewed from inside. (Saiyna Bashir for The Washington Post)
Its strong, consistent fibers give it mechanical properties comparable to the most durable manufactured materials.

“Architects call it natural steel,” said Liu Kewei, an engineer and member of the International Bamboo and Rattan Organization, who has worked on bamboo construction projects from China to Ecuador. “It’s really a marvelous material.”

Bamboo doesn’t always last as long as modern concrete, which has a life span of 50 to 100 years, but it can stand for at least 25. And, according to Lari, it often lasts much longer.

She is one of a growing number of architects pushing a modern bamboo renaissance. In the Philippines, engineering graduate Earl Forlales created a modular home known as Cubo, a reimagining of the traditional bamboo hut that can be constructed in four hours. Vietnamese architect Vo Trong Nghia has used bamboo to create grand latticed structures at numerous eco-friendly luxury resorts. In Bali, architect Elora Hardy and her company, Ibuku, have won plaudits for bending bamboo into sweeping shapes to make bespoke restaurants and houses.

Lari, meanwhile, has traded in the imposing designs of her previous career for simple dwellings that exploit bamboo’s ability to withstand extreme flooding. Bamboo rods may not always be the right building material beyond the tropical and subtropical climates where it grows easily, but in places like Pakistan, where monsoon rains and glacial melt have already displaced hundreds of thousands, it makes sense.

“As it is all tied together, it moves together,” Lari said of her bamboo hut model. “It might swell a bit, but it will come back to its shape.”

A copy-paste design
Lari designed some of Pakistan’s most recognizable buildings during the 1980s and 1990s, such as Karachi’s Finance and Trade Center, a hulking building using passive cooling for natural ventilation, and the Pakistan State Oil House, with its cascading glass facade. She retired from her practice in 2000 to focus on humanitarian work and to preserve historic buildings, a pivot she often says is meant to “atone” for her past.

“Every architect waits for that commission to do something spectacular,” Lari said. “But permission always comes from the rich … whether it was the Medicis of Florence, the robber barons of the East India Company, whoever they were.”

(Saiyna Bashir for The Washington Post)
Lari’s current project subverts that structure. The bamboo homes, which combine mud and limestone facades with inner bamboo skeletons or bamboo roofs, are designed to be copied and pasted across Pakistan and perhaps, beyond its borders. Her foundation’s free YouTube videos show how to build the homes.


A woman mixes a binding agent before applying it to her home, which is under construction in the Vasram village. (Saiyna Bashir for The Washington Post)

Women apply a binding agent to protect the mud wall of a bamboo home in Mirpur Khas. (Saiyna Bashir for The Washington Post)

Men work at a construction site at a bamboo village where residents have been trained in building bamboo homes. (Saiyna Bashir for The Washington Post)
A crew without much technical knowledge can manufacture and assemble the structures’ eight panels and the interior bamboo beams that support them on-site. Lari designed them so that homeowners can easily make repairs and even additions.

“If bamboo is taken care of,” she said, “bamboo can last forever.”

If a flood is coming, homeowners can dismantle the structure’s bamboo skeleton from its permanent foundation and move it to higher ground. Bigger buildings, such as community centers, stand on stilts several feet high.


Champa has trained other women in her village how to reconstruct their homes. (Saiyna Bashir for The Washington Post)
Lari’s plan to build 1 million homes calls for clusters of about 5,000 dwellings to sprout up across Pakistan’s most flood-damaged throughout this year and next.

Each of these permanent homes would cost just $176, Lari said, providing safe shelter for Pakistan’s flood victims and laying a foundation for sustainable recovery from future climate disasters.

Lari has used “intelligent yet simple” designs to “allow those who are in distress to build for their own needs,” said Simon Allford, chair of the Royal Institute of British Architects Honors Committee, which awarded Lari its 2023 Royal Gold Medal for Architecture. “She is a pioneer in designing architecture for disaster relief.”

(Saiyna Bashir for The Washington Post)
Each village shares its resources — community kitchens, vegetable and fish farms, chicken coops and production centers. The clusters also encourage women to be breadwinners and decision-makers — a principle deeply important to Lari, who broke through a male-dominated field to become Pakistan’s first practicing female architect.


A woman works at her tailoring shop in Vasram. (Saiyna Bashir for The Washington Post)

Dhani, pictured with her sister-in-law and nieces, was trained to build bamboo homes. (Saiyna Bashir for The Washington Post)

Champa walks in her village. (Saiyna Bashir for The Washington Post)
The daughter of a colonial officer, Lari said she was privileged to be able to study in Britain, then design homes upon returning to Pakistan. She describes her rise as blessed, but not without challenges. Male colleagues would make her life difficult, placing rickety ladders at job sites. “They wanted to test me,” she said.

Now 82, Lari continues to carve her own way. While others working to rebuild after recent floods are relying on donations, she’s funding her project through microloans meant to jump-start small businesses within the communities, so every cluster of homes will ultimately pay for itself.


“Whatever we build must be long lasting,” Lari says. (Tori Ferenc for The Washington Post)
“I am no longer relying on outside funding,” she said. “My communities will reach the target themselves with their own resources.”

At Pono village, a pilot cluster in Sindh province, residents have become self-sufficient by producing everything from terra cotta products to goat milk.

It’s a far cry from broad multinational relief efforts. Last year, the Pakistani government estimated it had suffered $40 billion in damage. In August 2022, it launched a response plan to raise $816 million for flood relief. Nearly a year later, it had met less than 70 percent of its goal.

The World Bank and the government of the Pakistani province of Sindh, for example, have used $500 million in donations thus far to build 380 temporary, high-carbon one-room houses after last year’s floods.

Lari’s foundation has built almost 40,000 homes since the 2022 floods, she estimates. She expects to complete 1 million by 2024 or 2025.

Rising waters won’t stop the project, said Lari. She has plans for future villages that could use moats and bamboo green walls to keep out water. Some are already experimenting with growing crops on raised platforms, inspired by structures at Sindh province’s famed archaeological site of Mohenjo-Daro, a city of at least 40,000 people built around 2500 B.C. and occupied for centuries.

“I’m just learning from everything that’s been there,” said Lari.

“If I could find a way to spread it everywhere — if I could go cluster by cluster, hub by hub, I want to do it that way.”
"""
if __name__ == '__main__':
    print(count_tokens(LOTS_OF_TEXT))
    print(readability_scores(LOTS_OF_TEXT))
    print(word_count(LOTS_OF_TEXT))