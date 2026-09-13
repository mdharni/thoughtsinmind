# Thoughts in Mind — website

Static, multi-page site. No build tools or hosting dependencies required.

## Pages
- index.html — Home
- about.html — Mission and research foundation (with references)
- workshops.html — The six workshops and what a session looks like
- team.html — Facilitators and training
- facilities.html — How it works with your facility, FAQ, families, service area
- contact.html — Contact details and inquiry form (opens the visitor's email app)

Shared: styles.css, site.js. Fonts load from Google Fonts (Fraunces, Atkinson Hyperlegible).

## Editing
Content lives in build.py. Edit the text there and run:

    python3 build.py

This regenerates every page with the shared header and footer. You can also edit the .html files directly if you prefer, but build.py will overwrite them next time it runs.

## Publishing
Upload the contents of this folder (not build.py or README.md) to any static host:
Netlify Drop, Cloudflare Pages, GitHub Pages, Vercel, or your domain registrar's hosting.
Point your domain at the host and the site is live.

## Preview locally

    python3 -m http.server 8765

Then open http://localhost:8765
