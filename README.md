<!--**username/username** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.-->
<img src="hello.gif">

> This animation is made with points in a Python collections.deque data structure, added by dragging the mouse (code shown bellow)
- 🔭 I'm currently working on a PhD at Unicamp
- 🌱 I should be talking less and concentrating, but...
- 💬 Ask me about drawing with Python! 
    - Check out [py5](https://py5coding.org) and [pyp5js](berinhard.github.io/pyp5js/pyodide/), they bring the Processing drawing infrastructure to Python!
- 👯 I’m looking to collaborate on open resources to teach programming in a visual context
    - If you find the things I share here usefull, consider supporting my work at [gumroad.com/villares](https://gumroad.com/villares), sending a donation [via PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=HCGAKACDMVNV2), or if you are in Brazil, mande um PIX:`46c37783-5edb-4f1c-b3a8-1309db11488c`!!!
- 📫 How to reach me: [Mastodon](ciberlandia.pt/@villares) or [Email](https://abav.lugaralgum.com/contato)
- 😄 Pronouns: he/him
- ⚡ Fun fact: I actually use this repo to store some helper [code](https://github.com/villares/villares) I use in my drawings.
    - I try to make a new drawing with code everyday, and I put the results at  [skech-a-day](https://abav.lugaralgum.com/sketch-a-day)

```python
from collections import deque  # a double-ended queue
import py5  # check out https://github.com/py5coding 

history = deque(maxlen=512)  # mouse dragged positions

def setup():   # py5 will call this once to set things up
    py5.size(600, 400)
    py5.no_stroke()
    py5.color_mode(py5.HSB)

def draw():   # py5 will call this in a loop
    py5.background(51)
    for i, (x, y) in enumerate(history):
        py5.fill(i / 2, 255, 255, 128)
        py5.circle(x, y, 8 + i / 16)
    if history:
        history.append(history.popleft())

def mouse_dragged():  # py5 will call this when you drag the mouse
    history.append((py5.mouse_x, py5.mouse_y))
    
def key_pressed():   # py5 will call this when a key is pressed
    history.clear()

py5.run_sketch()
```
