# City Grill Customer Analyst

An interactive customer-reviews dashboard and AI analyst for two City Grill Group restaurants in Bucharest — **Caru' cu Bere** and **Hanu' lui Manuc** — covering January 2025 to October 2026 (2026 year to date).

The interface follows the **Old Town Reviews Desk v2** layout (`reference/Old Town Reviews Desk v2.md`): venue ledgers, Ask the analyst, a data-source switch, ratings by half-year, star distribution, sub-ratings, themes, dishes and drinks, how Google reviews are written, key findings, trends, recommendations, the review sample and the method.

Management can pick a predefined question or ask their own (English or Romanian). The page counts and filters the reviews in code, shows the computed answer with KPIs and a module adapted to the question, highlights the relevant dashboard sections, sets the review explorer's filters, and suggests follow-ups and next analyses. A management briefing can be generated on demand.

## Repository contents

| Path | What it is |
| --- | --- |
| `index.html` | The application (v2 interface): one page, plain JavaScript, no build step. |
| `data/reviews.js` | The review data the page reads, generated from the coded CSV. |
| `tools/build_data.py` | Rebuilds `data/reviews.js` from `city_grill_reviews_coded.csv`. |
| `v1/index.html` | The previous interface (coded Tripadvisor sample only), kept for reference. |
| `AGENT_INSTRUCTIONS.md` | The agent's specification: role, data-integrity rules, dashboard views, predefined questions, briefing requirements. |
| `reference/` | The reference dashboards the agent was built from (v1 and v2). |

## Running it

Open `index.html` in a browser, or serve the folder with any static server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

The live copy is published with GitHub Pages from the `main` branch.

## Data

- **Google Maps:** 5,445 reviews pulled via the SignalQub API on 13 Oct 2026 (Caru' cu Bere 1,000, 30 Sep – 13 Oct, "most relevant"; Hanu' lui Manuc 4,445, 11 Aug – 13 Oct, "newest"). Themes and dishes are coded by multilingual keyword matching; praise/complaint follows the star rating (4–5★ / 1–2★).
- **Tripadvisor:** the 42 reviews with visits from Jan 2025 in the project's coded sample, paraphrased, coded per theme with +/− polarity, with sub-ratings where given.
- **Platform figures** (Google and Tripadvisor ratings and review counts, Oct 2026) are shown separately and never merged with the samples.

**Google review text is not published here.** Google's terms restrict redistributing review content, so `build_data.py` uses the text only to derive codes (themes, dishes, waiter named, name-only reviews, word count) and writes ratings, codes and flags, not the text. The Tripadvisor rows are paraphrases.

To rebuild the data after updating the CSV:

```bash
python3 tools/build_data.py path/to/city_grill_reviews_coded.csv v1/index.html
```

(`v1/index.html` supplies the Tripadvisor sub-ratings.)

## The AI analyst outside claude.ai

On claude.ai the page uses Claude directly (`window.claude`). Elsewhere (GitHub Pages, a local file) it has two modes:

1. **Calculated answers (default).** The page reads the restaurant, topic, dish, period and type of question, computes the answer from the reviews and writes it as an analyst would: conclusion first, comparisons, an example review, a recommended action and follow-up questions.
2. **Claude answers via your own proxy (optional).** Deploy `tools/analyst-proxy-worker.js` as a Cloudflare Worker with your `ANTHROPIC_API_KEY` as a secret, then set `ANALYST_ENDPOINT` in `index.html` to the Worker URL. The page sends the question plus the computed data (~100 KB) and shows Claude's answer; if the proxy fails it falls back to calculated answers. Never put an API key in the page itself.

## Data limitations

- Both samples show direction and themes, not statistically representative percentages.
- The two Google samples cover different periods and sort orders.
- The Tripadvisor sample over-represents longer, critical reviews; Hanu' lui Manuc has a single 2025 review.
- No dated menus are included, so menu-price history cannot be calculated; price analysis uses what reviewers say.

## Sources

- [Tripadvisor – Caru' cu Bere](https://www.tripadvisor.com/Restaurant_Review-g294458-d739896-Reviews-Caru_cu_bere-Bucharest.html)
- [Tripadvisor – Hanu' lui Manuc](https://www.tripadvisor.com/Restaurant_Review-g294458-d739908-Reviews-Restaurant_Hanu_Lui_Manuc-Bucharest.html)
- [SignalQub API](https://signalqub.com/docs)
- [RHN – Hanul lui Manuc, a strategic pillar for City Grill](https://rhn.ro/en/hanul-lui-manuc-a-strategic-pillar-for-city-grill/)
- [Financial Intelligence](https://financialintelligence.ro/?p=24097)
