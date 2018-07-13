from flask_assets import Bundle, Environment
from sinapse.buildup import app


bundles = {

    'js': Bundle(
        'js/d3.min.js',
        'js/neo4jd3.js',
        'js/main.js',
    ),
    'css': Bundle(
        "css/bootstrap.min.css",
        "css/font-awesome.min.css",
        "css/neo4jd3.min.css",
        "css/main.css",
        "css/sidebarRight.css",
    ),
}


assets = Environment(app)

assets.register(bundles)
