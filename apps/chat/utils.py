import re

def replace_boolean_tokens(text: str, boolean: bool) -> str:
    """
    Matndagi {%boolean:Opt1;Opt2%} tokendan Opt1 yoki Opt2 ni ajratib olib,
    boolean qiymatiga qarab almashtiradi.
    """
    # Regex: \{\%boolean:    –  literal "{%boolean:"
    # ([^;]+)                –  birinchi opsiyani, ";" oldigacha bo‘lgan hamma narsani
    # ;                      –  separator
    # ([^%]+)                –  ikkinchi opsiyani, "%" oldigacha bo‘lgan hamma narsani
    # \%\}                   –  literal "%}"
    pattern = re.compile(r"\{\%boolean:([^;]+);([^%]+)\%\}")
    def _replacer(match: re.Match) -> str:
        opt1, opt2 = match.group(1).strip(), match.group(2).strip()
        return opt1 if boolean else opt2
    return pattern.sub(_replacer, text)


