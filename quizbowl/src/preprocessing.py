import sys
import re
import nltk
import codecs
# nltk.download('punkt')


default_encoding = "utf-8"


def remove_simple_brackets(line):
    old_line = "X"
    while old_line != line:
        old_line = line
        line = re.sub("(.*?)\[{2}(\w*?)\]{2}(.*)", r"\1\2\3", line) # just remove the brackets
    return line


def remove_pipe_brackets(line):
    old_line = "X"
    while old_line != line:
        old_line = line
        line = re.sub("(.*?)\[{2}([^|\]{2}]*)\|(.*?)\]{2}(.*)", r"\1\3\4", line)    # for taking the second expression
    return line


def remove_link_brackets(line):
    old_line = "X"
    while old_line != line:
        old_line = line
        line = re.sub("(.*?)\[{2}[^\]{2}]*?:.*?\]{2}(.*)", r"\1\2", line)      # for links
    return line


def remove_brackets(line):
    line = remove_simple_brackets(line)
    line = remove_link_brackets(line)
    line = remove_pipe_brackets(line)
    return line


def yield_line(filepath):
    with codecs.open(filepath, "r", encoding=default_encoding) as f:
        for line in f:
            yield line


def parse_wikipedia(input_file, output_file, categories=None, tokenize=True, separator="|", debug_limit=None):
    writer = codecs.open(output_file, "w", encoding=default_encoding)
    title_to_text = {}
    default_category = "UNKNOWN"
    article_count = 1
    current_text = []
    for index, line in enumerate(yield_line(input_file), start=1):
        line = line.strip()
        mediawiki_opened = False
        if line:
            if "<doc id" in line:
                split = line.split("\"")
                title = split[-2]
                if "MediaWiki:" in title:       # ignore these articles
                    mediawiki_opened = True
                    continue
                print(article_count, title.encode(default_encoding))
                article_count += 1
                current_text = []
                title_to_text[title] = current_text
                last_title = title
            elif "</doc>" in line:
                mediawiki_opened = False
                writer.write(last_title + "\t")
                category = categories[last_title] if categories is not None and last_title in categories \
                    else default_category
                writer.write(category + "\t")
                writer.write(separator.join(current_text))
                writer.write("\n")
                current_text = []
            else:
                if not mediawiki_opened:
                    line = remove_brackets(line)
                    if tokenize:
                        tokenized = nltk.word_tokenize(line)
                        current_text.extend(tokenized)
                    else:
                        current_text.append(line)

        if debug_limit is not None and index >= debug_limit:
            break

    writer.close()


def parse_titles(input_file, output_file, debug_limit=None):
    writer = codecs.open(output_file, "w", encoding=default_encoding)
    article_count = 1
    for index, line in enumerate(yield_line(input_file), start=1):
        line = line.strip()
        mediawiki_opened = False
        if line:
            if "<doc id" in line:
                split = line.split("\"")
                id = split[1]
                title = split[-2]
                if "MediaWiki:" in title:
                    mediawiki_opened = True
                    continue
                print(article_count, title.encode(default_encoding))
                article_count += 1
                writer.write(id + "\t")
                writer.write(title)
                writer.write("\n")

        if debug_limit is not None and index >= debug_limit:
            break

    writer.close()


def read_dbpedia_categories(input):
    title_to_categories = {}
    with codecs.open(input, encoding=default_encoding) as f:
        for line in f:
            split = line.split("\t")
            title = re.sub("_", " ", split[0])
            categories = split[-1]
            title_to_categories[title] = categories
    return title_to_categories

if __name__ == "__main__":

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    title_to_categories = None
    if len(sys.argv) > 3:
        title_to_categories = read_dbpedia_categories(sys.argv[3])
        print(title_to_categories.items()[:10])
        print(title_to_categories["Asia"])

    parse_wikipedia(input_file, output_file, categories=title_to_categories)

    # parse_titles(input_file, output_file)
