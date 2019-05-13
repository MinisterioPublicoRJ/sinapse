from flask_assets import Bundle, Environment
from sinapse.buildup import app


bundles = {

    'js': Bundle(
        'js/vendor/jquery-3.4.0.min.js',
        'js/vendor/vis.min.js',
        'js/vendor/bootstrap.min.js',
    ),
    'css': Bundle(
        'css/vendor/bootstrap.min.css',
        # Font Awesome não pode ficar em 'vendor/'
        # porque se referencia às fontes como '../fonts/'
        'css/font-awesome.min.css',
        'css/vendor/vis.min.css',
        'css/main.css',
        'css/busca.css',
        'css/login.css',
        'css/sidebarRight.css',
        'css/graph.css',
        'css/filter.css',
        'css/entitylist.css',
        'css/colors.css',
    ),
}


assets = Environment(app)

assets.register(bundles)
