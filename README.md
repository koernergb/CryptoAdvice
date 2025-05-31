# Crypto Market Analyzer

A real-time cryptocurrency market analysis tool that scrapes the latest news from CoinDesk and provides AI-powered market insights using the Groq LLM.

## Features

- Live crypto news scraping from CoinDesk
- AI-powered market analysis including:
  - Key market signals (bullish/bearish indicators)
  - Asset allocation advice
  - Risk assessment
  - Actionable recommendations
- Clean, user-friendly Streamlit interface
- Real-time updates

## Prerequisites

- Python 3.7+
- Groq API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/koernergb/CryptoAdvice.git
cd crypto-market-analyzer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

3. Set up environment variables:

```bash
export GROQ_API_KEY=your_api_key_here
```

## Usage

Run the application locally:

```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration for automatic deployment.

To deploy:
1. Fork this repository
2. Create a new Web Service on Render
3. Connect your repository
4. Add your `GROQ_API_KEY` to the environment variables
5. Deploy!

## Tech Stack

- [Streamlit](https://streamlit.io/) - Web interface
- [Groq](https://groq.com/) - LLM API for market analysis
- [crawl4ai](https://github.com/crawl4ai/crawl4ai) - Web scraping
- [Playwright](https://playwright.dev/) - Browser automation

## License

[MIT License](LICENSE)
