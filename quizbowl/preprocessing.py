import sys
import re
import nltk
# nltk.download('punkt')


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
    with open(filepath, "r") as f:
        for line in f:
            yield line


def parse_wikipedia(input_file, output_file, tokenize=True, separator="|"):
    writer = open(output_file, "w")
    title_to_text = {}
    default_category = "CATEGORY"
    article_count = 1
    for index, line in enumerate(yield_line(input_file), start=1):
        line = line.strip()
        mediawiki_opened = False
        if line:
            if "<doc id" in line:
                split = line.split("\"")
                title = split[-2]
                if "MediaWiki:" in title:
                    mediawiki_opened = True
                    continue
                print(article_count, title)
                article_count += 1
                current_text = []
                title_to_text[title] = current_text
                last_title = title
            elif "</doc>" in line:
                mediawiki_opened = False
                writer.write(last_title + "\t")
                writer.write(default_category + "\t")           # category to be replaced later with real category
                writer.write(separator.join(current_text))
                writer.write("\n")
            else:
                if not mediawiki_opened:
                    line = remove_brackets(line)
                    if tokenize:
                        tokenized = nltk.word_tokenize(line)
                        current_text.extend(tokenized)
                    else:
                        current_text.append(line)

    writer.close()



if __name__ == "__main__":

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parse_wikipedia(input_file, output_file)