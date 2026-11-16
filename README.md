# copy-for-llm

A small script (no dependency, under 9 KB) that adds a "copy for an AI" button to any web page.
The button copies parts of the page as clean Markdown, with:

1. a ready-made prompt on top (for example "explain this solution step by step");
2. the content, with the math as **LaTeX source** read from KaTeX, MathJax 2, MathJax 3 or a `data-tex` attribute;
3. the source URL at the bottom, so the AI knows where the text comes from.

Why: selecting rendered math and pasting it into ChatGPT, Claude or Gemini gives each symbol twice and loses fractions, exponents and integrals. The AI then misreads the exercise. This script copies what the renderer kept in the page instead.

Made for [EPITA Doomscrolling](https://epitadoomscrolling.pierref.eu), an exam training site for EPITA prépa students, by [Morgan Pierrefeu](https://morgan.pierref.eu).

## Use

```html
<div id="statement">Compute $\int_0^1 x\,dx$.</div>
<div id="solution">…</div>

<button data-copy-llm="#statement|Exercise; #solution|Solution"
        data-copy-title="Exercise 3"
        data-copy-prompt="I don't understand this solution. Explain it step by step.">
  Copy for an AI
</button>

<script src="copy-for-llm.js"></script>
<script>
  CopyForLLM.config({ footer: 'Source: {url}', done: 'Copied', failed: 'Copy failed' });
</script>
```

Or from jsDelivr: `https://cdn.jsdelivr.net/gh/evaspace/copy-for-llm@v1.0.0/copy-for-llm.js`.

Clicking the button copies:

```markdown
I don't understand this solution. Explain it step by step.

# Exercise 3

## Exercise

Compute $\int_0^1 x\,dx$.

## Solution

…

---
Source: https://example.org/page
```

### Attributes

| Attribute | Meaning |
| --- | --- |
| `data-copy-llm` | Parts to copy: `selector|heading`, separated by `;`. A part inside a `hidden` element is left out, so a solution is only copied once it is shown. |
| `data-copy-title` | Optional `# heading` and `{title}` value. Default `{title}` is the page title. |
| `data-copy-prompt` | Prompt for this button. Default: the `prompt` setting (empty). |
| `data-copy-footer` | Footer for this button. Default: the `footer` setting (`Source: {url}`). |
| `data-copy-ignore` | On any element: never copied. Buttons, scripts, `nav`, `svg` and `canvas` are skipped too. |

`{url}` and `{title}` are replaced in the prompt and the footer. The button fires a `copy-llm` event (`detail.ok`, `detail.text`).

### Script API

- `CopyForLLM.config(settings)`: `prompt`, `footer`, `done`, `failed`.
- `CopyForLLM.toMarkdown(element)`: Markdown of an element.
- `CopyForLLM.build({parts: [{title, el}], prompt, title, url, footer})`: the full text.
- `CopyForLLM.copy(text)`: copies to the clipboard (falls back to `execCommand` where the Clipboard API is blocked); resolves to `true` or `false`.

Converted: headings, paragraphs, bold, italics, lists, tables, links, code, images (alt text) and math (inline `$…$`, display `$$…$$`).

## Test

```sh
pip install playwright pytest && playwright install chromium
python -m pytest test/
```

## Licence

MIT
