# Feature Engineering Pipeline Design

## 1. Project Context

This project focuses on building a first prototype of a feature engineering pipeline for app review text data.

The goal is not to build a large or highly sophisticated NLP system. Since the remaining internship time is limited, the scope is intentionally focused on a practical and lightweight prototype.

The pipeline should take raw review text and convert it into a more structured, model-ready representation that can support downstream analysis or machine learning tasks.

---

## 2. Project Goal

The goal of this prototype is to transform raw app review data into structured text-based features.

### Input

Raw review data, such as:

- review ID
- review text
- rating score
- review date

### Output

A structured feature table containing engineered features such as:

- basic text statistics
- sentiment or polarity
- subjectivity
- aspect labels
- complaint indicators
- optional semantic grouping features

The final output should be usable for downstream tasks such as:

- product issue analysis
- complaint detection
- review classification
- trend analysis
- model training
- dashboard reporting

---

## 3. Updated Scope Based on Feedback

Based on the latest feedback, the expected outcome is a clear and meaningful first prototype rather than a complete NLP system.

The prototype should demonstrate three things:

1. Clear research and rationale  
   - Identify which features are useful.
   - Explain why these features matter for downstream analysis or modeling.

2. Structured planning and design  
   - Show how the pipeline is organized.
   - Explain how raw review text becomes structured features.

3. Lightweight implementation  
   - Build a working pipeline that can process real review data.
   - Generate structured output.
   - Provide examples or light validation to show the features are meaningful.

This project should prioritize a smaller number of features implemented clearly and well instead of a broad but incomplete pipeline.

---

## 4. Success Criteria

The prototype will be considered successful if it can do the following:

1. Load real review data from an existing source such as JSON, CSV, or SQLite.
2. Clean and normalize raw review text.
3. Extract a reasonable set of structured features.
4. Explain why each selected feature is useful.
5. Save the engineered features into a structured output file or database table.
6. Provide examples showing that the extracted features make sense.
7. Clearly describe the current limitations and possible future improvements.

---

## 5. Selected Features

For the first version, the pipeline will focus on a small set of practical features.

### 5.1 Basic Text Features

These features describe the structure and length of the review text.

| Feature | Description | Why It Is Useful |
|---|---|---|
| `char_count` | Number of characters in the review | Helps measure review length and detail level |
| `word_count` | Number of words in the review | Useful for filtering short or low-information reviews |
| `sentence_count` | Number of sentences | Helps identify more complex reviews |
| `avg_word_length` | Average word length | May indicate writing complexity |
| `has_question` | Whether the review contains a question mark | Useful for identifying support-related or help-seeking reviews |
| `has_exclamation` | Whether the review contains an exclamation mark | May indicate strong emotional expression |
| `is_short_review` | Whether the review is below a minimum word threshold | Helps flag reviews that may contain limited information |

These features are simple, interpretable, and useful as a baseline for downstream modeling.

---

### 5.2 Sentiment and Polarity Features

Sentiment features estimate whether the review expresses a positive, negative, or neutral opinion.

| Feature | Description | Why It Is Useful |
|---|---|---|
| `polarity_score` | Numeric sentiment score | Measures overall positive or negative tone |
| `sentiment_label` | Positive, neutral, or negative label | Makes review tone easier to analyze |
| `subjectivity_score` | Estimate of how opinion-based the review is | Helps distinguish factual complaints from subjective opinions |

These features are useful because app reviews often contain emotional feedback. Sentiment can help identify user dissatisfaction, compare rating scores with review text, and prioritize negative reviews for further analysis.

---

### 5.3 Aspect Extraction Features

Aspect extraction identifies what topic or product area the review is discussing.

For the prototype, aspect extraction will use a keyword-based approach.

Example aspect categories:

| Aspect | Example Keywords |
|---|---|
| `login_account` | login, sign in, account, password |
| `performance` | slow, lag, freeze, crash, loading |
| `ui_design` | UI, interface, layout, design, button |
| `subscription_billing` | payment, billing, subscription, plus, charge |
| `voice_audio` | voice, audio, speech, microphone |
| `notification` | notification, alert, reminder |
| `update_version` | update, version, new release |
| `response_quality` | answer, response, accuracy, wrong, useful |

The output may include:

- `detected_aspects`
- `aspect_count`
- `has_performance_issue`
- `has_login_issue`
- `has_billing_issue`

This feature group is important because sentiment alone does not explain what the user is talking about. Aspect extraction helps connect user opinions to specific product areas.

---

### 5.4 Complaint Indicator Features

The pipeline can also generate simple complaint-related indicators.

| Feature | Description | Why It Is Useful |
|---|---|---|
| `is_complaint` | Whether the review likely contains a complaint | Useful for issue detection |
| `complaint_keywords_found` | Keywords that indicate complaints | Helps explain why a review was flagged |
| `negative_with_high_rating` | Negative text but high star rating | Helps identify rating-text mismatch |
| `positive_with_low_rating` | Positive text but low star rating | Helps detect unusual or inconsistent reviews |

These features can support quality checks and downstream classification tasks.

---

### 5.5 Optional Semantic Grouping

If time allows, the prototype may include a lightweight semantic grouping step.

Possible approach:

1. Convert review text into embeddings.
2. Cluster similar reviews.
3. Assign each review a `semantic_cluster` label.
4. Inspect sample reviews from each cluster.

Example groups may include:

| Cluster | Possible Meaning |
|---|---|
| Cluster 0 | Login or account issues |
| Cluster 1 | Crashes, freezing, or slow performance |
| Cluster 2 | Billing or subscription problems |
| Cluster 3 | Positive feedback about useful features |

This part should be treated as optional. The main prototype should still work without it.

---

## 6. Pipeline Design

The pipeline will follow this structure:

```text
Raw Review Data
        ↓
Load Reviews
        ↓
Clean and Normalize Text
        ↓
Extract Basic Text Features
        ↓
Extract Sentiment Features
        ↓
Extract Aspect Features
        ↓
Generate Complaint Indicators
        ↓
Optional Semantic Grouping
        ↓
Save Structured Feature Table
        ↓
Validate Sample Outputs
````

---

## 7. Pipeline Components

### 7.1 Load Reviews

The pipeline should load review data from an existing source.

Possible input sources:

* JSON file
* CSV file
* SQLite database

Expected fields:

```text
review_id
content
score
date
```

---

### 7.2 Clean Text

Text cleaning should include:

* converting text to lowercase
* removing extra spaces
* handling missing values
* removing invalid or empty reviews
* optionally removing very short reviews
* preserving original text for reference

The cleaned text should be stored separately from the original review text.

Example fields:

```text
content_original
content_cleaned
```

---

### 7.3 Extract Basic Features

The pipeline should calculate basic text statistics.

Example output:

```text
char_count
word_count
sentence_count
avg_word_length
has_question
has_exclamation
is_short_review
```

---

### 7.4 Extract Sentiment Features

The pipeline should generate sentiment-related features.

Example output:

```text
polarity_score
subjectivity_score
sentiment_label
```

A lightweight library such as TextBlob or VADER can be used for the first prototype.

---

### 7.5 Extract Aspect Features

The pipeline should use a dictionary-based method to detect aspects.

Example aspect dictionary:

```python
ASPECT_KEYWORDS = {
    "login_account": ["login", "sign in", "account", "password"],
    "performance": ["slow", "lag", "freeze", "crash", "loading"],
    "ui_design": ["ui", "interface", "layout", "design", "button"],
    "subscription_billing": ["payment", "billing", "subscription", "plus", "charge"],
    "voice_audio": ["voice", "audio", "speech", "microphone"],
    "notification": ["notification", "alert", "reminder"],
    "update_version": ["update", "version", "release"],
    "response_quality": ["answer", "response", "accuracy", "wrong", "useful"]
}
```

The output should include which aspects were detected for each review.

Example output:

```text
detected_aspects = ["performance", "update_version"]
aspect_count = 2
has_performance_issue = True
```

---

### 7.6 Generate Complaint Indicators

The pipeline should use sentiment and keywords to flag likely complaints.

Example logic:

```text
A review may be marked as a complaint if:
- sentiment is negative, or
- complaint-related keywords are present, or
- the review mentions product problems such as crashing, login failure, or billing issues.
```

Example output:

```text
is_complaint
complaint_keywords_found
```

---

### 7.7 Save Output

The pipeline should save the engineered features into a structured table.

Possible formats:

* CSV file
* SQLite table

Recommended first output:

```text
data/processed/engineered_reviews.csv
```

Optional database output:

```text
engineered_reviews table in SQLite
```

---

## 8. Expected Output Schema

The final feature table may include the following columns:

```text
review_id
content_original
content_cleaned
score
date

char_count
word_count
sentence_count
avg_word_length
has_question
has_exclamation
is_short_review

polarity_score
subjectivity_score
sentiment_label

detected_aspects
aspect_count
has_login_issue
has_performance_issue
has_billing_issue
has_ui_issue
has_voice_issue

is_complaint
complaint_keywords_found

semantic_cluster
```

The `semantic_cluster` column is optional and should only be included if semantic grouping is implemented.

---

## 9. Example Output

Example structured output:

| review_id | content_cleaned                     | score | word_count | sentiment_label | detected_aspects            | is_complaint |
| --------- | ----------------------------------- | ----: | ---------: | --------------- | --------------------------- | ------------ |
| 001       | app keeps crashing after the update |     1 |          6 | negative        | performance, update_version | True         |
| 002       | voice mode is very useful           |     5 |          5 | positive        | voice_audio                 | False        |
| 003       | i cannot log into my account        |     2 |          7 | negative        | login_account               | True         |
| 004       | subscription is too expensive       |     2 |          5 | negative        | subscription_billing        | True         |

---

## 10. Validation Plan

The prototype should include light validation rather than a full evaluation study.

### Manual Validation

Randomly sample 30 to 50 reviews and inspect:

1. Whether the detected aspect is reasonable.
2. Whether the sentiment label matches the review tone.
3. Whether complaint detection makes sense.
4. Whether any important issue was missed.

Example validation table:

| Review                               | Extracted Aspect | Sentiment | Is Output Reasonable? |
| ------------------------------------ | ---------------- | --------- | --------------------- |
| The app crashes every time I open it | performance      | negative  | Yes                   |
| I love the voice feature             | voice_audio      | positive  | Yes                   |
| I cannot sign into my account        | login_account    | negative  | Yes                   |
| The new design is confusing          | ui_design        | negative  | Yes                   |

### Summary Metrics

The validation section can report simple numbers:

```text
Number of reviews inspected: 50
Aspect extraction reasonable: 40 / 50
Sentiment label reasonable: 42 / 50
Complaint detection reasonable: 44 / 50
```

This is not a formal model evaluation. It is a lightweight sanity check to show that the pipeline output is meaningful.

---

## 11. Limitations

This first prototype has several limitations:

1. Keyword-based aspect extraction may miss implicit or indirect complaints.
2. Sentiment tools may not handle sarcasm or complex context well.
3. Some reviews may discuss multiple issues, making classification harder.
4. Short reviews may not contain enough information for reliable feature extraction.
5. The aspect dictionary must be updated manually.
6. Semantic grouping, if implemented, may require additional tuning and interpretation.

These limitations are acceptable for the first prototype because the current goal is to demonstrate a clear and practical feature engineering workflow.

---

## 12. Future Improvements

Possible future improvements include:

1. Expanding the aspect keyword dictionary.
2. Using embeddings to group similar complaints.
3. Training a supervised classifier for complaint detection.
4. Comparing review text sentiment with star ratings.
5. Tracking aspect frequency over time.
6. Building a dashboard for product issue monitoring.
7. Adding automated data quality checks.
8. Saving engineered features directly into a database table.

---

## 13. Proposed Project Structure

Recommended file structure:

```text
SA-Intern/
│
├── data/
│   ├── raw/
│   │   └── reviews.json
│   │
│   ├── processed/
│   │   └── engineered_reviews.csv
│
├── src/
│   ├── load_reviews.py
│   ├── clean_text.py
│   ├── extract_basic_features.py
│   ├── extract_sentiment.py
│   ├── extract_aspects.py
│   ├── validate_features.py
│   └── run_feature_pipeline.py
│
├── docs/
│   └── Feature_engineering_design.md
│
├── README.md
└── requirements.txt
```

---

## 14. Next Steps

### Step 1: Finalize Feature Scope

Start with the following required features:

```text
basic text features
sentiment / polarity
aspect extraction
complaint indicator
```

Treat semantic grouping as optional.

Do not expand the scope until the basic pipeline works end to end.

---

### Step 2: Prepare Input Data

Choose one input source:

```text
JSON file
CSV file
SQLite database
```

For the first implementation, using a CSV or JSON file is acceptable.

The input data should include at least:

```text
review_id
content
score
date
```

---

### Step 3: Build the Pipeline

Implement the pipeline in this order:

1. Load reviews.
2. Clean review text.
3. Extract basic text features.
4. Extract sentiment features.
5. Extract aspect labels.
6. Generate complaint indicators.
7. Save the output as CSV.
8. Run validation on sample reviews.

---

### Step 4: Generate Example Output

Create an output file:

```text
data/processed/engineered_reviews.csv
```

This file should show that raw review text has been converted into structured, model-ready features.

---

### Step 5: Validate the Results

Manually inspect 30 to 50 reviews.

Create a small validation summary showing:

```text
number of reviews inspected
examples of correct aspect extraction
examples of incorrect or missed extraction
main limitations
possible improvements
```

---

### Step 6: Update README

The README should explain:

1. What the pipeline does.
2. Why the selected features are useful.
3. How to run the pipeline.
4. What output file is generated.
5. What the current limitations are.

Example run command:

```bash
python src/run_feature_pipeline.py
```

---

## 15. Final Deliverables

The final deliverables for this stage should include:

1. `Feature_engineering_design.md`
   A design document explaining the feature choices, pipeline structure, and rationale.

2. `run_feature_pipeline.py`
   A runnable script that executes the full feature engineering pipeline.

3. `engineered_reviews.csv`
   A structured output file containing engineered review features.

4. `validate_features.py` or validation notes
   A lightweight validation showing that the extracted features are meaningful.

5. Updated `README.md`
   Instructions for running the prototype and understanding the output.

---

## 16. Key Principle

The main priority is not technical complexity.

The main priority is to build a small, clear, practical, and working prototype that demonstrates thoughtful feature engineering for review text data.

A focused pipeline with fewer features implemented well is better than a broad pipeline that is incomplete or difficult to explain.

