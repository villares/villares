<!--**username/username** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.-->
<img src="hello.gif">

> This animation is made with points in a Python collections.deque data structure, added by dragging the mouse (code shown bellow)
- 🔭 I'm currently working on a PhD at Unicamp
- 🌱 I should be talking less and concentrating
- 👯 I’m looking to collaborate on open resources to teach programming in a visual context
- 💬 Ask me about drawing with Python! 
    - Check out [py5](https://py5.ixora.io), it brings in the Processing drawing infrastructure!
- 📫 How to reach me: [twitter.com/villares](https://twitter.com/villares)
    - If you think the things that I share are usefull, consider donating at [ko-fi.com/villares](https://ko-fi.com/villares)
- 😄 Pronouns: he/him
- ⚡ Fun fact: I actually use this repo to store some helper [code](https://github.com/villares/villares) I use in my drawings.

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
