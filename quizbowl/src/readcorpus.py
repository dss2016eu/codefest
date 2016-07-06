import codecs
import sys
from collections import Counter
import math
import operator
import pickle
import re

class Article:

    def __init__(self, title, category, words):
        self.title = title
        self.category = category
        self.wordcounts = Counter(words)
        self.vocab = set(self.wordcounts.keys())
        for w in words:
            self.wordcounts[w] = self.wordcounts.get(w, 0) + 1
        self.length = sum(self.wordcounts.values())
        self.tfidf = {}
        self.norm = 0                  # |A|, needed for quick cosine
        self.termfreqencies = {word: self.wordcounts[word] / float(self.length) for word in self.vocab}

    def compute_norm(self):
        self.norm = math.sqrt(sum([val**2 for val in self.tfidf.values()]))

    def dotproduct(self, other):
        common_vocab = self.vocab.intersection(other.vocab)
        return sum(self.tfidf[word] * other.tfidf[word] for word in common_vocab)

    def similarity(self, other):
        """Calculate cosine between two articles."""
        return self.dotproduct(other) / float(self.norm * other.norm)

    def update_tfidf(self, doccount, docfrequencies):
        for word in self.vocab:
            if word in docfrequencies:
                self.tfidf[word] = math.log(doccount / float(docfrequencies[word])) * self.wordcounts[word]
            else:
                self.tfidf[word] = self.wordcounts[word]
        self.compute_norm()


class Wiki:

    def __init__(self):
        self.articles = set()
        self.docfrequencies = {}        # {"word": (word count in corpus, documents containing word)}
        self.articlecount = 0

    def add_article(self, article):
        self.articles.add(article)
        self.articlecount += 1
        self.update_docfrequencies(article)      # update document frequencies

    def update_docfrequencies(self, article):
        for word in article.vocab:
            self.docfrequencies[word] = self.docfrequencies.get(word, 0) + 1

    def vocab(self):
        return self.docfrequencies.keys()

    def update_tfidf(self):     # call when all articles have been added to the collection
        for article in self.articles:
            article.update_tfidf(self.articlecount, self.docfrequencies)

    def articles_similarity(self, hint_article, debug=False):
        title_to_similarity = {}
        for index, article in enumerate(self.articles, start=1):
            title_to_similarity[article.title] = hint_article.similarity(article)
            if debug and index % 10000 == 0:
                print("Computed similarity for %d documents."   % index)
        return title_to_similarity


def article_streamer(input_path, token_separator="|", debug_limit=None):
    with codecs.open(input_path) as f:
        for index, article in enumerate(f):
            split = article.strip().split("\t")
            title = split[0]
            category = split[1]
            tokens = split[-1].split(token_separator)
            yield title, category, tokens

            if debug_limit is not None and index >= debug_limit:
                break

def create_wiki(input, debug_limit=None):
    wiki = Wiki()
    for index, (title, cat, tokens) in enumerate(article_streamer(input, debug_limit=debug_limit), start=1):
        article = Article(title, cat, tokens)
        wiki.add_article(article)

        if index % 10000 == 0:
            print("Added %d articles to corpus" % index)

    wiki.update_tfidf()
    print("Finished building corpus.")
    return wiki


def correct_among_top_n(answer, ranking, top_n=1):
    topn_ranked = ranking[:top_n+1]
    return any(answer in candidate for (candidate, sim_score) in topn_ranked)


def play_quizbowl_with_stats(questions_path, wiki):
     correct_top1 = 0
     correct_top3 = 0
     correct_top5 = 0
     with codecs.open(questions_path, encoding="utf-8") as f:
        for question_index, line in enumerate(f, start=1):
            print("Question %d" % question_index)
            split = line.split(";")
            correct_answer = re.sub('"', "", split[2])
            print("Correct answer:", correct_answer)
            hint_text = split[-1]
            hints = hint_text.split("|||")
            hints_tokens = [hint.split() for hint in hints]
            for hint_index in range(1, len(hints_tokens)+1):
                hint_tokens = hints_tokens[:hint_index]
                hint_tokens = [item for sublist in hint_tokens for item in sublist]
                print(hint_index, " ".join(hint_tokens))
                hint_article = Article("hint", "UNKNOWN", hint_tokens )
                hint_article.update_tfidf(wiki.articlecount, wiki.docfrequencies)
                title_to_sim = wiki.articles_similarity(hint_article)
                sorted_title_to_sim = sorted(title_to_sim.items(), key=operator.itemgetter(1), reverse=True)[:10]
                print("Top 10 ranked answers:")
                print(sorted_title_to_sim)
                if correct_among_top_n(correct_answer, sorted_title_to_sim, 1):
                    correct_top1 += 1
                    print("Match among top 1")
                if correct_among_top_n(correct_answer, sorted_title_to_sim, 3):
                    correct_top3 += 1
                    print("Match among top 3")
                if correct_among_top_n(correct_answer, sorted_title_to_sim, 5):
                    correct_top5 += 1
                    print("Match among top 5")
            print("\n")

     print("P@1:", correct_top1/float(question_index))
     print("P@3:", correct_top3/float(question_index))
     print("P@5:", correct_top5/float(question_index))

if __name__ == '__main__':

    input = sys.argv[1]     # wiki corpus (tokenized in tsv format)
    questions_path = sys.argv[2]
    if ".pickle" in input:
        with codecs.open(input) as f:
            wiki = pickle.load(f)
    else:
        wiki = create_wiki(input, debug_limit=None)
        with codecs.open( input + ".pickle", "w") as f:
            pickle.dump(wiki, f)


    play_quizbowl_with_stats(questions_path, wiki)


