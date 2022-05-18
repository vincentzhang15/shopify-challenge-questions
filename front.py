from flask import render_template

def front_page(template, items=[], error="", title="", info=""):
    return render_template(template + '.html', items=items, error=error, title=title, info=info)
