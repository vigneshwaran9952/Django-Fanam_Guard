import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


CACHE_FILE = {
    "rag": "Cache/rag_cache.json",
    "enhance": "Cache/enhance_cache.json",
    "deep": "Cache/deep_cache.json",
    "global_expansion": "Cache/global_expansion_cache.json",
    "shariat": "Cache/shariat.json"
}


# ======================================================
# ✅ GET CACHE
# ======================================================
def get_cached_response(question, country, sector, mode, language=None):

    cache_file = CACHE_FILE.get(mode)
    if not cache_file or not os.path.exists(cache_file):
        return None

    with open(cache_file, "r", encoding="utf-8") as f:
        cache = json.load(f)

    # -----------------------------
    # GLOBAL MODES
    # -----------------------------
    if mode in ["global_expansion", "shariat"]:
        relevant_cache = cache

    # -----------------------------
    # 🇦🇪 UAE SPECIAL LOGIC
    # -----------------------------
    elif country == "UAE":
        relevant_cache = [
            item for item in cache
            if item.get("mode") == mode
            and item.get("language") == language
        ]

    # -----------------------------
    # NORMAL COUNTRIES
    # -----------------------------
    else:
        relevant_cache = [
            item for item in cache
            if item.get("country") == country
            and item.get("sector") == sector
            and item.get("mode") == mode
        ]

    if not relevant_cache:
        return None

    # -----------------------------
    # Similarity Matching
    # -----------------------------
    questions = [item["question"] for item in relevant_cache]

    vectorizer = TfidfVectorizer().fit_transform([question] + questions)
    vectors = vectorizer.toarray()

    cosine_sim = cosine_similarity([vectors[0]], vectors[1:])[0]
    max_idx = cosine_sim.argmax()

    # ⭐ Slightly stricter for UAE
    threshold = 0.95 if country == "UAE" else 0.90

    if cosine_sim[max_idx] > threshold:
        return relevant_cache[max_idx]

    return None


# ======================================================
# ✅ SAVE CACHE
# ======================================================
def save_to_cache(
    question,
    answer,
    country,
    sector,
    mode,
    suggestions=None,
    sources=None,
    audio_path=None,
    language=None
):

    cache_file = CACHE_FILE.get(mode)
    if not cache_file:
        return

    cache = []
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)

    # 🇦🇪 UAE → Don't store sector
    if country == "UAE":
        sector = None

    cache.append({
        "question": question,
        "answer": answer,
        "country": country,
        "sector": sector,
        "mode": mode,
        "language": language,
        "suggestions": suggestions or [],
        "sources": sources or [],
        "audio_path": audio_path
    })

    # Limit size
    if len(cache) > 500:
        cache.pop(0)

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)
