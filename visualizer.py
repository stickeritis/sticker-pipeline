import sys
from optparse import OptionParser

from PyQt5.QtCore import Qt, QEventLoop, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

from ud import sentencesToUD
from visualizer_window import Ui_VisualizerWindow

header = '''
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


conllu = '''
# sentence-label A
# visual-style 1	bgColor:blue
# visual-style 1	fgColor:white
# visual-style 2 1 nsubj	color:blue
# visual-style 4 1 nsubj	labelArrow:triangle,10,3
1	They	they	PRON	PRN	Case=Nom|Num=Plur	2	nsubj	4:nsubj	_
2	buy	buy	VERB	VBP	Num=Plur|Per=3|Tense=Pres	0	root	_	_
3	and	and	CONJ	CC	_	2	cc	_	_
4	sell	sell	VERB	VBP	Num=Plur|Per=3|Tense=Pres	2	conj	_	_
5	books	book	NOUN	NNS	Num=Plur	2	dobj	4:dobj	_
6	.	.	PUNCT	.	_	2	punct	_	_
'''

footer = '''
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

def print_signal(obj):
    print(obj)

class WebEngine(QWebEngineView):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

class Visualizer:
    def __init__(self):
        self._event_loop = QEventLoop()

    def displaySentence(self, sentence):
        self.displaySentences([sentence])

    def displaySentences(self, sentencesUD):
        self._engine = WebEngine()
        self.engine.closed.connect(self.event_loop.quit)
        self.engine.setHtml(header + sentencesUD + footer)
        self.engine.show()
        self.event_loop.exec_()

    @property
    def app(self):
        return self._app

    @property
    def engine(self):
        return self._engine

    @property
    def event_loop(self):
        return self._event_loop

class VisualizerWindow(QMainWindow):
    def __init__(self, pipeline):
        super(VisualizerWindow, self).__init__()
        self._pipeline = pipeline
        self.ui = Ui_VisualizerWindow()
        self.ui.setupUi(self)
        self.ui.processButton.clicked.connect(self.processClicked)

    def processClicked(self):
        self.processSentences(self.ui.inputTextEdit.toPlainText())

    def processSentences(self, text):
        sentences = self.pipeline.annotate_text(text)
        ud = sentencesToUD(sentences)
        self.ui.annotationsWebView.setHtml(header + ud + footer)

    @property
    def pipeline(self):
        return self._pipeline
