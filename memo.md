# Docset Generation Tips

## General Guide
The steps here are for sphinx docs and HTML files.

### Generation
Edit `docs/conf.py`
- suppress generate of sidebar and decorations for sphinx doc
- enable custom styles at the end of `conf.py`, if it's available

```python
# options for alabaster
html_theme = "alabaster"
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
    'code_font_family': "'IBM Plex Mono', Consolas, Menlo, 'Deja Vu Sans Mono', 'Bitstream Vera Sans Mono', monospace",
    'code_font_size': '0.85em',
}

html_css_files = ["custom.css"]
```

Tweak width of content, sidebar, margin, etc, with custom css.

```css
/* copy and paste the content below into
 * docs/_build/html/_static/custom.css
 */
div.footer {width:auto; max-width:none;} div.document {max-width:none; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} div.bodywrapper {margin: 0 0 0 0px;}
body {padding-left:30px;padding-right:30px;max-width:none !important;}
div.body {padding-left:0;padding-right:0;max-width:none !important;}
pre {padding: 7px 10px !important;margin: 15px 0 !important;overflow:auto;}
div.admonition {margin:20px 0; padding:10px 10px;}
```

```css
// indent of the list
@media screen and (max-width: 870px) {
    ol, ul {
        margin-left: 1em;
    }
}
```

First part of the styles above is borrowed from Dash docset named Flask, which I think is added by Kapeli, the creator of Dash.

Use styles below to modify font family if `html_theme_options` doesn't support font settings.

```css
body, div.body {font-family: 'Gentium Book Basic',Georgia,'Bitstream Charter',serif;font-size:1.0625rem;line-height:1.4;color:#3E4349;}
div.admonition p.admonition-title {font-family: 'Garamond','Georgia','Bitstream Charter',serif;}
pre, tt, code {font-family: 'IBM Plex Mono',Consolas,Menlo,'Deja Vu Sans Mono','Bitstream Vera Sans Mono',monospace;font-size: 0.8em!important;}
h1, h2, h3, h4, h5, h6 {font-family: Garamond,Georgia,'Bitstream Charter',serif !important;font-weight:normal;}
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
### aiocache
- https://aiocache.readthedocs.io/en/0.11.1/
- https://github.com/argaen/aiocache
- `pip install ".[redis,memcached,msgpack,dev]"`

### aiohttp
- https://aiohttp.readthedocs.io/en/stable/
- [Detailed generation steps](https://github.com/Kapeli/Dash-User-Contributions/blob/3ac3210d4fc1ce68ce39e54138617e538603dd5d/docsets/aiohttp/README.md)
- aiohttp theme is based on alabaster, so all options are available.
- Combine aiohttp doc and [aiohttp-demos](https://github.com/aio-libs/aiohttp-demos) doc together with relative path in `href`
    - Build aiohttp-demos and move the generated "html" folder into aiohttp as `docs/aiohttp-demos`
    - Configure `intersphinx_mapping` in `conf.py` for aiohttp-demos, build aiohttp docs
    - Move the "aiohttp-demos" folder into `_build/html` within aiohttp
- Modify css to maximize content width

### aioredis
- https://aioredis.readthedocs.io/en/v1.3.1/
- https://github.com/aio-libs/aioredis/

### asyncpg
- https://magicstack.github.io/asyncpg/current/
- https://github.com/MagicStack/asyncpg
- Clone recursively to get the submodule
- Remove badges `a.image-reference` in `index.html`

### Babel
- http://babel.pocoo.org/en/latest/
- Custom bable theme based on basic.
    - Only support `"nosidebar": True` in `html_theme_options`
- Modifying `babel.css` is needed: style, font.

### BeautifulSoup
- https://www.crummy.com/software/BeautifulSoup/bs4/download/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- `nosidebar`, the only option
- Generate a toc behind "Getting help" since the toc in sidebar is removed:

```restructured
Table of Content
----------------

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

### CacheControl
- https://cachecontrol.readthedocs.io/en/latest/
- Replace default with theme: alabaster
- Build index with dashing

```json
    "selectors": {
        "h1, h2": {
            "type": "Guide",
            "regexp": "�",
            "replacement": ""
        }
    },
```

### Celery
- http://docs.celeryproject.org/en/v4.2.1/
- Try to preserve the style, only code font is overridden

### Click
- https://click.palletsprojects.com/en/7.x/
- theme: click
- `pip install -r docs/requirements.txt`
- Do customization in `click.css`
- Do not add padding or margin for `pre`
- Resize margin between list items:
    - `li > p {margin:0;}`

### Conda
- https://conda.io/docs/
- https://github.com/conda/conda-docs
- Override theme as alabaster
- Enable toctree in `index.rst`
    - Move `release-notes` to the end
    - `:maxdepth: 2`
- Dependencies `docs/deps.recipe/meta.yaml`
    - `help2man`
    - `man2html`
    - `numpydoc`
- `make html`

### Django
- Based on docset distributed by Dash
- Customize font family only in `pygments.css`

```css
body {font-family: 'Gentium Book Basic',Georgia,'Bitstream Charter','Hiragino Mincho Pro',serif;font-size: 17px !important;line-height:1.4;}
```

### Elasticsearch-Py
- https://github.com/elastic/elasticsearch-py
- https://elasticsearch-py.readthedocs.io/en/6.3.1/

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

### Falcon
- https://github.com/falconry/falcon
- https://falcon.readthedocs.io/en/3.0.0a1/
- `export DASHBUILD=True`
- Modify `custom.csS` brought by Falcon
  - comment font-family Oxygen of body, code, etc.
  - disable bold font weight in headers

### Flask-Admin
- https://flask-admin.readthedocs.io/en/v1.5.2/
- `pip install -r requirements-dev.txt`
- `sphinx-build -b html -c . -d _build/doctrees . _build/html`
- `flasky` theme, modify `flasky.css` with font style override

Keep list indentation on small screen with:

```css
@media screen and (max-width: 870px) {
    ul {
        margin-left: 0;
    }
}
```

### Flask-Bootstrap
- https://pythonhosted.org/Flask-Bootstrap/

### Flask-CKEditor
- https://github.com/greyli/flask-ckeditor/
- https://flask-ckeditor.readthedocs.io/en/stable/
- Override font family with `custom.css`

```shell
pip install -r docs_requirements.txt
pip install wtforms
```

### Flask-DebugToolbar
- https://flask-debugtoolbar.readthedocs.io/en/stable/
- `pip install Flask-Sphinx-Themes`
- Override content width and font family in `custom.css`
- Remove side padding from `div.body`, leave it on `body`

### Flask-Login
- https://flask-login.readthedocs.io/en/0.4.1/
- Override layout and font family in `custom.css`
- Remove github badge manually

### Flask-RESTful
- https://flask-restful.readthedocs.io/en/0.3.6/
- Modify `_static/flasky.css` with font style override

### Flask-Script
- https://flask-script.readthedocs.io/en/latest/
- `python setup.py develop`
- Remove github badges after HTML files being built

### Flask-Security
- https://pythonhosted.org/Flask-Security/
- `pip install -r docs/requirements.txt`
- Override content width and font family in `custom.css`

### Flask-SQLAlchemy
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/ (3.x is still in development)
- `pip install -r docs/requirements.txt`
- Remove sidebar
- Override default font in `flask.css` after building html

### Flask-WTF
- https://flask-wtf.readthedocs.io/en/stable/
- `pip install Flask-Sphinx-Themes`
- `__import__("flask_sphinx_themes")` in `docs/conf.py`
- Modify `_static/flasky.css`

### IPython
- https://ipython.readthedocs.io/en/7.1.1/
- https://github.com/ipython/ipython
- `pip install -r docs/requirements.txt`
- `pip install nose testpath`
- Enable `toctree` with depth 2 in `index.rst`
    - Enable `toctree` in all source files

```python
html_theme_options = {
    "analytics_id": "",
    "logo_only": False,
    "display_version": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 34,
    "includehidden": True,
    "titles_only": False,
}
```

- Override styles of font-family in `_static/css/theme.css`
- Build docset with JavaScript enabled

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
- https://marshmallow.readthedocs.io/en/2.x-line/
- https://marshmallow.readthedocs.io/en/3.0/
- Both 2.x and 3.x are needed
- `pip install sphinx{,issues,version-warning}`
- Modify `static/custom.css`

### Matplotlib
- Failed to build
- https://matplotlib.org/2.2.3/
- https://matplotlib.org/3.0.2/
- Download source from the doc branches with `git clone`
    - `https://github.com/matplotlib/matplotlib.git`
    - `git clone -b v2.2.3-doc https://github.com/matplotlib/matplotlib.git matplotlib-v2.2.3-doc`
    - `git clone -b v3.0.2-doc https://github.com/matplotlib/matplotlib.git matplotlib-v3.0.2-doc`
- `pip install -r requirements/doc-requirements.txt`
- `brew install graphviz`
- `brew cask install basictex`

### Mutagen
- `index.rst`, enable `:toctree`, move to the end with heading "Table of Contents"
- https://mutagen.readthedocs.io/en/latest/
- https://github.com/quodlibet/mutagen/

### Peewee
- http://docs.peewee-orm.com/en/latest/
- https://github.com/coleifer/peewee
- Choose the "alabaster" theme, not the classic one

### Peewee Async
- https://peewee-async.readthedocs.io/en/latest/
- https://github.com/05bit/peewee-async
- Choose the "alabaster" theme, not the classic one

### Pipenv
- https://pipenv.readthedocs.io/en/latest/
- theme: alabaster
- `pip install -r ./docs/requirements.txt`
- Remove decorations
    - `div.section > h1 + img`
    - `div.section > h1 ~ a.image-reference`
- Enable javascript for vimeo video
- ~~Incorrect build: `install.html`~~ (Fix them manually)
    - Caused by "Title underline too short."

### Pygal
- http://www.pygal.org/en/2.4.0/
- Change theme as alabaster
- `make watch`
- Build docset with JavaScript enabled

### PyJWT
- https://pyjwt.readthedocs.io/en/latest/
- Use alabaster as the default theme

### PyMongo
- https://api.mongodb.com/python/3.8.0/
- https://github.com/mongodb/mongo-python-driver/

`conf.py` option doesn't work for theme `pydoctheme`, enable custom css file,

```html
html_css_files = ["custom.css"]
```

Override font family and text color. Remove left padding for `div.body`.

```css
div.footer {width:auto; max-width:none;} div.document {max-width:none; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} div.bodywrapper {margin: 0 0 0 0px;}
div.body {max-width:none !important; padding-left:0px;}

pre {padding: 7px 10px !important;margin: 15px 0 !important;overflow:auto;}
div.admonition {margin:20px 0; padding:10px 10px;}

body, div.body {font-family: 'Gentium Book Basic',Georgia,'Bitstream Charter','Hiragino Mincho Pro',serif;font-size: 1.0625rem;line-height:1.4;color:#3E4349;}
div.admonition p.admonition-title {font-family: 'Garamond','Georgia','Bitstream Charter',serif;}
pre, tt, code {font-family: Monaco,Consolas,Menlo,'Deja Vu Sans Mono','Bitstream Vera Sans Mono',monospace;font-size: 0.8em!important;}
h1, h2, h3, h4, h5, h6 {font-family: Garamond,Georgia,'Bitstream Charter',serif !important;font-weight:normal;}
```

### PyQuery
- https://pyquery.readthedocs.io/en/latest/
- `native` theme. Only two options are available:
    - `nosidebar`
    - `sidebarwidth`
- `html_css_files = ["custom.css"]`
- Remove badges `a.image-reference` in `index.html`
- Disable javascript since there's a ajax request for mathjax

### pysheeet, Cheatsheet of Python
- https://www.pythonsheets.com/
- Increase max depth for toc in `docs/index.rst`: `:maxdepth: 2`.
- Put custom style in `style.css`
- Display toc `div#table-of-contents {display: block;}`. Cause sidebar is removed, we need toc for navigation.

### Pytest
- https://docs.pytest.org/en/4.6.3/
- Based on flask theme, no useful options for docset generation
- Maybe it's a good idea to use theme `alabaster` since those two are very similar

### Requests
- http://docs.python-requests.org/en/master/
- remove badges: `find("body div h1").siblings().filter("a")`
- remove decorative images: `body div h1 + img`

### Requests-HTML
- https://html.python-requests.org/
- remove badges

### Requests-OAuthlib
- https://requests-oauthlib.readthedocs.io/en/latest/
- `pip install requests-oauthlib`

### Requests-Toolbelt
- https://toolbelt.readthedocs.io/en/latest/
- override theme sphinx_rtd_theme with alabaster

### Sanic
- https://sanic.readthedocs.io/en/latest/
- https://github.com/huge-success/sanic
- `pip install -e . ".[docs]"`

### Sanic JWT
- Use the new default theme alabaster but not the classic
- https://sanic-jwt.readthedocs.io/en/latest/
- https://github.com/ahopkins/sanic-jwt
- Remove badges on `index.html`

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

### Supervisor
- http://supervisord.org/
- Change theme as alabaster
- Disable `html_style` in `conf.py`
- `python2 setup.py develop`

### WeasyPrint
- https://weasyprint.readthedocs.io/en/v51/
- https://github.com/Kozea/WeasyPrint

### Werkzeug
- http://werkzeug.pocoo.org/docs/0.14/
- The theme of it is based on alabaster, but there's no `html_theme_options` support. Append custom styles into `html/_static/werkzeug.css`.

### WTForms
- https://wtforms.readthedocs.io/en/stable/
- Custom CSS is used by the doc. Change the `main.css` directly.

```css
/* additional */
#body {
    margin: auto;
    max-width: none;
}
```

### urllib3
- https://urllib3.readthedocs.io/en/latest/
- theme: alabaster
- `pip install mock pyopenssl pysocks`
