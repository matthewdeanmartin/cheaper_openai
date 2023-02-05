import re

import pkg_resources
try:
    from symspellpy import SymSpell, Verbosity
    AVAIL = True
except ModuleNotFoundError:
    AVAIL = False

if AVAIL:
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)


def check_document(document: str) -> tuple[bool, str]:
    if not AVAIL:
        return True, document
    results = []
    all_right = True
    for word in document.split():
        suggestion = check_spelling(word)
        if suggestion != word:
            all_right = False
        results.append(suggestion)
    return all_right, " ".join(results)


def check_spelling(input_term: str):
    # lookup suggestions for single-word input strings
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    stripped_term = "".join(re.split("[^a-zA-Z]*", input_term)).lower()
    suggestions = sym_spell.lookup(stripped_term, Verbosity.CLOSEST, max_edit_distance=2)
    # display suggestion term, edit distance, and term frequency
    if len(suggestions) == 1:
        return input_term

    results = []
    for suggestion in suggestions[0:3]:
        results.append(suggestion.term)
    if len(suggestions) == 0:
        return f"{input_term} !!!(no suggestion)"
    else:
        return f"{input_term} !!!({','.join(results)})"


if __name__ == "__main__":
    print(check_spelling("cat"))
    print(check_spelling("crat"))
    print(check_spelling("frat"))
    print(check_spelling("blat"))
