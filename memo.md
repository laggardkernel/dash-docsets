# Docset Generation Tips

## General Guide
The steps here are for sphinx docs and HTML files.

### Generation
Edit `docs/conf.py`
- suppress generate of sidebar and decorations for sphinx doc
- enable custom CSS at the end of `conf.py`

```python
# options for html_theme = "alabaster"
html_theme_options = {
    'nosidebar': True,
    'show_powered_by': True,
    'show_related': False,
    'show_relbars': False,
    'github_button': False,
    'github_banner': False,

    # the display style I need
    'font_family': "Georgia, 'Bitstream Charter', Hiragino Mincho Pro, serif",
    'font_size': '1.0625rem',
    'head_font_family': "Garamond, Georgia, 'Bitstream Charter', serif",
    'code_font_family': "Monaco, Consolas, Menlo, 'Deja Vu Sans Mono', 'Bitstream Vera Sans Mono', monospace",
    'code_font_size': '0.85em',
}
```

```python
# at the end of confi.py
if "custom.css" in html_css_files:
    html_css_files.remove("custom.css")
html_css_files.append("custom.css")
```

Tweak width of content, sidebar, margin, etc, with custom css.

```css
/* copy and paste the content below into
 * docs/_build/html/_static/custom.css
 */
div.footer {width:auto; max-width:940px} div.document {max-width:none; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} div.bodywrapper {margin: 0 0 0 0px;}
div.body {max-width:none !important;}

pre {padding: 7px 10px !important;margin: 15px 0 !important;overflow:auto;}
div.admonition {margin:20px 0; padding:10px 10px;}
```

First part of the styles above is borrowed from Dash docset named Flask, which I think is added by Kapeli, the creator of Dash.

Build the docset with [doc2dash](https://github.com/hynek/doc2dash) for sphinx doc, and [dashing](https://github.com/technosophos/dashing) for general HTML files.

```shell
# sphinx doc with index
doc2dash -jv -n aiohttp -I index.html -u https://aiohttp.readthedocs.io/en/stable/ <path to HTML doc folder of aiohttp>

# OR
# html files without index
dashing create # edit dash.json
dashing build  # index will be generated
```

### Distribution
Most of the steps below could be got from [guide in repo Dash-User-Contributions](https://github.com/Kapeli/Dash-User-Contributions)

Compress the docset as a tarball.

```shell
tar --exclude='.DS_Store' -cvzf {doc_name}.tgz {doc_name}.docset
```

If you're making a contribution to [Dash-User-Contributions](https://github.com/Kapeli/Dash-User-Contributions) repo. You'd better verify the tarball beforehand. Put your files in the correct sub-folder in the forked repo, `cd` into the root folder, verify the compressed docset with the command from [.travis.yml](https://github.com/Kapeli/Dash-User-Contributions/blob/master/.travis.yml):

```shell
wget http://kapeli.com/feeds/zzz/docsetcontrib.tgz && tar -xzf docsetcontrib.tgz && ./docsetcontrib --verify
```

## Specific Memos
### aiohttp
- [Detailed generation steps written by me](https://github.com/Kapeli/Dash-User-Contributions/blob/3ac3210d4fc1ce68ce39e54138617e538603dd5d/docsets/aiohttp/README.md)
- Combine aiohttp doc and [aiohttp-demos](https://github.com/aio-libs/aiohttp-demos) doc together with relative path in `href`

### lxml
- When scraping the official site, leave folders of old version(`x.y`) and folder `files`.
- Be sure to enable javascript when building it with `doc2dash`

### pysheeet, cheatsheet of Python
- Increase max depth for toc in `docs/index.rst`: `:maxdepth: 2`.
- Display toc `div#table-of-contents {display: block;}`. Cause sidebar is removed, we need toc for navigation.
