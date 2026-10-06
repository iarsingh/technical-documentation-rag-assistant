import re

STOP = {"the", "a", "an", "is", "of", "and", "to", "in", "what", "why", "does", "how"}
PASSAGES = [("probes.md", 'Readiness probes gate traffic. Liveness probes restart a stuck process.'), ("other.md", 'Office wifi is in the lobby closet.')]
MIN_OVERLAP = 2


class InputError(ValueError):
    pass


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP


def answer(question, source=None):
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise InputError("question must contain 1 to 2000 characters")
    if source is not None and (not isinstance(source, str) or len(source) > 200):
        raise InputError("source must be a filename of at most 200 characters")
    corpus = PASSAGES
    if source is not None:
        corpus = [item for item in corpus if item[0] == source]
        if not corpus:
            raise InputError(f"unknown source: {source}")
    query = words(question)
    ranked = []
    for name, text in corpus:
        overlap = query & words(text)
        ranked.append({"source": name, "text": text, "overlap": len(overlap), "matched_terms": sorted(overlap), "query_coverage": len(overlap) / max(1, len(query))})
    ranked.sort(key=lambda row: (-row["overlap"], row["source"]))
    best = ranked[0]
    if best["overlap"] < MIN_OVERLAP:
        return {"answered": False, "answer": "No passage shares enough terms.", "citation": None, "passages": ranked}
    return {"answered": True, "answer": best["text"], "citation": best["source"], "passages": ranked}
