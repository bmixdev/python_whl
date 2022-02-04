from prompt_toolkit.shortcuts import ProgressBar
import time
import threading
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts.progress_bar import formatters


title = HTML('Downloading <style bg="yellow" fg="black">4 files...</style>')

style = Style.from_dict({
    'label': 'bg:#ffff00 #000000',
    'percentage': 'bg:#ffff00 #000000',
    'current': '#448844',
    'bar': '',
})


custom_formatters = [
    formatters.Label(),
    formatters.Text(': [', style='class:percentage'),
    formatters.Percentage(),
    formatters.Text(']', style='class:percentage'),
    formatters.Text(' '),
    formatters.Bar(sym_a='=', sym_b='>', sym_c='.'),
    formatters.Text('  '),
    formatters.Progress(),
    formatters.Text(" "),
    formatters.Text("осталось [", style="class:time-left"),
    formatters.TimeLeft(),
    formatters.Text("]", style="class:time-left"),
    formatters.Text(" ")
]

with ProgressBar(style=style, formatters=custom_formatters) as pb:
    # Two parallel tasks.
    def task_1():
        label = HTML('<ansired>Task1</ansired>: ')            
        for i in pb(range(100), label=label):
            time.sleep(.05)

    def task_2():
        for i in pb(range(150)):
            time.sleep(.08)

    def task_3():
        for i in pb(range(200)):
            time.sleep(1)


    # Start threads.
    t1 = threading.Thread(target=task_1)
    t2 = threading.Thread(target=task_2)
    t3 = threading.Thread(target=task_3)
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    t3.start()

    # Wait for the threads to finish. We use a timeout for the join() call,
    # because on Windows, join cannot be interrupted by Control-C or any other
    # signal.
    for t in [t1, t2, t3]:
        while t.is_alive():
            t.join(timeout=.5)