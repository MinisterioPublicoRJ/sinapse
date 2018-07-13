from flask_assets import Bundle, Environment
from sinapse.buildup import app


bundles = {

    'js': Bundle(
        'js/vendor/d3.min.js',
        'js/vendor/neo4jd3.min.js',
        'js/main.js',
    ),
    'css': Bundle(
        'css/vendor/neo4jd3.min.css',
        'css/main.css',
        'css/busca.css',
    ),
}


assets = Environment(app)

assets.register(bundles)
