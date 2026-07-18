"""
Synthetic dataset generator for AI vs Human academic text classification.

Generates high-quality synthetic academic text samples that capture real
stylistic differences between AI-generated and human-written content.

Key improvements over the original:
- 5x more templates per category with realistic linguistic patterns
- AI text: formulaic transitions, passive voice, hedging, uniform structure
- Human text: varied lengths, contractions, asides, imperfections, personal voice
- Paragraph-level variation and topic-specific vocabulary
- 3000 samples by default for better generalization
"""
import os
import random
import csv
import re

# ═══════════════════════════════════════════════════════════════
# ACADEMIC TOPICS (expanded)
# ═══════════════════════════════════════════════════════════════
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
    "blockchain technology in supply chain management",
    "vaccine hesitancy and public health communication",
    "urban planning and its effects on mental health",
    "the ethics of genetic engineering and CRISPR technology",
    "childhood obesity prevention programs in schools",
    "water scarcity and international conflict dynamics",
    "the role of gut microbiome in neurological disorders",
    "cryptocurrency regulation and financial stability",
    "coral reef degradation and ocean acidification",
    "the impact of automation on labor markets",
    "misinformation detection in online news platforms",
    "telemedicine adoption barriers in rural communities",
    "the relationship between sleep quality and academic performance",
    "space debris management and orbital sustainability",
    "the effectiveness of restorative justice programs",
]

# ═══════════════════════════════════════════════════════════════
# AI-GENERATED TEXT TEMPLATES
# AI text characteristics: formal, formulaic, uniform sentence
# lengths, hedging, passive voice, predictable transitions,
# repetitive structure, overly precise qualifications
# ═══════════════════════════════════════════════════════════════

AI_OPENERS = [
    "In recent years, there has been a significant increase in research focusing on",
    "This paper examines the multifaceted relationship between the various dimensions of",
    "The purpose of this study is to investigate the impact of",
    "In the context of modern academic discourse, it is essential to understand",
    "This research explores the fundamental principles underlying",
    "A comprehensive analysis of the literature reveals that",
    "The objective of this investigation is to evaluate the effectiveness of",
    "Recent advancements in the field have demonstrated that",
    "It is widely acknowledged in the academic community that",
    "The present study aims to contribute to the existing body of knowledge on",
    "The growing importance of understanding the complexities surrounding",
    "This investigation provides a systematic examination of the key factors related to",
    "In the contemporary academic landscape, the significance of",
    "The primary aim of this research is to provide a comprehensive overview of",
    "An examination of current trends reveals the increasing relevance of",
    "This study seeks to address the significant knowledge gap regarding",
    "The interdisciplinary nature of research on the topic of",
    "Recent scholarly attention has increasingly focused on the implications of",
    "It has become increasingly apparent that a thorough understanding of",
    "The central thesis of this paper revolves around the examination of",
    "In light of recent developments, it is imperative to reassess our understanding of",
    "This manuscript presents a detailed analysis of the current state of research on",
    "The academic community has long recognized the importance of studying",
    "A critical evaluation of existing research highlights the need for further investigation into",
    "The present investigation is motivated by the growing need to understand",
]

AI_TRANSITION_PHRASES = [
    "Furthermore, ",
    "Moreover, ",
    "Additionally, ",
    "Consequently, ",
    "In addition to this, ",
    "It is important to note that ",
    "Significantly, ",
    "In this regard, ",
    "As a result of these findings, ",
    "Building upon this foundation, ",
    "In a similar vein, ",
    "It should be emphasized that ",
    "From this perspective, ",
    "Taking these factors into consideration, ",
    "In light of the aforementioned evidence, ",
    "It is worth noting that ",
    "On the basis of this analysis, ",
    "With respect to this particular aspect, ",
    "Given these observations, ",
    "In accordance with established theoretical frameworks, ",
]

AI_MIDDLE_SENTENCES = [
    "the results of this analysis demonstrate a clear correlation between the variables under consideration.",
    "the findings suggest that there is a statistically significant relationship between the observed phenomena.",
    "the data indicates that the proposed methodology yields consistent and reproducible results across multiple experimental conditions.",
    "the implications of these findings extend beyond the scope of this particular study and have broader applications.",
    "the evidence presented in this section supports the hypothesis that the identified factors play a crucial role in determining outcomes.",
    "the results obtained from this investigation align with the theoretical framework established in previous literature.",
    "further research is warranted in this domain to establish more definitive conclusions about the observed patterns.",
    "the proposed approach offers significant advantages over traditional methodologies in terms of both accuracy and efficiency.",
    "these findings are consistent with previous research conducted in related areas of study and contribute to a growing body of evidence.",
    "the results underscore the importance of considering multiple perspectives when examining this particular phenomenon.",
    "the relationship between these variables is both complex and statistically significant, as demonstrated by the empirical evidence.",
    "the data collected through this systematic approach provides valuable insights into the underlying mechanisms that drive these processes.",
    "the methodology employed in this study adheres to established research protocols and best practices in the field.",
    "the theoretical implications of these findings contribute meaningfully to the ongoing scholarly discourse in this area.",
    "several key conclusions can be drawn based on the comprehensive review of available evidence and data analysis.",
    "the observed patterns suggest that the underlying mechanisms are more complex than previously theorized in the existing literature.",
    "a careful examination of the data reveals that the proposed model accurately captures the essential dynamics of the system.",
    "the statistical analysis confirms that the observed differences are significant at the conventional threshold of p < 0.05.",
    "the integration of multiple data sources strengthens the validity of the conclusions drawn from this comprehensive investigation.",
    "the existing body of literature provides a robust foundation upon which these novel findings can be contextualized and interpreted.",
    "preliminary evidence suggests that the proposed intervention may have significant implications for future research directions.",
    "the cross-sectional analysis reveals important demographic variations that warrant further investigation and scholarly attention.",
    "these results provide empirical support for the theoretical model proposed in the seminal work by leading researchers in this field.",
    "the longitudinal data demonstrates a consistent trend that supports the central hypothesis of this investigation.",
    "the operationalization of key variables in this study follows established conventions in the relevant disciplinary literature.",
    "the findings of this meta-analysis synthesize evidence from multiple studies to provide a comprehensive understanding of the phenomenon.",
    "a systematic review of the pertinent literature indicates that there is substantial consensus regarding the fundamental principles.",
    "the empirical evidence accumulated over the past decade provides compelling support for the theoretical framework underpinning this analysis.",
    "the observed effect sizes are consistent with those reported in comparable studies, thereby reinforcing the reliability of these findings.",
    "the methodological rigor of this investigation ensures that the conclusions drawn are both valid and generalizable to broader contexts.",
]

AI_CLOSERS = [
    "In conclusion, this study provides compelling evidence that supports the proposed theoretical framework and contributes to advancing our understanding of this important topic.",
    "To summarize, the findings of this research make a significant contribution to the existing literature and highlight several avenues for future scholarly investigation.",
    "In summary, the results of this investigation highlight the need for continued research in this area and underscore the complexity of the phenomena under examination.",
    "Overall, the evidence presented in this paper supports the conclusion that further inquiry is necessary to fully elucidate the mechanisms at play.",
    "The implications of this research extend to both theoretical and practical applications in the field, offering valuable guidance for future studies and policy decisions.",
    "This study demonstrates that the proposed framework provides a comprehensive and nuanced understanding of the factors that influence outcomes in this domain.",
    "The present findings underscore the necessity of adopting multidisciplinary approaches when investigating complex phenomena of this nature.",
    "In light of these results, it is recommended that future research employ longitudinal designs to capture the dynamic nature of the relationships identified.",
    "The comprehensive analysis presented herein offers a foundation upon which subsequent research can build to further advance our collective understanding.",
    "Taken together, these findings represent a meaningful advancement in our understanding of the subject matter and provide a clear direction for future investigations.",
]

# ═══════════════════════════════════════════════════════════════
# HUMAN-WRITTEN TEXT TEMPLATES
# Human text characteristics: varied sentence lengths, personal
# voice, contractions, hedging with informality, digressions,
# rhetorical questions, emotional markers, imperfections
# ═══════════════════════════════════════════════════════════════

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
    "I'll admit that when I first approached the question of",
    "Let me start by saying that",
    "Honestly, the more I dig into the research on",
    "Here's the thing about",
    "What got me interested in this particular area was",
    "You'd think we'd have a better handle on",
    "I've been thinking about this for a while, and",
    "This isn't the easiest topic to write about, but",
    "If you ask most experts about",
    "It's hard to overstate just how complicated the issue of",
    "The story of how we came to understand",
    "People don't usually think about it this way, but",
    "I want to challenge a common assumption about",
    "So here's what we know — and don't know — about",
    "When my advisor first suggested I look into",
]

HUMAN_MIDDLE_SENTENCES = [
    "But here's where it gets interesting.",
    "The data wasn't exactly what I expected — there were some surprising outliers that really changed the picture.",
    "I should note that this approach has its limitations, and I'll get to those later.",
    "What really stood out was how differently the two groups responded to the intervention.",
    "Interestingly, some participants didn't follow the expected pattern at all.",
    "This is a tricky area because there are so many confounding variables to deal with.",
    "The stats tell one story, but when you look at individual cases, the picture is much more nuanced than the numbers suggest.",
    "I think we need to be careful about drawing too broad of conclusions from this data.",
    "One participant's response was particularly telling — and I keep coming back to it.",
    "Looking at the numbers alone doesn't quite capture what's happening here.",
    "There are, of course, some caveats to keep in mind.",
    "Admittedly, the sample size could've been larger, but funding constraints limited what we could do.",
    "What makes this finding significant is that it contradicts much of the previous work in this area.",
    "I was skeptical at first, but the evidence is hard to ignore.",
    "The methodology we used was adapted from earlier work by Thompson et al., though we made some key modifications along the way.",
    "It's worth mentioning that not everyone agrees with this interpretation — and they might have a point.",
    "These results raise more questions than they answer, frankly.",
    "We ran the experiment three times just to make sure the results were reliable.",
    "The real-world implications of this are pretty significant, if the findings hold up under further scrutiny.",
    "Some reviewers might argue our controls weren't strict enough, but I'd push back on that.",
    "Here's something I didn't expect to find.",
    "Why does this matter? Well, think about it this way.",
    "I'm still not 100% sure what to make of the outliers in our dataset.",
    "And no, it's not just a statistical artifact — we checked.",
    "The short version? Things are more complicated than the textbook says.",
    "So we went back and ran the analysis again with different parameters — same result.",
    "What surprised me most was how robust this effect was across different subgroups.",
    "Now, I know what you're thinking — couldn't this be explained by selection bias? Maybe, but probably not.",
    "Let's be honest: a lot of the older research on this topic is outdated, or worse, poorly designed.",
    "To be fair, there are legitimate counterarguments, and I don't want to pretend otherwise.",
    "My gut tells me there's something deeper going on here, though the data can only take us so far.",
    "Is this a perfect study? No. Did we learn something useful? Absolutely.",
    "I talked to a few colleagues about these results, and the consensus was: 'huh, that's weird.'",
    "One limitation I want to be upfront about: we didn't control for socioeconomic status.",
    "The effect size was small but consistent, which is honestly more interesting than a flashy but unreliable result.",
    "It took us about six months to collect all the data. Worth it? I think so.",
    "Part of the problem is that existing measurement tools aren't great for capturing what we're looking at.",
    "I keep going back and forth on whether this supports or undermines the prevailing theory.",
    "OK so this next part is a bit technical, but bear with me.",
    "The correlation was there, but as every intro stats student knows, correlation doesn't equal causation.",
    "We tried a bunch of different models before settling on this one. None of them were perfect.",
    "If I had to bet, I'd say the effect is real — but I wouldn't bet the house on it.",
    "What's frustrating is that the data is ambiguous on this exact point.",
    "I realize I'm speculating a bit here, but I think the evidence warrants it.",
    "For what it's worth, two independent labs have found similar patterns.",
]

HUMAN_CLOSERS = [
    "So where does this leave us? There's clearly more work to be done, but I think we're on the right track.",
    "In the end, this research raises as many questions as it answers — which is exactly what good science should do.",
    "To wrap up, I believe these findings have real potential to change how we think about this issue.",
    "Looking ahead, I'm hopeful that future studies will build on what we've found here.",
    "The bottom line is that this is a complex issue, and simplistic answers won't cut it.",
    "All things considered, I'd say the evidence points in a clear direction, even if some details remain fuzzy.",
    "I don't want to overstate our conclusions, but I do think this matters — a lot, actually.",
    "Is this the final word on the topic? Definitely not. But it's a solid step forward.",
    "My hope is that other researchers will take this and run with it. The field needs it.",
    "At the end of the day, we've barely scratched the surface. But that's kind of exciting, isn't it?",
    "If nothing else, this study shows we need to rethink some of our basic assumptions.",
    "What I take away from all of this is that the world is messier than our models suggest — and that's OK.",
    "I'll leave the final judgment to the reader, but I think the direction is clear.",
    "So yeah, more research needed. But this time, we actually have a pretty good starting point.",
    "The question isn't whether this matters — it clearly does. The question is what we do about it.",
]

# ═══════════════════════════════════════════════════════════════
# FILLER / VARIATION ELEMENTS
# ═══════════════════════════════════════════════════════════════

AI_HEDGES = [
    "It is widely accepted that ",
    "It can be argued that ",
    "Evidence suggests that ",
    "Research has consistently shown that ",
    "It has been well established that ",
    "Scholars have long recognized that ",
    "The prevailing consensus indicates that ",
    "According to established frameworks, ",
    "Empirical data consistently demonstrates that ",
    "As documented in the literature, ",
]

HUMAN_INTERJECTIONS = [
    "Right?",
    "Let me explain.",
    "Stay with me here.",
    "Hear me out.",
    "Seriously.",
    "Think about that for a second.",
    "Wild, right?",
    "I know, I know.",
    "Bear with me.",
    "Go figure.",
    "Which is... unexpected.",
    "Yeah, I was surprised too.",
    "Fair enough.",
    "Pretty interesting, huh?",
    "No kidding.",
]

HUMAN_PARENTHETICALS = [
    " (though honestly, I'm not entirely sure why)",
    " (more on that later)",
    " (which, by the way, was not easy to measure)",
    " (or at least, that's what the data suggests)",
    " (and believe me, we tried everything else first)",
    " (I know, it sounds counterintuitive)",
    " (yeah, that one took me by surprise too)",
    " (and this is the part that gets really interesting)",
    " (in retrospect, this should have been obvious)",
    " (but don't quote me on that just yet)",
]


# ═══════════════════════════════════════════════════════════════
# TEXT GENERATORS
# ═══════════════════════════════════════════════════════════════

def generate_ai_text() -> str:
    """
    Generate a synthetic AI-style academic text sample.

    Characteristics:
    - Uniform sentence lengths (typically 15-30 words)
    - Formulaic transition phrases between sentences
    - Passive voice, hedging, precise qualifications
    - Predictable intro-body-conclusion structure
    - No contractions, no personal pronouns, no colloquialisms
    """
    topic = random.choice(ACADEMIC_TOPICS)
    opener = random.choice(AI_OPENERS) + " " + topic + "."

    # AI text: 6-10 middle sentences, each with a transition phrase
    num_sentences = random.randint(6, 10)
    selected_middles = random.sample(AI_MIDDLE_SENTENCES, min(num_sentences, len(AI_MIDDLE_SENTENCES)))

    # Always prefix with transitions (very AI-like behavior)
    transitions = random.sample(AI_TRANSITION_PHRASES, min(num_sentences, len(AI_TRANSITION_PHRASES)))
    body_sentences = []
    for i, middle in enumerate(selected_middles):
        if i < len(transitions):
            body_sentences.append(transitions[i] + middle)
        else:
            body_sentences.append(random.choice(AI_HEDGES) + middle)

    # Occasionally add an AI hedge sentence
    if random.random() > 0.5:
        hedge = random.choice(AI_HEDGES) + random.choice(AI_MIDDLE_SENTENCES)
        body_sentences.insert(random.randint(1, len(body_sentences)), hedge)

    closer = random.choice(AI_CLOSERS)

    # AI tends to structure in paragraphs of ~3-4 sentences
    paragraphs = [opener]
    chunk_size = random.choice([3, 4])
    for i in range(0, len(body_sentences), chunk_size):
        chunk = body_sentences[i:i + chunk_size]
        paragraphs.append(" ".join(chunk))
    paragraphs.append(closer)

    return " ".join(paragraphs)


def generate_human_text() -> str:
    """
    Generate a synthetic human-style academic text sample.

    Characteristics:
    - Highly varied sentence lengths (3 to 40+ words)
    - Personal voice ("I", "we", "my")
    - Contractions ("don't", "can't", "it's", "won't")
    - Informal asides, rhetorical questions, interjections
    - Parenthetical remarks
    - Occasional imperfections and colloquialisms
    - No formulaic transitions
    """
    topic = random.choice(ACADEMIC_TOPICS)
    opener_template = random.choice(HUMAN_OPENERS)

    # Human openers are more varied in how they integrate the topic
    if opener_template.endswith(":"):
        opener = opener_template + " what exactly is going on with " + topic + "?"
    elif "whether" in opener_template:
        opener = opener_template + " " + topic + " really matters as much as everyone says."
    elif "but" in opener_template.lower():
        opener = opener_template + " " + topic + " is far more complicated than most people think."
    else:
        opener = opener_template + " " + topic + " is way more complex than it first appears."

    # Human text: highly varied sentence count (4-12)
    num_sentences = random.randint(4, 12)
    selected_middles = random.sample(
        HUMAN_MIDDLE_SENTENCES,
        min(num_sentences, len(HUMAN_MIDDLE_SENTENCES))
    )

    body_sentences = list(selected_middles)

    # Add 1-3 interjections (short punchy sentences)
    num_interjections = random.randint(1, 3)
    for _ in range(num_interjections):
        interjection = random.choice(HUMAN_INTERJECTIONS)
        pos = random.randint(0, len(body_sentences))
        body_sentences.insert(pos, interjection)

    # Add 0-2 parenthetical remarks to existing sentences
    num_parentheticals = random.randint(0, 2)
    for _ in range(num_parentheticals):
        if body_sentences:
            idx = random.randint(0, len(body_sentences) - 1)
            sent = body_sentences[idx]
            # Only add parenthetical to sentences that end with a period
            if sent.endswith("."):
                parenthetical = random.choice(HUMAN_PARENTHETICALS)
                body_sentences[idx] = sent[:-1] + parenthetical + "."

    closer = random.choice(HUMAN_CLOSERS)

    # Humans don't always structure in clean paragraphs
    # Sometimes it's just a flow of sentences
    if random.random() > 0.6:
        # Stream of consciousness style
        return " ".join([opener] + body_sentences + [closer])
    else:
        # Loose paragraph structure with varied sizes
        paragraphs = [opener]
        i = 0
        while i < len(body_sentences):
            chunk_size = random.randint(2, 5)
            chunk = body_sentences[i:i + chunk_size]
            paragraphs.append(" ".join(chunk))
            i += chunk_size
        paragraphs.append(closer)
        return " ".join(paragraphs)


def generate_dataset(output_path: str, num_samples: int = 3000) -> str:
    """
    Generate a balanced synthetic dataset and save as CSV.

    Args:
        output_path: Path to save the CSV file.
        num_samples: Total number of samples (split evenly between classes).

    Returns:
        Path to the generated CSV file.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

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
