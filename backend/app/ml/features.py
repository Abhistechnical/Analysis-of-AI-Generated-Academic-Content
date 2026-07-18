"""
Feature extraction module for AI vs Human text classification.

Extracts comprehensive linguistic features from text:
- Basic statistics (sentence/word counts)
- Lexical diversity and vocabulary richness
- Readability metrics
- Repetition and predictability analysis
- AI-specific markers (transition density, passive voice, hedging)
- Human-specific markers (contractions, personal pronouns, questions)
- Structural analysis (burstiness, sentence start diversity)
- Punctuation patterns
"""
import re
import math
import numpy as np
from collections import Counter


# ═══════════════════════════════════════════════════════════════
# BASIC TEXT UTILITIES
# ═══════════════════════════════════════════════════════════════

def count_sentences(text: str) -> int:
    """Count sentences using punctuation-based splitting."""
    sentences = re.split(r'[.!?]+', text.strip())
    return len([s for s in sentences if s.strip()])


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def get_sentences(text: str) -> list:
    """Split text into sentences."""
    sentences = re.split(r'[.!?]+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def compute_sentence_lengths(text: str) -> list:
    """Get word count per sentence."""
    sentences = get_sentences(text)
    return [len(s.split()) for s in sentences]


# ═══════════════════════════════════════════════════════════════
# ORIGINAL FEATURES (improved)
# ═══════════════════════════════════════════════════════════════

def lexical_diversity(text: str) -> float:
    """
    Type-Token Ratio: unique words / total words.
    Higher values indicate more diverse vocabulary.
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def vocabulary_richness(text: str) -> float:
    """
    Yule's K measure approximation.
    Returns a simplified richness score as a percentage.
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if len(words) < 2:
        return 0.0

    freq = Counter(words)
    total = len(words)
    unique = len(freq)

    # Simplified: percentage of unique words
    return round((unique / total) * 100, 2)


def readability_score(text: str) -> float:
    """
    Flesch-Kincaid Grade Level approximation.
    Higher scores = harder to read.
    """
    words = text.split()
    sentences = get_sentences(text)
    num_words = len(words)
    num_sentences = max(len(sentences), 1)

    # Count syllables (approximation)
    def count_syllables(word):
        word = word.lower().strip(".,!?;:'\"")
        if len(word) <= 3:
            return 1
        vowels = "aeiou"
        count = 0
        prev_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith("e") and count > 1:
            count -= 1
        return max(count, 1)

    total_syllables = sum(count_syllables(w) for w in words)

    if num_words == 0:
        return 0.0

    # Flesch-Kincaid Grade Level
    grade = (0.39 * (num_words / num_sentences) +
             11.8 * (total_syllables / num_words) - 15.59)
    return round(max(grade, 0), 2)


def repetition_score(text: str, n: int = 3) -> float:
    """
    Measure repetition via n-gram frequency.
    Higher score = more repetitive (more characteristic of AI text).
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if len(words) < n:
        return 0.0

    ngrams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    if not ngrams:
        return 0.0

    freq = Counter(ngrams)
    repeated = sum(1 for count in freq.values() if count > 1)
    return round(repeated / len(freq), 4)


def sentence_length_uniformity(text: str) -> float:
    """
    Measure how uniform sentence lengths are.
    Low std dev = more uniform (AI-like). Returns normalized score 0-1.
    """
    lengths = compute_sentence_lengths(text)
    if len(lengths) < 2:
        return 0.0

    mean = np.mean(lengths)
    std = np.std(lengths)

    if mean == 0:
        return 0.0

    # Coefficient of variation (inverted: lower CV = higher uniformity)
    cv = std / mean
    uniformity = max(0, 1 - cv)
    return round(uniformity, 4)


def predictability_score(text: str) -> float:
    """
    Simple predictability metric based on word frequency distribution.
    AI text tends to use more common academic words in predictable patterns.
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0

    freq = Counter(words)
    total = len(words)

    # Entropy-based: lower entropy = more predictable
    entropy = 0.0
    for count in freq.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    # Normalize to 0-1 (max entropy = log2(total unique words))
    max_entropy = math.log2(max(len(freq), 1))
    if max_entropy == 0:
        return 1.0

    normalized = 1 - (entropy / max_entropy)
    return round(normalized, 4)


# ═══════════════════════════════════════════════════════════════
# NEW FEATURES: AI-SPECIFIC MARKERS
# ═══════════════════════════════════════════════════════════════

# Common AI transition words/phrases
_AI_TRANSITIONS = {
    'furthermore', 'moreover', 'additionally', 'consequently',
    'subsequently', 'nevertheless', 'nonetheless', 'henceforth',
    'accordingly', 'correspondingly', 'similarly', 'conversely',
    'notwithstanding', 'alternatively', 'specifically',
    'significantly', 'fundamentally', 'inherently', 'intrinsically',
}

# AI hedge phrases (individual words to count)
_AI_HEDGE_WORDS = {
    'arguably', 'potentially', 'presumably', 'conceivably',
    'ostensibly', 'purportedly', 'plausibly', 'theoretically',
    'hypothetically', 'empirically', 'systematically',
    'comprehensively', 'substantively', 'demonstrably',
}

# Passive voice indicators (simplified: forms of "to be" + past participle pattern)
_PASSIVE_PATTERNS = [
    r'\b(?:is|are|was|were|been|being|be)\s+\w+(?:ed|en|t)\b',
    r'\bit\s+(?:is|was|has been)\s+(?:noted|observed|found|shown|demonstrated|established|argued|suggested|reported|recognized|acknowledged|documented|determined|concluded|hypothesized)\b',
]


def transition_word_density(text: str) -> float:
    """Count density of formulaic AI transition words."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    count = sum(1 for w in words if w in _AI_TRANSITIONS)
    return round(count / len(words), 4)


def passive_voice_ratio(text: str) -> float:
    """Estimate ratio of passive voice constructions."""
    sentences = get_sentences(text)
    if not sentences:
        return 0.0

    passive_count = 0
    for sent in sentences:
        for pattern in _PASSIVE_PATTERNS:
            if re.search(pattern, sent.lower()):
                passive_count += 1
                break  # Count each sentence at most once

    return round(passive_count / len(sentences), 4)


def hedge_word_density(text: str) -> float:
    """Count density of hedge/qualifier words typical of AI text."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    count = sum(1 for w in words if w in _AI_HEDGE_WORDS)
    return round(count / len(words), 4)


def avg_word_length(text: str) -> float:
    """Average word length. AI tends toward longer academic words."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    return round(np.mean([len(w) for w in words]), 4)


def function_word_ratio(text: str) -> float:
    """Ratio of function words (articles, prepositions, etc.)."""
    _FUNCTION_WORDS = {
        'the', 'a', 'an', 'of', 'in', 'to', 'for', 'on', 'with', 'at',
        'by', 'from', 'as', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'under', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'shall',
        'that', 'which', 'this', 'these', 'those', 'it', 'its',
    }
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    count = sum(1 for w in words if w in _FUNCTION_WORDS)
    return round(count / len(words), 4)


# ═══════════════════════════════════════════════════════════════
# NEW FEATURES: HUMAN-SPECIFIC MARKERS
# ═══════════════════════════════════════════════════════════════

def contraction_count(text: str) -> int:
    """Count contractions (e.g., don't, isn't, we're). Humans use many, AI rarely does."""
    contractions = re.findall(
        r"\b\w+(?:'(?:t|s|re|ve|ll|d|m))\b",
        text.lower()
    )
    return len(contractions)


def contraction_density(text: str) -> float:
    """Density of contractions relative to word count."""
    words = text.split()
    if not words:
        return 0.0
    return round(contraction_count(text) / len(words), 4)


def first_person_pronoun_ratio(text: str) -> float:
    """Ratio of first-person pronouns (I, we, my, our, me, us)."""
    _FIRST_PERSON = {'i', 'we', 'my', 'our', 'me', 'us', 'myself', 'ourselves', 'mine', 'ours'}
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    count = sum(1 for w in words if w in _FIRST_PERSON)
    return round(count / len(words), 4)


def question_density(text: str) -> float:
    """Density of question marks. Humans ask more rhetorical questions."""
    words = text.split()
    if not words:
        return 0.0
    questions = text.count('?')
    return round(questions / len(words), 4)


def exclamation_density(text: str) -> float:
    """Density of exclamation marks. Humans use these; AI almost never does."""
    words = text.split()
    if not words:
        return 0.0
    exclamations = text.count('!')
    return round(exclamations / len(words), 4)


def parenthetical_density(text: str) -> float:
    """Density of parenthetical expressions. Humans use asides in parentheses."""
    words = text.split()
    if not words:
        return 0.0
    parens = len(re.findall(r'\([^)]+\)', text))
    return round(parens / len(words), 4)


def informal_conjunction_density(text: str) -> float:
    """Density of sentence-starting conjunctions (But, And, So, Or). Human writing marker."""
    sentences = get_sentences(text)
    if not sentences:
        return 0.0
    _CONJUNCTIONS = {'but', 'and', 'so', 'or', 'yet', 'nor'}
    count = 0
    for sent in sentences:
        first_word = sent.strip().split()[0].lower() if sent.strip().split() else ""
        if first_word in _CONJUNCTIONS:
            count += 1
    return round(count / len(sentences), 4)


# ═══════════════════════════════════════════════════════════════
# NEW FEATURES: STRUCTURAL ANALYSIS
# ═══════════════════════════════════════════════════════════════

def sentence_start_diversity(text: str) -> float:
    """
    How many unique ways sentences start. AI tends to start sentences the same way.
    Returns ratio of unique first words / total sentences.
    """
    sentences = get_sentences(text)
    if len(sentences) < 2:
        return 1.0

    first_words = [s.strip().split()[0].lower() for s in sentences if s.strip().split()]
    if not first_words:
        return 1.0

    unique_starters = len(set(first_words))
    return round(unique_starters / len(first_words), 4)


def burstiness_score(text: str) -> float:
    """
    Measure burstiness — the tendency for sentence lengths to alternate
    between short and long. Human writing is bursty; AI is uniform.

    Calculated as the mean absolute difference between consecutive
    sentence lengths, normalized by mean sentence length.
    """
    lengths = compute_sentence_lengths(text)
    if len(lengths) < 3:
        return 0.0

    diffs = [abs(lengths[i] - lengths[i - 1]) for i in range(1, len(lengths))]
    mean_length = np.mean(lengths)
    if mean_length == 0:
        return 0.0

    return round(np.mean(diffs) / mean_length, 4)


def sentence_length_range(text: str) -> float:
    """
    Max sentence length minus min sentence length.
    Humans have wider range. Normalized by mean.
    """
    lengths = compute_sentence_lengths(text)
    if len(lengths) < 2:
        return 0.0

    mean_length = np.mean(lengths)
    if mean_length == 0:
        return 0.0

    return round((max(lengths) - min(lengths)) / mean_length, 4)


def hapax_legomena_ratio(text: str) -> float:
    """
    Ratio of words that appear only once (hapax legomena).
    Humans tend to use more unique one-off words.
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0

    freq = Counter(words)
    hapax = sum(1 for count in freq.values() if count == 1)
    return round(hapax / len(words), 4)


def comma_density(text: str) -> float:
    """Density of commas. AI uses commas more systematically."""
    words = text.split()
    if not words:
        return 0.0
    commas = text.count(',')
    return round(commas / len(words), 4)


def semicolon_colon_density(text: str) -> float:
    """Density of semicolons and colons. AI uses these more in formal writing."""
    words = text.split()
    if not words:
        return 0.0
    count = text.count(';') + text.count(':')
    return round(count / len(words), 4)


def dash_density(text: str) -> float:
    """Density of dashes (em-dash, en-dash). Humans use these for asides."""
    words = text.split()
    if not words:
        return 0.0
    dashes = text.count('—') + text.count('–') + text.count(' - ')
    return round(dashes / len(words), 4)


# ═══════════════════════════════════════════════════════════════
# FEATURE EXTRACTION (COMBINED)
# ═══════════════════════════════════════════════════════════════

def extract_features(text: str) -> dict:
    """
    Extract all linguistic features from a text sample.

    Returns a dictionary of feature names → values.
    """
    words = text.split()
    sentences = get_sentences(text)
    sent_lengths = compute_sentence_lengths(text)

    return {
        # Original features
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_sentence_length": round(np.mean(sent_lengths), 2) if sent_lengths else 0,
        "sentence_length_std": round(np.std(sent_lengths), 2) if sent_lengths else 0,
        "lexical_diversity": round(lexical_diversity(text), 4),
        "vocabulary_richness": vocabulary_richness(text),
        "readability_score": readability_score(text),
        "repetition_score": repetition_score(text),
        "sentence_uniformity": sentence_length_uniformity(text),
        "predictability_score": predictability_score(text),

        # AI-specific markers
        "transition_word_density": transition_word_density(text),
        "passive_voice_ratio": passive_voice_ratio(text),
        "hedge_word_density": hedge_word_density(text),
        "avg_word_length": avg_word_length(text),
        "function_word_ratio": function_word_ratio(text),

        # Human-specific markers
        "contraction_density": contraction_density(text),
        "first_person_ratio": first_person_pronoun_ratio(text),
        "question_density": question_density(text),
        "exclamation_density": exclamation_density(text),
        "parenthetical_density": parenthetical_density(text),
        "informal_conjunction_density": informal_conjunction_density(text),

        # Structural analysis
        "sentence_start_diversity": sentence_start_diversity(text),
        "burstiness_score": burstiness_score(text),
        "sentence_length_range": sentence_length_range(text),
        "hapax_legomena_ratio": hapax_legomena_ratio(text),
        "comma_density": comma_density(text),
        "semicolon_colon_density": semicolon_colon_density(text),
        "dash_density": dash_density(text),
    }


def extract_feature_vector(text: str) -> list:
    """
    Extract features as a numeric vector for ML model input.
    Returns list of floats in a fixed order.
    """
    feats = extract_features(text)
    return [
        # Original features (normalized)
        feats["avg_sentence_length"] / 30.0,        # normalize ~0-1
        feats["sentence_length_std"] / 15.0,         # normalize ~0-1
        feats["lexical_diversity"],                   # already 0-1
        feats["vocabulary_richness"] / 100.0,         # normalize to 0-1
        feats["readability_score"] / 20.0,            # normalize roughly
        feats["repetition_score"],                    # already ~0-1
        feats["sentence_uniformity"],                 # already 0-1
        feats["predictability_score"],                # already 0-1

        # AI-specific markers
        feats["transition_word_density"] * 20.0,      # amplify small signal
        feats["passive_voice_ratio"],                 # already 0-1
        feats["hedge_word_density"] * 20.0,           # amplify small signal
        feats["avg_word_length"] / 10.0,              # normalize ~0-1
        feats["function_word_ratio"],                 # already ~0-1

        # Human-specific markers
        feats["contraction_density"] * 10.0,          # amplify small signal
        feats["first_person_ratio"] * 10.0,           # amplify small signal
        feats["question_density"] * 20.0,             # amplify small signal
        feats["exclamation_density"] * 20.0,          # amplify small signal
        feats["parenthetical_density"] * 20.0,        # amplify small signal
        feats["informal_conjunction_density"],         # already 0-1

        # Structural analysis
        feats["sentence_start_diversity"],            # already 0-1
        feats["burstiness_score"],                    # already ~0-1
        feats["sentence_length_range"] / 5.0,         # normalize ~0-1
        feats["hapax_legomena_ratio"],                # already 0-1
        feats["comma_density"],                       # already ~0-1
        feats["semicolon_colon_density"] * 10.0,      # amplify small signal
        feats["dash_density"] * 20.0,                 # amplify small signal
    ]


# Feature names in the same order as extract_feature_vector
FEATURE_NAMES = [
    # Original features
    "Avg Sentence Length",
    "Sentence Length Variation",
    "Lexical Diversity",
    "Vocabulary Richness",
    "Readability Score",
    "Repetition Score",
    "Sentence Uniformity",
    "Predictability Score",

    # AI-specific markers
    "Transition Word Density",
    "Passive Voice Ratio",
    "Hedge Word Density",
    "Avg Word Length",
    "Function Word Ratio",

    # Human-specific markers
    "Contraction Density",
    "First Person Pronoun Ratio",
    "Question Density",
    "Exclamation Density",
    "Parenthetical Density",
    "Informal Conjunction Density",

    # Structural analysis
    "Sentence Start Diversity",
    "Burstiness Score",
    "Sentence Length Range",
    "Hapax Legomena Ratio",
    "Comma Density",
    "Semicolon/Colon Density",
    "Dash Density",
]
