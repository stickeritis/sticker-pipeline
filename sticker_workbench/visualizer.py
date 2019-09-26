from PyQt5.QtCore import QEventLoop, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView

CONLLU_JS_HEADER = '''
<head>
    <meta charset="utf-8">
    <title>Dependency tree visualization</title>
    <meta name="viewport" content="width=device-width">

    <link rel="stylesheet" href="http://spyysalo.github.io/conllu.js/css/jquery-ui-redmond.css">
    <link rel="stylesheet" href="http://spyysalo.github.io/conllu.js/css/main.css">
    <link rel="stylesheet" href="http://spyysalo.github.io/conllu.js/css/style-vis.css">

    <script type="text/javascript" src="http://spyysalo.github.io/conllu.js/lib/ext/head.load.min.js"></script>
</head>

<body>
  <div class="page-content">
    <div class="wrap">
      <div class="entry">


<article class="entry-content">
<code class="conllu-parse" tabs="yes"><pre>
'''

CONLLU_JS_FOOTER = '''
</pre></code>

</body>

<script type="text/javascript">
    var root = 'http://spyysalo.github.io/conllu.js/'; // filled in by jekyll
    head.js(
        // External libraries
        root + 'lib/ext/jquery.min.js',
        root + 'lib/ext/jquery.svg.min.js',
        root + 'lib/ext/jquery.svgdom.min.js',
        root + 'lib/ext/jquery-ui.min.js',
        root + 'lib/ext/waypoints.min.js',

        // brat helper modules
        root + 'lib/brat/configuration.js',
        root + 'lib/brat/util.js',
        root + 'lib/brat/annotation_log.js',
        root + 'lib/ext/webfont.js',
        // brat modules
        root + 'lib/brat/dispatcher.js',
        root + 'lib/brat/url_monitor.js',
        root + 'lib/brat/visualizer.js',

        // annotation documentation support
        'http://spyysalo.github.io/annodoc/lib/local/annodoc.js',
        root + 'lib/local/config.js',

        // the conllu.js library itself
        root + 'conllu.js'
    );

    var webFontURLs = [
        root + 'static/fonts/PT_Sans-Caption-Web-Regular.ttf',
        root + 'static/fonts/Liberation_Sans-Regular.ttf'
    ];

    /* not used here */
    var documentCollections = {};

    head.ready(function() {
        // performes all embedding and support functions
        Annodoc.activate(Config.bratCollData, documentCollections);
    });
</script>

</html>
'''


class WebEngine(QWebEngineView):
    """
    A small wrapper around QWebEngine that sends the 'closed' signal
    when the view is closed.
    """

    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        # Override close events to send a signal.
        self.closed.emit()
        event.accept()


class Visualizer:
    """
    CoNLL-U visualizer
    """

    def __init__(self):
        self._event_loop = QEventLoop()
        self._engine = WebEngine()
        self.engine.closed.connect(self.event_loop.quit)
        self.engine.resizeEvent = self.resized
        self.engine.setHtml("")

    def stop(self):
        """
        Stop the visualizer's event loop.
        """
        self.event_loop.exit(0)

    def run(self):
        """
        Start the visualizer's event loop.
        """
        self.engine.show()
        self.event_loop.exec_()

    def resized(self, size):
        # Reload the page when the veiw is resized.
        self.engine.reload()

    def setSentences(self, ud):
        """
        Change the sentences that are visualized, the method
        should be provided with well-formed UD.
        """
        self.engine.setHtml(CONLLU_JS_HEADER + ud + CONLLU_JS_FOOTER)

    @property
    def engine(self):
        return self._engine

    @property
    def event_loop(self):
        return self._event_loop
