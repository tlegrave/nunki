import re
import unicodedata


def normalize_unicode_text(text):
    """
    Takes a unicode text and normalize it with unicode names.
    We could be doing a lot more here like spell checking, substitution of contractions, URLs cleaning...
    """
    text = _remove_urls_in_text(text)
    return "".join(
        f"[{unicodedata.name(c)}]"
        if (cat := unicodedata.category(c)) == "So"
        else ("" if cat == "Mn" else c)
        for c in unicodedata.normalize("NFKC", text)
    )


def _remove_urls_in_text(text):
    """
    Removes URLs in the given text
    """
    url_regex = r"(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
    text = re.sub(url_regex, "", text)
    return text
