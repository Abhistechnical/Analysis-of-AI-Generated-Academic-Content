"""
Synthetic dataset generator for AI vs Human academic text classification.

Generates template-based academic text samples that capture stylistic
differences between AI-generated and human-written content.
"""
import os
import random
import csv

# ─── Text Templates ─────────────────────────────────────────

# AI-generated text tends to be: uniform sentence length, formal,
# repetitive transitions, predictable structure, low diversity
AI_OPENERS = [
    "In recent years, there has been a significant increase in research focusing on",
    "This paper examines the multifaceted relationship between",
    "The purpose of this study is to investigate the impact of",
    "In the context of modern academic discourse, it is essential to understand",
    "This research explores the fundamental principles underlying",
    "A comprehensive analysis of the literature reveals that",
    "The objective of this investigation is to evaluate the effectiveness of",
    "Recent advancements in the field have demonstrated that",
    "It is widely acknowledged in the academic community that",
    "The present study aims to contribute to the existing body of knowledge on",
]

AI_MIDDLE_SENTENCES = [
    "Furthermore, the results of this analysis demonstrate a clear correlation between the variables under consideration.",
    "Moreover, the findings suggest that there is a statistically significant relationship between the observed phenomena.",
    "Additionally, the data indicates that the proposed methodology yields consistent and reproducible results.",
    "It is important to note that the implications of these findings extend beyond the scope of this particular study.",
    "The evidence presented in this section supports the hypothesis that the identified factors play a crucial role.",
    "Consequently, the results obtained from this investigation align with the theoretical framework established previously.",
    "In light of these observations, it becomes apparent that further research is warranted in this domain.",
    "The analysis reveals that the proposed approach offers significant advantages over traditional methodologies.",
    "These findings are consistent with previous research conducted in related areas of study.",
    "The results underscore the importance of considering multiple perspectives when examining this phenomenon.",
    "As demonstrated by the empirical evidence, the relationship between these variables is both complex and significant.",
    "The data collected through this systematic approach provides valuable insights into the underlying mechanisms.",
    "It should be emphasized that the methodology employed in this study adheres to established research protocols.",
    "The theoretical implications of these findings contribute meaningfully to the ongoing scholarly discourse.",
    "Based on the comprehensive review of available evidence, several key conclusions can be drawn.",
]

AI_CLOSERS = [
    "In conclusion, this study provides compelling evidence that supports the proposed theoretical framework.",
    "To summarize, the findings of this research make a significant contribution to the existing literature.",
    "In summary, the results of this investigation highlight the need for continued research in this area.",
    "Overall, the evidence presented in this paper supports the conclusion that further inquiry is necessary.",
    "The implications of this research extend to both theoretical and practical applications in the field.",
]

# Human-written text: varied lengths, personal voice, occasional informal
# phrasing, contractions, hedging, varied vocabulary, some imperfections
HUMAN_OPENERS = [
    "When I first started looking into this topic, I was surprised to find that",
    "There's been a lot of debate recently about whether",
    "This paper tries to shed some light on the complex issue of",
    "It might seem obvious, but the relationship between",
    "One thing that's often overlooked in discussions about",
    "My research started with a simple question:",
    "The idea for this study came from observing that",
    "While reviewing existing literature, I noticed a gap in our understanding of",
    "Most people would agree that the subject of",
    "After spending several months analyzing data on this topic, I found that",
]

HUMAN_MIDDLE_SENTENCES = [
    "But here's where it gets interesting.",
    "The data wasn't exactly what I expected – there were some surprising outliers that changed the picture considerably.",
    "I should note that this approach has its limitations, and I'll discuss those later.",
    "What really stood out was how differently the two groups responded to the intervention.",
    "Interestingly, some participants didn't follow the expected pattern at all.",
    "This is a tricky area because there are so many confounding variables to account for.",
    "The stats tell one story, but when you look at individual cases, the picture is more nuanced.",
    "I think we need to be careful about drawing too broad of conclusions from this data.",
    "One participant's response was particularly telling.",
    "Looking at the numbers alone doesn't quite capture what's happening here.",
    "There are, of course, some caveats to keep in mind.",
    "Admittedly, the sample size could've been larger.",
    "What makes this finding significant is that it contradicts much of the previous work in this area.",
    "I was skeptical at first, but the evidence is hard to ignore.",
    "The methodology we used was adapted from earlier work by Thompson et al., though we made some modifications.",
    "It's worth mentioning that not everyone agrees with this interpretation.",
    "These results raise more questions than they answer, frankly.",
    "We ran the experiment three times to make sure the results were reliable.",
    "The real-world implications of this are pretty significant, if the findings hold up.",
    "Some reviewers might argue that our controls weren't strict enough, but I'd push back on that.",
]

HUMAN_CLOSERS = [
    "So where does this leave us? There's clearly more work to be done, but I think we're on the right track.",
    "In the end, this research raises as many questions as it answers – which is exactly what good science should do.",
    "To wrap up, I believe these findings have real potential to change how we think about this issue.",
    "Looking ahead, I'm hopeful that future studies will build on what we've found here.",
    "The bottom line is that this is a complex issue, and simplistic answers won't cut it.",
    "All things considered, I'd say the evidence points in a clear direction, even if some details remain fuzzy.",
]

ACADEMIC_TOPICS = [
    "climate change and its socioeconomic impacts",
    "machine learning applications in healthcare diagnostics",
    "the role of social media in political polarization",
    "renewable energy adoption in developing nations",
    "the effectiveness of remote learning in higher education",
    "artificial intelligence ethics and governance frameworks",
    "biodiversity conservation in urban environments",
    "the impact of microplastics on marine ecosystems",
    "cognitive behavioral therapy for anxiety disorders",
    "quantum computing and cryptographic security",
    "sustainable agriculture practices and food security",
    "the digital divide and educational inequality",
    "neuroscience of decision-making under uncertainty",
    "antibiotic resistance and public health strategies",
    "the economics of universal basic income programs",
    "gender representation in STEM academic publishing",
    "autonomous vehicle safety and regulatory challenges",
    "the psychological effects of chronic social media use",
    "deep learning architectures for natural language processing",
    "the intersection of cultural identity and globalization",
]


def generate_ai_text() -> str:
    """Generate a synthetic AI-style academic text sample."""
    topic = random.choice(ACADEMIC_TOPICS)
    opener = random.choice(AI_OPENERS) + " " + topic + "."

    # AI text: consistently 5-8 middle sentences, uniform length
    num_sentences = random.randint(5, 8)
    middles = random.sample(AI_MIDDLE_SENTENCES, min(num_sentences, len(AI_MIDDLE_SENTENCES)))

    closer = random.choice(AI_CLOSERS)

    return " ".join([opener] + middles + [closer])


def generate_human_text() -> str:
    """Generate a synthetic human-style academic text sample."""
    topic = random.choice(ACADEMIC_TOPICS)
    opener = random.choice(HUMAN_OPENERS) + " " + topic + " is far more complex than it appears."

    # Human text: varied sentence count (3-10), mix of long and short
    num_sentences = random.randint(3, 10)
    middles = random.sample(HUMAN_MIDDLE_SENTENCES, min(num_sentences, len(HUMAN_MIDDLE_SENTENCES)))

    # Occasionally add short interjections
    if random.random() > 0.5:
        middles.insert(random.randint(0, len(middles)), "Right?")
    if random.random() > 0.6:
        middles.insert(random.randint(0, len(middles)), "Let me explain.")

    closer = random.choice(HUMAN_CLOSERS)

    return " ".join([opener] + middles + [closer])


def generate_dataset(output_path: str, num_samples: int = 1000) -> str:
    """
    Generate a balanced synthetic dataset and save as CSV.

    Args:
        output_path: Path to save the CSV file.
        num_samples: Total number of samples (split evenly between classes).

    Returns:
        Path to the generated CSV file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    samples = []
    half = num_samples // 2

    # Generate AI samples (label=1)
    for _ in range(half):
        samples.append({"text": generate_ai_text(), "label": 1})

    # Generate Human samples (label=0)
    for _ in range(half):
        samples.append({"text": generate_human_text(), "label": 0})

    # Shuffle
    random.seed(42)
    random.shuffle(samples)

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(samples)

    print(f"Dataset generated: {len(samples)} samples -> {output_path}")
    return output_path


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    generate_dataset(os.path.join(base, "data", "dataset.csv"))
