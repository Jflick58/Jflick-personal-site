# justinflick.com

Personal blog built with [Jekyll](https://jekyllrb.com/) and deployed via GitHub Pages.

## Adding a blog post

1. Create a file in `_posts/` named `YYYY-MM-DD-your-title.md`
2. Add front matter:
   ```yaml
   ---
   layout: post
   title: "Your Title"
   date: YYYY-MM-DD
   tags: [tag1, tag2]
   ---
   ```
3. Write your post in markdown below the front matter
4. Push to a branch and open a PR for a preview, or push to `main` to deploy

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000`.
