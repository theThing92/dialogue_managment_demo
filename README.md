# Dialogue Managment Demo
Das vorliegende Git-Repository enthält den Beispiel-Code für das Sitzungsreferat zum Thema ***Implementing Dialog Managment*** vom 09.01.2020 im Hauptseminar "Dialogsysteme" (WS 2019/2020).

## Frameworks
**Hinweis:** Alle gelisteten Frameworks sind für Python geschrieben im Hintergrund wird daraus jedoch - aus Performanzgründen - meist C-Code kompiliert (z.B. mit Cython).
- [Natural Language Toolkit (NLTK) (v3.4.5)](https://www.nltk.org/)
  - Sammlung verschiedener Funktionalitäten und Korpora zur computerlinguistischen Sprachverarbeitung. Enthält leider meist 'nur' ältere Verfahren, allerdings m.E. nach sehr gute Funktionaltiäten für Vorverarbeitung (z.B. Stemming, Tokenisierung, N-Gramm-Erstellung etc.). 
- [Jupyter (v1.0.0)](https://jupyter.org/)
  - Ermöglicht zellenweise Ausführung von Python-Code in Form eines sogenannten Notebooks. Eignet sich inbesondere für didaktische Präsentation von Programmiercode sowie schnelles Prototyping.
- [Scikit-Learn (v0.21.3)](https://scikit-learn.org/stable/)
  - Framework mit Implementationen der gängigsten Machine-Learning Algorithmen (nicht nur NLP). Leichter Zugriff auf Modelle durch einheitliche API.
- [Pandas (v0.25.3)](https://pandas.pydata.org/)
  - Framework zum tabellarischen Einlesen und Verarbeiten von Daten, vergleichbar mit Dataframes in R.
  
## Installation
- [**Python 3.6 installieren**](https://www.python.org/downloads/)<br> 
**Hinweis:**<br>
Getestet mit Python 3.6.8.<br>
Flair benötigt notwendigerweise Python 3.6+, die anderen Teile des Tutorials *könnten* aber auch älteren Python-Versionen laufen (**nicht getestet, keine Garantie**).

- [**Virtuelle Laufzeitumgebung für Python einrichten**](https://docs.python.org/3/tutorial/venv.html)<br>
Kommandozeile öffnen, dann folgende Befehle eingeben: 

```
# Wechsel in das Verzeichnis der Demo
cd path/to/repo/word_embeddings_demo
```

**Linux/Mac**
```
python3 -m venv venv
```
**Windows**
```
py -m venv venv
```

Anschließend muss die virtuelle Umgebung aktiviert werden (in derselben Kommandozeile):

**Linux/Mac**
```
source venv/bin/activate
```
**Windows**
```
venv\Scripts\activate
```

In der Kommandozeile sollte nun ein (venv) vor dem Prompt erscheinen.<br>
Anschließend können innerhalb dieser virtuellen Umgebung alle benötigten Software-Abhängigkeiten für die Demo installiert werden.

```
# Installation der Pakete
pip install -r requirements.txt
```
**Hinweis:**<br>

## Starten der Demo

- Jupyter-Notebook-Server starten<br>

**Linux/Mac**
```
jupyter notebook
```
**Windows**
```
venv\Scripts\jupyter-notebook.exe
```
- Öffnen des Jupyter-Notebooks im Browser (sollte automatisch geschehen)
```
# Folgenden Link öffnen:
http://localhost:8888/tree
```
Anschließend kann die Datei **dialog_managment_demo.ipynb** geöffnet werden. Die Demo kann dann zellenweise ausgeführt werden.
