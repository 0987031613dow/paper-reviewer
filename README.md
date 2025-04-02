# Paper Reviewer Web Application

This is a web interface for the [paper-reviewer](https://github.com/deep-diver/paper-reviewer) project, which generates comprehensive reviews of academic papers from arXiv and OpenReview.

## Features

- Input arXiv ID or OpenReview ID to generate a review
- View detailed paper information including title, authors, abstract
- Explore paper sections with AI-generated summaries
- See extracted figures and tables with captions
- Browse paper references
- Download the full HTML review

## How to Use

1. Enter your Gemini API Key in the sidebar (required)
2. Enter an arXiv ID (e.g., "2310.06825") or OpenReview ID
3. Click "Process Paper" to generate a review
4. Explore the generated review with expandable sections

## Credits

This web application is built on top of the [paper-reviewer](https://github.com/deep-diver/paper-reviewer) project by deep-diver, which powers the [AI Paper Reviewer](https://deep-diver.github.io/ai-paper-reviewer) for Hugging Face Daily Papers.

## Setup for Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install poppler-utils (required for pdf2image)
# For Ubuntu
apt-get install poppler-utils
# For macOS
brew install poppler

# Set up environment variables
export GEMINI_API_KEY="your-api-key"
# Optional
export UPSTAGE_API_KEY="your-upstage-api-key"

# Run the app
streamlit run app.py
```

## Deployment

This app is designed to be deployed on Hugging Face Spaces. You can deploy it by:

1. Creating a new Space on Hugging Face
2. Select Docker as the SDK
3. Link this GitHub repository
4. Set your API keys as secrets in the Space settings

## Note

Processing papers can take some time, especially for longer papers or when using figure extraction features.
