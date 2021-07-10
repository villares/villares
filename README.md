<!--**username/username** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.-->
### Hi there 👋

<img src="https://abav.lugaralgum.com/sketch-a-day/2020/sketch_2020_09_17deque/sketch_2020_09_17deque.gif">

> This animation is made with points in a Python collections.deque data structure, added by dragging the mouse in Processing Python mode (code shown bellow)
- 🔭 I'm currently working on a PhD at Unicamp
- 🌱 I’m currently learning how not to talk too much and concentrate
- 👯 I’m looking to collaborate on open resources to teach programming in a visual context
- 💬 Ask me about drawing with Python!
- 📫 How to reach me: [twitter.com/villares](https://twitter.com/villares)
- 😄 Pronouns: he/him
- ⚡ Fun fact: I think I actually need a repo named *villares* to store some [code](https://github.com/villares/villares).

```python
from collections import deque

h = deque([(0, 0)], 300) # mouse drag position history

def setup():
    size(500, 500)
    noStroke()
    colorMode(HSB)

def draw():
    background(51)
    for i, (x, y) in enumerate(h):
        fill(i, 255, 255, 255 / 2)
        circle(x, y, i / 5)
    h.append(h.popleft())

def mouseDragged():
    h.append((mouseX, mouseY))
```
