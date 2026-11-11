# Sales Agent

Research agents that prepare a salesperson for a first meeting. Describe your product and the company you're meeting, and Sales Agent searches the web for the account's priorities, the people in the room and how your competitors compare. It then writes a one-page brief with talking points. Every source in the brief is a page the agents actually cited.

Built with Python, Streamlit and Claude (Sonnet 5.5 with server-side web search). Live at [sales-agent.tahamukhtar.com](https://sales-agent.tahamukhtar.com).

## How it works

Five agents run as a short pipeline: a product summary, then three research agents in parallel (account, stakeholders, competitors), then a final briefing. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the flow, each agent's role and how citations become the source list.

## Running locally

Requires Python 3.12 and an Anthropic API key.

```bash
cp .env.example .env        # then set ANTHROPIC_API_KEY
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

With Docker instead:

```bash
cp .env.example .env        # then set ANTHROPIC_API_KEY
docker compose up
```

## Configuration

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | | Anthropic API key |
| `ANTHROPIC_MODEL` | No | `claude-sonnet-5-5` | Claude model used by the agents |
| `SESSION_BRIEF_LIMIT` | No | `2` | Briefs per browser session; `0` turns the limit off |
| `DAILY_BRIEF_LIMIT` | No | `10` | Briefs per UTC day across all visitors; `0` turns the limit off |

## Limitations

- Results depend on what is publicly findable; for small or private companies the brief says when it couldn't verify something.
- Each brief makes four or five model calls with up to 36 web searches, so it takes a minute or two and costs a few cents.

## Deployment

The app runs on Streamlit Community Cloud, with the API key and the limits set in the app's Secrets. Streamlit Community Cloud doesn't support custom domains, so `redirect/` is a small Cloudflare Worker that sends sales-agent.tahamukhtar.com to the Streamlit URL (`npx wrangler deploy` from that folder).

## License

MIT, see [LICENSE](LICENSE).

The `markdown-pdf` dependency pulls in PyMuPDF, which is licensed under AGPL-3.0.
