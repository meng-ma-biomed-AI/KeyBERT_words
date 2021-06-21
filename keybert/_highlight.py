import re
from rich.console import Console
from rich.highlighter import RegexHighlighter


class NullHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = ""
    highlights = [r""]


def highlight_document(doc, keywords):
    keywords_only = [keyword for keyword, _ in keywords]
    max_len = max([len(token.split(" ")) for token in keywords_only])

    if max_len == 1:
        highlighted_text = _highlight_one_gram(doc, keywords_only)
    else:
        highlighted_text = _highlight_n_gram(doc, keywords_only)

    console = Console(highlighter=NullHighlighter())
    console.print(highlighted_text)


def _highlight_one_gram(doc, keywords):
    tokens = re.sub(r' +', ' ', doc.replace("\n", " ")).split(" ")

    highlighted_text = " ".join([f"[black on #FFFF00]{token}[/]"
                                 if token.lower() in keywords
                                 else f"{token}"
                                 for token in tokens]).strip()
    return highlighted_text


def _highlight_n_gram(doc, keywords):
    max_len = max([len(token.split(" ")) for token in keywords])
    tokens = re.sub(r' +', ' ', doc.replace("\n", " ")).strip().split(" ")
    n_gram_tokens = [[" ".join(tokens[i: i + max_len][0: j + 1]) for j in range(max_len)] for i, _ in enumerate(tokens)]
    highlighted_text = []
    skip = False

    for n_grams in n_gram_tokens:
        candidate = False

        if not skip:
            for index, n_gram in enumerate(n_grams):

                if n_gram.lower() in keywords:
                    candidate = f"[black on #FFFF00]{n_gram}[/]" + n_grams[-1].split(n_gram)[-1]
                    skip = index + 1

            if not candidate:
                candidate = n_grams[0]

            highlighted_text.append(candidate)

        else:
            skip = skip - 1

    return " ".join(highlighted_text)
