"""
Feature extraction module for text classification.

Extracts linguistic features from text for AI vs Human detection:
- TF-IDF vectorization
- Sentence statistics
- Lexical diversity
- Readability metrics
- Repetition analysis
"""
import re
import math
import numpy as np
from collections import Counter


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


def extract_features(text: str) -> dict:
    """
    Extract all linguistic features from a text sample.

    Returns a dictionary of feature names → values.
    """
    words = text.split()
    sentences = get_sentences(text)
    sent_lengths = compute_sentence_lengths(text)

    return {
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
    }


def extract_feature_vector(text: str) -> list:
    """
    Extract features as a numeric vector for ML model input.
    Returns list of floats in a fixed order.
    """
    feats = extract_features(text)
    return [
        feats["avg_sentence_length"],
        feats["sentence_length_std"],
        feats["lexical_diversity"],
        feats["vocabulary_richness"] / 100.0,  # normalize to 0-1
        feats["readability_score"] / 20.0,      # normalize roughly
        feats["repetition_score"],
        feats["sentence_uniformity"],
        feats["predictability_score"],
    ]


# Feature names in the same order as extract_feature_vector
FEATURE_NAMES = [
    "Avg Sentence Length",
    "Sentence Length Variation",
    "Lexical Diversity",
    "Vocabulary Richness",
    "Readability Score",
    "Repetition Score",
    "Sentence Uniformity",
    "Predictability Score",
]
