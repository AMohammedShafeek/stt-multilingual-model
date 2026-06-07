# Whisper Model Benchmark Report

## Test Environment

* Language: Tamil
* Audio Length: 26.49 seconds
* Hardware:

  * NVIDIA RTX 3060 Laptop GPU (6GB VRAM)
  * 16GB RAM
  * 1TB SSD
* Framework: Faster-Whisper

---

## Model Comparison

### Tiny

Result:

* Repeated the same word continuously ("வேண்டும்")
* Failed to understand the speech content
* Severe hallucination

Assessment:

* Accuracy: 1/10
* Not usable for Tamil transcription

---

### Base

Result:

* Captured sentence structure
* Multiple recognition mistakes
* Heavy hallucination towards the end

Assessment:

* Accuracy: 4/10
* Understands speech partially
* Not reliable for production use

---

### Small

Result:

* Significant improvement
* Most sentences correctly recognized
* Some English words and Tamil words incorrectly decoded
* Minor hallucinations

Assessment:

* Accuracy: 7/10
* Good balance between speed and accuracy

---

### Medium

Result:

* Failed on this sample
* Repeated phrases continuously
* Severe hallucination

Assessment:

* Accuracy: 2/10
* Unexpected behavior
* Requires investigation

Possible Causes:

* Decoding parameters
* Faster-Whisper configuration
* Language detection issue

---

### Large-v2

Result:

* Best transcription quality
* Captured Tamil conversational style
* Correctly recognized:

  * continuity
  * consistency
  * contextual meaning
* Minimal hallucination

Assessment:

* Accuracy: 9/10
* Production-ready output

---

## Accuracy Ranking

1. Large-v2 ⭐⭐⭐⭐⭐
2. Small ⭐⭐⭐⭐
3. Base ⭐⭐
4. Medium ⭐
5. Tiny ⭐

---

## Speed vs Accuracy

| Model    | Speed    | Accuracy            |
| -------- | -------- | ------------------- |
| Tiny     | Fastest  | Very Low            |
| Base     | Fast     | Low                 |
| Small    | Moderate | Good                |
| Medium   | Slower   | Poor (Current Test) |
| Large-v2 | Slowest  | Excellent           |

---

## Recommendation

For Tamil Speech-to-Text:

### Best Accuracy

* Large-v2

### Best Cost vs Performance

* Small

### Best Learning Model

* Tiny

### Production Recommendation

* Small (real-time systems)
* Large-v2 (high accuracy systems)

---

## Key Finding

The jump from Tiny/Base to Small is substantial.

Large-v2 demonstrates significantly better contextual understanding, especially for conversational Tamil mixed with English terms such as "continuity" and "consistency".

For Tamil STT applications, Whisper Small appears to be the minimum practical model size, while Large-v2 provides the highest transcription quality among the tested models.
