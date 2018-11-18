# Docset Generation Tips

## General Guide
The steps here are for sphinx docs and HTML files.

### Generation
Edit `docs/conf.py`
- suppress generate of sidebar and decorations for sphinx doc
- enable custom styles at the end of `conf.py`, if it's available

```python
# options for html_theme = "alabaster"
html_theme_options = {
    'nosidebar': True,
    'show_powered_by': True,
    'show_related': False,
    'show_relbars': False,
    'github_button': False,
    'github_banner': False,

    # Only works for alabaster?
    'font_family': "'Gentium Book Basic', Georgia, 'Bitstream Charter', Hiragino Mincho Pro, serif",
    'font_size': '1.0625rem',
    'head_font_family': "Garamond, Georgia, 'Bitstream Charter', serif",
    'code_font_family': "Monaco, Consolas, Menlo, 'Deja Vu Sans Mono', 'Bitstream Vera Sans Mono', monospace",
    'code_font_size': '0.85em',
}
```

Tweak width of content, sidebar, margin, etc, with custom css.

```css
/* copy and paste the content below into
 * docs/_build/html/_static/custom.css
 */
div.footer {width:auto; max-width:none;} div.document {max-width:none; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} div.bodywrapper {margin: 0 0 0 0px;}
div.body {padding-left:30px;padding-right:30px;max-width:none !important;}

pre {padding: 7px 10px !important;margin: 15px 0 !important;overflow:auto;}
div.admonition {margin:20px 0; padding:10px 10px;}
```

First part of the styles above is borrowed from Dash docset named Flask, which I think is added by Kapeli, the creator of Dash.

Use styles below to modify font family if `html_theme_options` doesn't support font settings.

```css
body {font-family: 'Gentium Book Basic',Georgia,'Bitstream Charter','Hiragino Mincho Pro',serif;font-size: 1.0625rem;line-height:1.4;}
div.admonition p.admonition-title {font-family: 'Garamond','Georgia','Bitstream Charter',serif;}
pre, tt, code {font-family: Monaco,Consolas,Menlo,'Deja Vu Sans Mono','Bitstream Vera Sans Mono',monospace;font-size: 0.8em!important;}
h1, h2, h3, h4, h5, h6 {font-family: Garamond,Georgia,'Bitstream Charter',serif !important;font-weight:normal;}
/* optional */
/* body, div.body {...; color:#3E4349} */
```

Build HTML doc, with `make html`, or

```shell
# sphinx-build -b html {source_folder?} {output_folder}
sphinx-build -b html . ./_build
```

Build the docset with [doc2dash](https://github.com/hynek/doc2dash) for sphinx doc, and [dashing](https://github.com/technosophos/dashing) for general HTML files.

```shell
# sphinx doc with index
# enable javascript only if it's needed
doc2dash -v -n aiohttp -I index.html -u https://aiohttp.readthedocs.io/en/stable/ <path to HTML doc folder of aiohttp>

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

## Specific Formulae
### aiohttp
- https://aiohttp.readthedocs.io/en/stable/
- [Detailed generation steps](https://github.com/Kapeli/Dash-User-Contributions/blob/3ac3210d4fc1ce68ce39e54138617e538603dd5d/docsets/aiohttp/README.md)
- aiohttp theme is based on alabaster, so all options are available.
- Combine aiohttp doc and [aiohttp-demos](https://github.com/aio-libs/aiohttp-demos) doc together with relative path in `href`

### BeautifulSoup
- https://www.crummy.com/software/BeautifulSoup/bs4/download/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- `nosidebar`, the only option
- Generate a toc behind "Getting help" since the toc in sidebar is removed:

```restructured
Documentation content
---------------------

.. toctree::
   :maxdepth: 3

   index
```

- Override font family, font color
- Generate index with dashing

```json
    "selectors": {
        "div.section h1":{
            "type": "Guide",
            "regexp": "¶",
            "replacement": ""
        },
        "div.section h2":{
            "type": "Guide",
            "regexp": "¶",
            "replacement": ""
        },
        "div.section h3":{"type": "Guide",
            "regexp": "¶",
            "replacement": ""
        }
    },
```

### Bottle
- https://bottlepy.org/docs/0.12/
- ~~`make docs` in root folder of the source~~
- Use theme folder named `sphinx` from [bottlepy.org](https://github.com/bottlepy/bottlepy.org) repo
    - `html_theme = "alabaster"`
- `sphinx-build -b html -c docs/sphinx -d build/docs/doctrees docs build/docs/html`
- Use custom font styles since `bottle.css` replaces `alabaster.css`
    - `div.body {padding-left:30px;padding-right:30px;max-width:none !important;}`

### Celery
- http://docs.celeryproject.org/en/v4.2.1/
- Try to preserve the style, only code font is overridden

### Fabric
- http://docs.fabfile.org/en/2.4/
- `python setup.py develop`
- `sites/shared_conf.py`
- `export READTHEDOCS=True`, generate external links
- `sphinx-build -b html -c . -d _build/doctrees . _build/html`
- combine docs and www files together, relatify links with prefix `href="`:
    - `href="http://www.fabfile.org` -> `href="www`
    - `href="http://fabfile.org` -> `href="www/index.html`
    - `href="http://docs.fabfile.org/en/latest` -> `href="..`
    - `href="http://docs.fabfile.org` -> `href="../index.html`
- Enable toctree for www files in `index.rst`:

```
Table of Contents
-----------------

.. toctree::
    :maxdepth: 3

    changelog
    changelog-v1
    FAQs <faq>
    installing
    installing-1.x
    upgrading
    development
    troubleshooting
    Roadmap <roadmap>
    contact
```

- TODO: add docs of pyinvoke and paramiko

### Flask-RESTful
- https://flask-restful.readthedocs.io/en/0.3.6/
- `_static/flasky.css`
- Keep 1em indent on small screen:

```css
@media screen and (max-width: 870px) {
    ul {
        margin-left: 1em;
    }
}
```

### Flask-Script
- https://flask-script.readthedocs.io/en/latest/
- `python setup.py develop`
- Remove github badges after HTML files being built

### lxml
- https://lxml.de/
- Get the HTML files by building from the source, or scraping from the webside
    - When scraping the official site, leave folders of old version(`x.y`) and folder `files` alone
- Use custom styles for font
- Disable media query for `div.document` and `div.sidemenu`, use menu trigger all the time with styles below:

```css
/* copied from 2nd media query for div.sidemenu */
div.sidemenu > div.menutrigger {
    display: block;
    border: solid darkgreen 2px;
    padding: 2px;
    text-align: center;
    width: 6ex;
}

div.sidemenu > div.menu {
    display: none;
    position: absolute;
    z-index: 999;
    font-size: 9pt;
    text-align: left;
    border: groove gray;
    padding-right: 1ex;
    background: #FFFAFA url("python-xml.png") no-repeat top right;
}

div.sidemenu:hover > div.menu,
div.sidemenu.visible > div.menu {
    display: block;
}
/* give the content some padding */
div.document {padding:0 20px;color:#333;}
```

- Generate docset from these HTML files using [dashing](https://github.com/technosophos/dashing). Tweak the conf to get a better searchIndex.
    - Remove 404 items in searchIndex if it's needed.

### marshmallow
- Both 2.x and 3.x are needed

### PyQuery
- https://pyquery.readthedocs.io/en/latest/
- `native` theme. Only two options are available:
    - `nosidebar`
    - `sidebarwidth`
- `html_css_files = ["custom.css"]`
- Remove badges `a.image-reference` in `index.html`
- Disable javascript since there's a ajax request for mathjax

### PyMongo
- https://api.mongodb.com/python/3.7.2/
- https://github.com/mongodb/mongo-python-driver/
- Remove left padding for `div.body`

### pysheeet, Cheatsheet of Python
- https://www.pythonsheets.com/
- Increase max depth for toc in `docs/index.rst`: `:maxdepth: 2`.
- Display toc `div#table-of-contents {display: block;}`. Cause sidebar is removed, we need toc for navigation.

### Pytest
- https://docs.pytest.org/en/3.10.0/
- Based on flask theme, no useful options for docset generation
- Fix indent of unordered list in media query:

```css
@media screen and (max-width: 870px) {
    ul {
        margin-left: 1em;
    }
}
```

- Maybe it's a good idea to use theme `alabaster` since those two are very similar

### Requests
- http://docs.python-requests.org/en/master/
- remove badges: `find("body div h1").siblings().filter("a")`
- remove decorative images: `body div h1 + img`

### Requests-HTML
- https://html.python-requests.org/
- remove badges

### Selenium Python
- https://selenium-python.readthedocs.io/
- confi file path: `selenium-python/source/conf.py`

### Setuptools
- https://setuptools.readthedocs.io/en/stable/
- `:maxdepth: 3` for toctree of index page
- `html_theme = "alabaster"`, or comment the original theme since [alabaster](https://github.com/bitprophet/alabaster/) is the default theme.
- Remove underline in headings:

```css
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {text-decoration:none;}
```

- Dashing selector: `"a.toc-backref": "Guide"`

### Sphinx
- The theme is an adjusted version of the sphinxdoc theme. Only two options are available:
    - `nosidebar`
    - `sidebarwidth`
- Hence, additional styles for font-family are needed.
- Resize body width and reduce the size of `div.pageheader`:

```css
body {min-width: 0;max-width: none;border-left:none;border-right:0;}
div.pageheader {padding: 0;}
div.pageheader img {height:50px;}
div.pageheader ul {margin-top:15px;}
```

### Werkzeug
- http://werkzeug.pocoo.org/docs/0.14/
- The theme of it is based on alabaster, but there's no `html_theme_options` support. Append custom styles into `html/_static/werkzeug.css`.
