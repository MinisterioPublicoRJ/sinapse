from flask_assets import Bundle, Environment
from sinapse.buildup import app


bundles = {

    'js': Bundle(
        'js/vendor/d3.min.js',
        'js/vendor/force-graph-d3-wrapper.js',
        'js/main.js',
    ),
    'css': Bundle(
        'css/vendor/bootstrap.min.css',
        # Font Awesome não pode ficar em 'vendor/'
        # porque se referencia às fontes como '../fonts/'
        'css/font-awesome.min.css',
        'css/vendor/force-graph-d3-wrapper.css',
        'css/main.css',
        'css/busca.css',
        'css/login.css',
        'css/sidebarRight.css',
        'css/graph.css',
    ),
}


assets = Environment(app)

assets.register(bundles)
