# Dash Docsets
Dash docsets with custom styles

### Why
- There's still no way to load custom CSS in Dash. I need to modify the styles by myself.
- Some of the user contributed docsets are far from the criterion of [Docset Contribution Checklist](https://github.com/Kapeli/Dash-User-Contributions/wiki/Docset-Contribution-Checklist), especially those with sidebar, github banner, decoration images, etc.
- It's not a good idea to submit to [Dash-User-Contributions repo](https://github.com/Kapeli/Dash-User-Contributions) with flavored docsets but not the vanilla ones.
- I need a place to share these docsets.

### Docset Feeds
- aiohttp
    - https://github.com/laggardkernel/dash-docsets/raw/master/feeds/aiohttp.xml
    - dash-feed://https%3A//github.com/laggardkernel/dash-docsets/raw/master/feeds/aiohttp.xml

**Note**: Dash feed links could not be rendered clickable because of [sanitization](https://github.com/jch/html-pipeline/blob/5feb0c185fb1e5037e3ad6d6bd533fb4af3685d8/lib/html/pipeline/sanitization_filter.rb#L40) of html-pipline.
