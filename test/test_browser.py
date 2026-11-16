"""Browser test: python -m pytest test/ (needs `pip install playwright pytest` and `playwright install chromium`)."""
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

FIXTURE = (Path(__file__).parent / 'fixture.html').resolve().as_uri()

EXPECTED = """Explain Ex 1.

# Ex 1

## Exercise

Compute $\\int_0^1 x\\,dx$ and **justify**.

$$a < b$$

1. first
2. second *one*

MathJax 2: $x^2$ and $\\frac12$

| x | f |
| --- | --- |
| 0 | 1 \\| 2 |

---
Source: %s
""" % FIXTURE


def test_build_and_copy():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
        ctx = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = ctx.new_page()
        page.goto(FIXTURE)
        page.click('#go')
        page.wait_for_function("document.getElementById('go').textContent === 'Copied'")
        text = page.evaluate('navigator.clipboard.readText()')
        assert text == EXPECTED, text
        # A part revealed later is included.
        page.evaluate("document.getElementById('solution').hidden = false")
        md = page.evaluate("CopyForLLM.build({parts: [{title: 'Solution', el: document.getElementById('solution')}], prompt: '', footer: ''})")
        assert md == '## Solution\n\nsecret\n'
        browser.close()
