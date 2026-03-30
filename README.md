# CMP-X305 GitHub Pages Site

This workspace now includes a publishable GitHub Pages site under [`docs/`](c:/Sekhons/Roehampton/CYB/docs).

## What Was Added

- [`docs/index.html`](c:/Sekhons/Roehampton/CYB/docs/index.html): homepage
- [`docs/report/index.html`](c:/Sekhons/Roehampton/CYB/docs/report/index.html): full report page
- [`docs/assets/css/styles.css`](c:/Sekhons/Roehampton/CYB/docs/assets/css/styles.css): shared styling
- [`docs/assets/js/site.js`](c:/Sekhons/Roehampton/CYB/docs/assets/js/site.js): reveal and TOC behavior
- [`docs/assets/docs/cmp-x305-cybersecurity-portfolio-final.docx`](c:/Sekhons/Roehampton/CYB/docs/assets/docs/cmp-x305-cybersecurity-portfolio-final.docx): downloadable submission DOCX
- [`docs/assets/img/`](c:/Sekhons/Roehampton/CYB/docs/assets/img): normalized screenshot assets

## Deployment

1. Create a new GitHub repository and push this folder.
2. In GitHub, open `Settings` -> `Pages`.
3. Set `Build and deployment` to `Deploy from a branch`.
4. Select your main branch and choose the `/docs` folder.
5. Save. GitHub Pages will publish the site at `https://<username>.github.io/<repo>/`.

## Regenerating The HTML

If the report markdown changes, rerun:

```powershell
python .\_scripts\generate_github_pages_site.py
```
