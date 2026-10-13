# City Grill Customer Analyst

An interactive customer-reviews dashboard and AI analyst for two City Grill Group restaurants in Bucharest — **Caru' cu Bere** and **Hanu' lui Manuc** — covering January 2023 to October 2026 (2026 year to date).

Management can pick a predefined question or ask their own (English or Romanian). The page computes counts, rankings, trends and sub-ratings from a coded review sample in code, then adapts its KPIs, charts, findings, recommendations and evidence table to the question. It can also generate a management briefing from the current view.

## Repository contents

| Path | What it is |
| --- | --- |
| `index.html` | The full application: a single self-contained page (React 18 + htm from CDN, no build step). |
| `AGENT_INSTRUCTIONS.md` | The agent's specification — role, data-integrity rules, dashboard views, predefined questions, briefing requirements. |
| `reference/Old Town Reviews Desk.md` | The original reference dashboard the agent was built from (qualitative findings, platform ratings, sources). |

## Running it

Open `index.html` in a browser, or serve the folder with any static server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

To host it, enable **GitHub Pages** on this repository (Settings → Pages → deploy from the `main` branch, root folder).

## How the analysis works

- **Data:** a coded sample of 63 paraphrased Tripadvisor reviews (visits Aug 2023 – Oct 2026), embedded in `index.html` between the `ANALYTICS-START` / `ANALYTICS-END` markers. Each record holds venue, visit month, stars, optional Tripadvisor sub-ratings, theme codes (`+` praise, `-` complaint), a paraphrase and party type.
- **Calculations in code:** theme frequency, impact score (`mentions × (5 − average stars of those reviews)`), star distribution, averages by year, sub-rating comparisons, keyword-based sub-drivers, price mentions.
- **Platform figures** (Google and Tripadvisor ratings and review counts, Oct 2026) are shown separately from the sample and never merged with it.

## The AI analyst outside claude.ai

The written answers and briefing call Claude through the claude.ai artifact runtime (`window.claude`). That runtime only exists when the page is opened as a claude.ai Artifact. Opened from GitHub or locally, the dashboard, filters, charts, routing, findings and evidence table all still work from the embedded data, but the AI-written narrative will not. To restore it in a standalone deployment, replace the `window.claude.use("sample")` call with a call to your own backend that proxies the Anthropic API (never put an API key in the page).

## Data limitations

- The sample is small and not statistically representative of all reviews.
- 2023 has only 2 reviews (Hanu' lui Manuc only); 2026 dominates the sample.
- Three Oct 2026 Caru' cu Bere entries come from Tripadvisor's "recent 5★" strip and skew positive.
- No dated menu prices are included, so menu-price history cannot be calculated yet; price analysis uses anecdotal mentions in reviews only.

## Sources

- [Tripadvisor – Caru' cu Bere](https://www.tripadvisor.com/Restaurant_Review-g294458-d739896-Reviews-Caru_cu_bere-Bucharest.html)
- [Tripadvisor – Hanu' lui Manuc](https://www.tripadvisor.com/Restaurant_Review-g294458-d739908-Reviews-Restaurant_Hanu_Lui_Manuc-Bucharest.html)
- [RHN – Hanul lui Manuc, a strategic pillar for City Grill](https://rhn.ro/en/hanul-lui-manuc-a-strategic-pillar-for-city-grill/)
- [Financial Intelligence](https://financialintelligence.ro/?p=24097)
