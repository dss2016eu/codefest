import codecs
import sys
from collections import Counter
import math
import operator
import re
import json
import nltk

class Article:

    def __init__(self, title, category, words):
        self.title = title
        self.category = category
        self.wordcounts = Counter(words)
        self.length = sum(self.wordcounts.values())
        self.tfidf = {}
        self.norm = 0                  # |A|, needed for quick cosine
        self.termfreqencies = {word: self.wordcounts[word] / float(self.length) for word in self.wordcounts.keys()}

    def compute_norm(self):
        self.norm = math.sqrt(sum([val**2 for val in self.tfidf.values()]))

    def dotproduct(self, other):
        vocab = set(self.wordcounts.keys())
        other_vocab = set(other.wordcounts.keys())
        common_vocab = vocab.intersection(other_vocab)
        return sum(self.tfidf[word] * other.tfidf[word] for word in common_vocab)

    def similarity(self, other):
        """Calculate cosine between two articles."""
        return self.dotproduct(other) / float(self.norm * other.norm)

    def update_tfidf(self, doccount, docfrequencies):
        for word in self.wordcounts.keys():
            if word in docfrequencies:
                self.tfidf[word] = math.log(doccount / float(docfrequencies[word])) * (1 + math.log(self.wordcounts[word]))
            else:
                self.tfidf[word] = self.wordcounts[word]
        self.compute_norm()

    def __repr__(self):
        return "Article(title=%r, category=%r)"  % (self.title, self.category)


class Wiki:

    def __init__(self):
        self.articles = []
        self.docfrequencies = {}        # {"word": (word count in corpus, documents containing word)}
        self.articlecount = 0

    def add_article(self, article):
        self.articles.append(article)
        self.articlecount += 1
        self.update_docfrequencies(article)      # update document frequencies

    def update_docfrequencies(self, article):
        for word in article.wordcounts.keys():
            self.docfrequencies[word] = self.docfrequencies.get(word, 0) + 1

    def vocab(self):
        return self.docfrequencies.keys()

    def update_tfidf(self):     # call when all articles have been added to the collection
        for article in self.articles:
            article.update_tfidf(self.articlecount, self.docfrequencies)

    def articles_similarity(self, hint_article, debug=False):
        titlecat_to_similarity = {}
        for index, article in enumerate(self.articles, start=1):
            titlecat_to_similarity[(article.title, article.category)] = hint_article.similarity(article)
            if debug and index % 10000 == 0:
                print("Computed similarity for %d documents."   % index)
        return titlecat_to_similarity


def article_streamer(input_path, token_separator="|", debug_limit=None, length_filter=None):
    skipped_count = 0
    with codecs.open(input_path, encoding="utf-8") as f:
        for index, article in enumerate(f):
            split = article.strip().split("\t")
            title = split[0]
            category = split[1]
            tokens = split[-1].split(token_separator)
            if length_filter is not None and len(tokens) <= length_filter:
                skipped_count += 1
                if skipped_count % 10000 == 0:
                    print("%d. %s skipped" % (skipped_count, title))
                continue
            yield title, category, tokens

            if debug_limit is not None and index >= debug_limit:
                break
        print("Altogether %d articles skipped" % (skipped_count))


def create_wiki(input, debug_limit=None, length_filter=None):
    wiki = Wiki()
    for index, (title, cat, tokens) in enumerate(article_streamer(input, debug_limit=debug_limit, length_filter=length_filter), start=1):
        article = Article(title, cat, tokens)
        wiki.add_article(article)

        if index % 10000 == 0:
            print("Added %d articles to corpus" % index)

    wiki.update_tfidf()
    print("Finished building corpus.")
    return wiki


def correct_among_top_n(answer, ranking, top_n=1):
    topn_ranked = ranking[:top_n+1]
    return any(answer in candidate_title for ((candidate_title, candidate_cat), sim_score) in topn_ranked)


def title_contained_in_hint(candidate_title, hint_str):
    tokenized_title = nltk.word_tokenize(candidate_title)
    tokenized_title_entities = [word for word in tokenized_title if word[0].isupper()]
    return any(entity in hint_str for entity in tokenized_title_entities)


def filter_pattern(pattern_file, tokenized_words):
    wstring = ' '.join(tokenized_words)
    filterlines = [line.strip() for line in codecs.open(pattern_file, "r", encoding="utf-8")]
    for l in filterlines:
        pattern, reply = l.split('\t')
        if re.search(pattern, wstring, flags=re.IGNORECASE):
            return reply
    return "UNKNOWN"


def rank_articles(hint_str, wiki, filter_patterns, top_n):
    tokenized = nltk.word_tokenize(hint_str)
    hint_article = Article("hint", "UNKNOWN", tokenized)
    hint_article.update_tfidf(wiki.articlecount, wiki.docfrequencies)
    titlecat_to_sim = wiki.articles_similarity(hint_article)
    sorted_title_to_sim = sorted(titlecat_to_sim.items(), key=operator.itemgetter(1), reverse=True)[:100]
    return_titles = []
    articles_counter = 0
    desired_category = filter_pattern(filter_patterns, tokenized)
    print("Desired category", desired_category)
    for (candidate_title, candidate_category), candidate_sim in sorted_title_to_sim:
        if title_contained_in_hint(candidate_title, hint_str):         # check if title in contained in hint
            continue
        if desired_category != "UNKNOWN" and desired_category not in candidate_category:
            continue
        return_titles.append(((candidate_title, candidate_category), candidate_sim))
        articles_counter += 1
        if articles_counter >= top_n:
            break
    return return_titles


def rank_articles_for_all_hints(hints_str, wiki, filter_patterns, top_n):
    hints = hints_str.split("|||")
    for hint_index in range(1, len(hints)+1):
        hint = hints[:hint_index]
        hint_str = " ".join(hint)
        topn_articles = rank_articles(hint_str, wiki, filter_patterns, top_n)
        yield hint_str, topn_articles


def play_quizbowl_with_stats(questions_path, wiki, filter_patterns):
     correct_top1 = correct_top3 = correct_top5 = 0
     hints_counter = 0
     with codecs.open(questions_path, encoding="utf-8") as f:
        for question_index, line in enumerate(f, start=1):
            print("Question %d" % question_index)
            split = line.split(";")
            correct_answer = re.sub('"', "", split[2])
            print("Correct answer:", correct_answer)
            print("\n")
            hints_str = split[-1]
            for hint_str, topn_articles in rank_articles_for_all_hints(hints_str, wiki, filter_patterns, top_n=10):
                print("Hint", hint_str)
                hints_counter += 1
                print("Top 10 ranked answers:")
                print(topn_articles)
                if correct_among_top_n(correct_answer, topn_articles, 1):
                    correct_top1 += 1
                    print("Match among top 1")
                if correct_among_top_n(correct_answer, topn_articles, 3):
                    correct_top3 += 1
                    print("Match among top 3")
                if correct_among_top_n(correct_answer, topn_articles, 5):
                    correct_top5 += 1
                    print("Match among top 5")
                print("\n")
            print("\n")

     print("P@1:", correct_top1/float(hints_counter))
     print("P@3:", correct_top3/float(hints_counter))
     print("P@5:", correct_top5/float(hints_counter))


def json_serialiser(output_path, wiki):
    with codecs.open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({"docfrequencies": wiki.docfrequencies,
                            "articlecount": wiki.articlecount}).encode("utf-8"))
        f.write("\n")
        for article in wiki.articles:
            f.write(json.dumps(article.__dict__).encode("utf-8"))
            f.write("\n")


def json_deserialiser(input_path):
    wiki = Wiki()
    with codecs.open(input_path, encoding="utf-8") as f:
        first = json.loads(next(f))
        wiki.docfrequencies = first["docfrequencies"]
        wiki.articlecount = first["articlecount"]
        wiki_articles = []
        for line in f:
            article = Article("", "", [])
            article.__dict__ = json.loads(line)
            wiki_articles.append(article)
        wiki.articles = wiki_articles
    return wiki


if __name__ == '__main__':

    input_path = sys.argv[1]     # wiki corpus (tokenized in tsv format)
    questions_path = sys.argv[2]
    patterns_path = "../EU/input_patterns.csv" if len(sys.argv) <= 3 else sys.argv[3]

    if ".json" in input_path:
        wiki = json_deserialiser(input_path)
        print("Wiki corpus loaded from %s" % input_path)

    else:
        wiki = create_wiki(input_path, debug_limit=None, length_filter=100)
        json_path = input_path + ".json"
        # json_serialiser(json_path, wiki)
        # print("Wiki dumped to %s" % json_path)

    play_quizbowl_with_stats(questions_path, wiki, filter_patterns=patterns_path)



