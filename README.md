# City Grill Customer Analyst

An interactive customer-reviews dashboard with an AI analyst for two City Grill Group restaurants in Bucharest, **Caru' cu Bere** and **Hanu' lui Manuc**, covering January 2025 to October 2026 (2026 year to date).

Management can ask a question in English or Romanian, or pick a suggested one, and get an answer grounded in the review data, with follow-up questions. The rest of the page shows ratings by half-year, star distribution, sub-ratings, themes, dishes and drinks, Google review habits, key findings, trends, recommendations, a filterable review explorer and the method.

## Repository contents

| Path | What it is |
| --- | --- |
| `index.html` | The application: one self-contained page (plain JavaScript, no build step, data embedded). |
| `data/tripadvisor_2025_2026_coded.csv` | The 406 Tripadvisor reviews used (paraphrased), with stars, sub-ratings, party type and themes coded as praised / criticised. |
| `data/google_2026_coded.csv` | The 5,445 Google Maps ratings used, with keyword-coded themes and flags (waiter named, owner replied, has text), without review text. |
| `tools/analyst-proxy-worker.js` | Optional Cloudflare Worker that lets copies outside claude.ai get Claude-written answers. |
| `AGENT_INSTRUCTIONS.md` | The agent's specification: role, data-integrity rules, dashboard views, predefined questions. |

## Running it

Open `index.html` in a browser, or serve the folder (`python3 -m http.server 8000`). The live copy is published with GitHub Pages from `main`.

## How the analyst answers

- **Inside claude.ai** (the page opened as a claude.ai Artifact): the page sends Claude its instructions, the review summaries it has calculated and the reviews most relevant to the question. Claude writes the answer: conclusion first, then insights with concrete details from the reviews.
- **Anywhere else** (GitHub Pages, a local file): Claude is not available, so the page answers by itself. It reads the restaurant, topic, dish, period and type of question, computes the figures from the data and writes a structured answer with an example review, a recommended action and follow-ups. These answers are accurate but rule-based.
- **Optional:** deploy `tools/analyst-proxy-worker.js` as a Cloudflare Worker with an `ANTHROPIC_API_KEY` secret and set `ANALYST_ENDPOINT` in `index.html` to its URL to get Claude-written answers outside claude.ai. Never put an API key in the page.

## Data

- **Google Maps:** 5,445 reviews pulled via the SignalQub API on 13 Oct 2026. Caru' cu Bere: 1,000 reviews (30 Sep – 13 Oct 2026, "most relevant"). Hanu' lui Manuc: 4,445 reviews (11 Aug – 13 Oct 2026, "newest"). The API returns at most ~4,445 per request, so earlier Google reviews are not covered. Reviewer names and photos were removed. Themes are coded by multilingual keyword matching; praise / complaint follows the star rating (4–5★ / 1–2★).
- **Tripadvisor:** 406 English-language reviews with visits from Jan 2025 to Oct 2026 (Caru' cu Bere 280, Hanu' lui Manuc 126), read page by page on Tripadvisor on 13–14 Oct 2026, each paraphrased and coded per theme with praise / complaint polarity and sub-ratings where given.
- **Platform figures** (Google 4.6 / 4.7, Tripadvisor 4.1 / 4.1, Oct 2026) are shown separately and never merged with the samples.

## Limitations

- Both samples show direction and themes, not statistically representative percentages.
- The Google samples cover only Aug–Oct 2026, with different periods and sort orders per restaurant, so history comes from Tripadvisor alone.
- Tripadvisor lists reviews in its "detailed reviews" order; the sample averages about 3.5–3.6★ against 4.1 platform-wide, so longer, critical reviews are over-represented.
- Many Google reviews name a waiter (about half at Caru' cu Bere, three in four at Hanu' lui Manuc), which suggests prompted reviews and inflates the Google average.
- No dated menus are included, so menu-price history cannot be calculated; price analysis uses what reviewers say.
- `index.html` embeds the original Google review text so the review explorer and the analyst can show it. Google's terms restrict redistributing review content; keep the repository private or remove the text before sharing publicly.

## Sources

- [Tripadvisor – Caru' cu Bere](https://www.tripadvisor.com/Restaurant_Review-g294458-d739896-Reviews-Caru_cu_bere-Bucharest.html)
- [Tripadvisor – Hanu' lui Manuc](https://www.tripadvisor.com/Restaurant_Review-g294458-d739908-Reviews-Restaurant_Hanu_Lui_Manuc-Bucharest.html)
- [SignalQub API](https://signalqub.com/docs)
- [RHN – Hanul lui Manuc, a strategic pillar for City Grill](https://rhn.ro/en/hanul-lui-manuc-a-strategic-pillar-for-city-grill/)
- [Financial Intelligence](https://financialintelligence.ro/?p=24097)
