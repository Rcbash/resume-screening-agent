# Resume Screening Agent

A Python-based CLI tool for automatically ranking resumes against a job description using NLP similarity scoring.

## Overview

The Resume Screening Agent analyzes job descriptions and multiple resume files, scoring each candidate based on skill match, text similarity, and experience relevance. It supports multiple resume formats (.txt, .pdf, .docx) and can optionally use OpenAI's API for enhanced reasoning.

## Features

- **Multi-Format Support**: Parse resumes in .txt, .pdf, and .docx formats
- **Intelligent Scoring**: Uses TF-IDF and cosine similarity for unbiased ranking
- **Skill Extraction**: Automatically identifies technical skills and competencies
- **OpenAI Integration**: Optional AI-powered reasoning for deeper analysis
- **Comprehensive Output**: Generates ranked results in CSV and JSON formats
- **Clear Reasoning**: Provides detailed scoring explanations for each candidate
- **No External Dependencies (Optional)**: Works with just Python stdlib, enhanced features opt-in

## Project Structure

```
Roman tech assesment 1/
├── main.py                          # CLI entry point
├── resume_parser.py                 # Resume file parsing
├── resume_scorer.py                 # Scoring logic
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── verify_setup.py                  # Setup verification script
├── data/
│   ├── job_description.txt          # Sample job description
│   └── resumes/                     # Sample resume files (11 files)
│       ├── resume_01_john_anderson.txt
│       ├── resume_02_sarah_martinez.txt
│       ├── resume_03_michael_chen.txt
│       ├── resume_04_emma_wilson.txt
│       ├── resume_05_david_kumar.txt
│       ├── resume_06_jessica_patel.txt
│       ├── resume_07_alex_thompson.txt
│       ├── resume_08_rachel_green.txt
│       ├── resume_09_mark_johnson.txt
│       ├── resume_10_lisa_anderson.txt
│       └── resume_11_robert_wilson.txt
└── outputs/                         # Generated results (created after first run)
    ├── ranked_candidates.csv        # Results in CSV format
    └── ranked_candidates.json       # Results in JSON format
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### 1. Clone or Download the Project

```bash
cd "Roman tech assesment 1"
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install required packages (only needed for PDF/DOCX support)
pip install -r requirements.txt
```

**Note**: The core functionality works with just Python's standard library. Additional packages are only needed if you want to process PDF or DOCX resume files.

### 4. (Optional) Configure OpenAI API

If you want to use OpenAI's API for enhanced scoring:

```bash
# Set your OpenAI API key (replace with your actual key)
export OPENAI_API_KEY='your-api-key-here'

# On Windows:
set OPENAI_API_KEY=your-api-key-here
```

## How to Run

### Basic Usage

Run the agent with the sample data:

```bash
python main.py --jd data/job_description.txt --resumes data/resumes --output outputs
```

### Command Line Options

```
python main.py --help

Options:
  --jd PATH              Path to job description file (required)
  --resumes PATH         Path to folder containing resumes (required)
  --output PATH          Output directory for results (required)
  --use-openai           Use OpenAI API for enhanced scoring (optional)
  --verbose              Print verbose output (optional)
```

### Example Commands

**Basic run with sample data:**
```bash
python main.py --jd data/job_description.txt --resumes data/resumes --output outputs
```

**With verbose output:**
```bash
python main.py --jd data/job_description.txt --resumes data/resumes --output outputs --verbose
```

**With OpenAI API (requires OPENAI_API_KEY):**
```bash
export OPENAI_API_KEY='sk-...'
python main.py --jd data/job_description.txt --resumes data/resumes --output outputs --use-openai
```

**Custom paths:**
```bash
python main.py --jd custom_job.txt --resumes ./candidate_resumes --output ./results
```

## Scoring Methodology

### Local Scoring Method (Default)

The agent uses a hybrid scoring approach:

#### 1. **TF-IDF Similarity (70% weight)**
   - Converts job description and resume to TF-IDF vectors
   - Calculates cosine similarity between vectors
   - Measures overall text relevance
   
   **Formula**: 
   ```
   TF-IDF = (Term Frequency × Inverse Document Frequency)
   Similarity = (vec1 · vec2) / (||vec1|| × ||vec2||)
   ```

#### 2. **Skill Matching (30% weight)**
   - Extracts technical keywords from job description
   - Identifies skills found in resume
   - Scores based on skill overlap
   
   **Factors**:
   - Direct skill matches with job requirements
   - Total number of relevant skills (shows broad expertise)
   - Percentage of job-required skills present

#### 3. **Final Score Calculation**
   ```
   Score = (TF-IDF_Score × 0.7 + Skill_Match × 0.3) × 100
   Range: 0-100
   ```

### Optional OpenAI Enhancement

If OpenAI API is configured, the system also:
- Sends resume summary to GPT-3.5-turbo
- Gets AI assessment of candidate fit
- Blends OpenAI score (30%) with local score (70%)
- Provides additional reasoning and context

### Scoring Interpretation

- **90-100**: Excellent fit - Strong skills match, high relevance
- **80-89**: Very Good fit - Most required skills present
- **70-79**: Good fit - Adequate skills, some gaps
- **60-69**: Fair fit - Some relevant experience, notable gaps
- **50-59**: Partial fit - Limited relevant experience
- **Below 50**: Poor fit - Minimal relevance to role

## Output Files

### 1. ranked_candidates.csv
Tab-separated file with columns:
- **rank**: Candidate ranking (1 = best match)
- **name**: Candidate name
- **score**: Relevance score (0-100)
- **skills**: Top detected technical skills
- **education**: Education summary
- **reasoning**: Brief scoring reason

### 2. ranked_candidates.json
Structured JSON with detailed information:
```json
{
  "total_candidates": 11,
  "timestamp": "2024-01-15T10:30:00.000000",
  "candidates": [
    {
      "rank": 1,
      "name": "John Anderson",
      "score": 85.42,
      "skills": ["Python", "React", "AWS", "Docker", "Kubernetes"],
      "education": "Bachelor of Science in Computer Science",
      "experience": "Senior Full Stack Engineer with 7+ years...",
      "reasoning": "Comprehensive TF-IDF analysis..."
    }
  ]
}
```

## Tradeoffs and Limitations

### Strengths
✓ **No API dependency** - Works without internet or OpenAI API
✓ **Fast processing** - TF-IDF scoring is computationally efficient
✓ **Fair and consistent** - Uses mathematical formulas, not subjective rules
✓ **Transparent** - Detailed reasoning provided for each score
✓ **Multi-format** - Supports .txt, .pdf, and .docx files
✓ **Extensible** - Easy to add custom scoring rules

### Limitations
✗ **Text-based only** - Cannot assess soft skills, personality, or communication style from text
✗ **Keyword-dependent** - May miss relevant experience written differently than expected keywords
✗ **No parsing edge cases** - Assumes well-formatted resumes; struggles with unusual layouts
✗ **Generic skills extraction** - No deep understanding of context or experience depth
✗ **No candidate verification** - Cannot verify claimed skills or employment history
✗ **Language dependent** - Works best with English language resumes
✗ **One-way comparison** - Scores fit to job, not company culture or candidate preferences

### Recommendations for Use
- **Use as screening tool only** - Not a replacement for human review
- **Combine with other signals** - Consider interviews, portfolios, references
- **Verify top candidates** - Always review top-ranked resumes manually
- **Adjust weights** - Modify TF-IDF/skill weights for different roles
- **Regular calibration** - Compare AI rankings with actual hire success

## Sample Output

When you run the agent with the included sample data, you'll see output like:

```
Loading job description...
✓ Job description loaded (2145 characters)

Loading and parsing resumes...
Found 11 resume(s) to process
  ✓ Parsed: resume_01_john_anderson.txt
  ✓ Parsed: resume_02_sarah_martinez.txt
  ...
✓ Successfully parsed 11 resume(s)

Scoring resumes against job description...
✓ Scoring complete

Creating output directory...
✓ Output directory: outputs

Saving results...
✓ CSV results saved: outputs/ranked_candidates.csv
✓ JSON results saved: outputs/ranked_candidates.json

================================================================================
RESUME RANKING RESULTS
================================================================================

################################################################################
Rank: 1
Name: John Anderson
Score: 85.42/100
Skills: Python, JavaScript, TypeScript, React, PostgreSQL, AWS, Docker, Kubernetes

Reasoning:
Candidate: John Anderson
Overall Score: 85.42
Score Breakdown:
  - TF-IDF Similarity: 78.3%
  - Skill Match: 92.5%
Detected Skills: Python, JavaScript, TypeScript, React, PostgreSQL, AWS, Docker, Kubernetes

...
```

## Verification Script

To verify your setup is correct:

```bash
python verify_setup.py
```

This will:
- Check Python version
- Verify required files exist
- Test resume parsing
- Verify output directory creation
- Report any issues

## Troubleshooting

### Issue: "Job description file not found"
**Solution**: Ensure the path to the job description file is correct and the file exists.

### Issue: "No resume files found"
**Solution**: 
- Check that the resumes directory exists
- Verify files have correct extensions (.txt, .pdf, .docx)
- Ensure the path is spelled correctly

### Issue: "ImportError: No module named 'docx'"
**Solution**: Install python-docx:
```bash
pip install python-docx
```

### Issue: "OpenAI API error" when using --use-openai
**Solution**:
- Verify OPENAI_API_KEY is set correctly
- Check your API key is valid and has credits
- Ensure network connection is working

### Issue: Strange characters in resume output
**Solution**: Resume files may use different encodings. Try:
```bash
# Convert file to UTF-8
iconv -f ISO-8859-1 -t UTF-8 resume.txt -o resume_utf8.txt
```

## How to Use With Your Own Data

### 1. Prepare Job Description
Create a file (e.g., `my_job.txt`) with the job description:
```
Senior Backend Engineer

Requirements:
- 5+ years experience with Python
- AWS and Docker knowledge
...
```

### 2. Prepare Resumes Folder
Create a folder with resume files:
```
my_resumes/
├── candidate_1.txt
├── candidate_2.txt
├── candidate_3.pdf
└── candidate_4.docx
```

### 3. Run the Agent
```bash
python main.py --jd my_job.txt --resumes my_resumes --output my_results
```

### 4. Review Results
Check the output files:
- `my_results/ranked_candidates.csv` - Quick overview
- `my_results/ranked_candidates.json` - Detailed analysis

## Advanced Usage

### Modifying Scoring Weights

Edit `resume_scorer.py` in the `score_resume()` method:

```python
# Change weights (default: 0.7 TF-IDF, 0.3 skill match)
local_score = min(100, (tfidf_score * 0.8 + skill_bonus * 0.2) * 100)
```

### Adding Custom Keywords

Edit `resume_scorer.py` in the `_extract_key_keywords()` method to add your own technical keywords.

### Custom Scoring Logic

Create a subclass of `ResumeScorer` and override the `score_resume()` method with your custom logic.

## Performance

- **Parsing**: ~50-100ms per resume (text files faster than PDF/DOCX)
- **Scoring**: ~10-20ms per resume (depends on resume length)
- **Total Time**: ~1-2 seconds for 10 resumes (mostly I/O)
- **Memory**: Minimal (<50MB for 100 resumes)

## Technical Stack

- **Language**: Python 3.7+
- **Core Libraries**: 
  - `collections` - For Counter, word frequency analysis
  - `math` - For cosine similarity calculations
  - `csv` - For CSV output
  - `json` - For JSON output
- **Optional Libraries**:
  - `PyPDF2` - PDF parsing
  - `python-docx` - DOCX parsing
  - `openai` - OpenAI API integration

## Contributing

To extend the agent:

1. **Add new scoring methods** - Create methods in `ResumeScorer` class
2. **Support new resume formats** - Add parsers to `ResumeParser` class
3. **Improve skill extraction** - Enhance `_extract_skills()` method
4. **Add output formats** - Create new save functions (Excel, JSON, etc.)

## License

This project is provided as-is for evaluation and educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the sample output for expected behavior
3. Verify all files are in the correct locations
4. Run `verify_setup.py` to check configuration

---

**Ready to screen resumes?** Run this command:
```bash
python main.py --jd data/job_description.txt --resumes data/resumes --output outputs
```
