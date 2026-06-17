# -*- coding: utf-8 -*-
"""GeoFlash generator -> writes GeoFlash.html (single-file, no build)."""
import math, json

# ---------- tiny SVG DSL ----------
def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r*math.cos(a), cy - r*math.sin(a))

def ang_of(cx, cy, px, py):
    return math.degrees(math.atan2(cy - py, px - cx))

def f(n):
    return f"{n:.1f}".rstrip('0').rstrip('.')

def line(x1, y1, x2, y2, cls="fl"):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="{cls}"/>'

def polyline(pts, cls="fl", closed=False):
    d = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts) + (" Z" if closed else "")
    return f'<path d="{d}" class="{cls}"/>'

def circ(cx, cy, r, cls="fl"):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" class="{cls}"/>'

def dot(x, y, cls="fp"):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="3.1" class="{cls}"/>'

def txt(x, y, s, cls="flbl", anchor="middle"):
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}" text-anchor="{anchor}">{s}</text>'

def arc2(cx, cy, r, a1, a2, cls="fa"):
    d = ((a2 - a1 + 180) % 360) - 180
    n = max(2, int(abs(d)//6) + 2)
    pts = [pol(cx, cy, r, a1 + d*i/n) for i in range(n+1)]
    dd = "M " + " L ".join(f"{f(x)} {f(y)}" for x, y in pts)
    return f'<path d="{dd}" class="{cls}"/>'

def alabel(cx, cy, r, a1, a2, s, cls="flbl"):
    d = ((a2 - a1 + 180) % 360) - 180
    x, y = pol(cx, cy, r, a1 + d/2)
    return txt(x, y+5, s, cls)

def rightangle(cx, cy, a1, a2, s=13):
    p1 = pol(cx, cy, s, a1); p2 = pol(cx, cy, s, a2)
    c = (p1[0] + p2[0] - cx, p1[1] + p2[1] - cy)
    return f'<path d="M {f(p1[0])} {f(p1[1])} L {f(c[0])} {f(c[1])} L {f(p2[0])} {f(p2[1])}" class="fl thin"/>'

def tickmark(x1, y1, x2, y2):
    mx, my = (x1+x2)/2, (y1+y2)/2
    dx, dy = x2-x1, y2-y1
    L = math.hypot(dx, dy) or 1
    px, py = -dy/L, dx/L
    return line(mx-px*5, my-py*5, mx+px*5, my+py*5, "fl thin")

def chevron(x, y, deg=0, s=6):
    a = math.radians(deg)
    p  = (x + s*math.cos(a), y - s*math.sin(a))
    t1 = (x - s*math.cos(a-0.6), y + s*math.sin(a-0.6))
    t2 = (x - s*math.cos(a+0.6), y + s*math.sin(a+0.6))
    return f'<path d="M {f(t1[0])} {f(t1[1])} L {f(p[0])} {f(p[1])} L {f(t2[0])} {f(t2[1])}" class="fl thin"/>'

def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(d) < 1e-9:
        return ((x1+x3)/2, (y1+y3)/2)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / d
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))

def wrap(inner):
    return ('<svg viewBox="0 0 320 220" class="figsvg" '
            'preserveAspectRatio="xMidYMid meet" aria-hidden="true">' + inner + '</svg>')

cards = []
def add(topic, q, options, answer, sol, tip, t, fig):
    cards.append({"topic": topic, "q": q, "options": options, "answer": answer,
                  "sol": sol, "tip": tip, "t": t, "fig": wrap(fig)})

# ---- 1. Complementarios ----
V = (70, 178)
fig = (line(*V, *pol(*V, 200, 0)) + line(*V, *pol(*V, 145, 90)) + line(*V, *pol(*V, 165, 33))
       + rightangle(*V, 0, 90, 15)
       + arc2(*V, 52, 0, 33, "fau") + alabel(*V, 36, 0, 33, "x", "fu")
       + arc2(*V, 82, 33, 90, "fa") + alabel(*V, 64, 33, 90, "2x", "fg")
       + dot(*V))
add("Ángulos", "Dos ángulos forman un ángulo recto. Si uno es el doble del otro, halla x.",
    ["30°", "45°", "20°", "60°"], "30°",
    "Complementarios: x + 2x = 90° ⇒ 3x = 90° ⇒ x = 30°.",
    "Si dos ángulos forman un ángulo recto, son complementarios: suman 90°.", 18, fig)

# ---- 2. Suplementarios en recta ----
V = (165, 152)
fig = (line(40, 152, 290, 152) + line(*V, *pol(*V, 108, 62))
       + arc2(*V, 40, 0, 62, "fa") + alabel(*V, 56, 0, 62, "3x", "fg")
       + arc2(*V, 40, 62, 180, "fa") + alabel(*V, 58, 62, 180, "2x", "fg")
       + dot(*V))
add("Ángulos", "Halla el valor de x.",
    ["36°", "30°", "45°", "40°"], "36°",
    "Sobre una recta: 3x + 2x = 180° ⇒ 5x = 180° ⇒ x = 36°.",
    "Ángulos sobre una línea recta (par lineal) suman 180°.", 18, fig)

# ---- 3. Opuestos por el vértice ----
C = (160, 112)
A1 = ang_of(*C, 262, 56); A2 = ang_of(*C, 58, 56)
B1 = ang_of(*C, 262, 168); B2 = ang_of(*C, 58, 168)
fig = (line(58, 56, 262, 168) + line(58, 168, 262, 56)
       + arc2(*C, 32, A1, A2, "fa") + alabel(*C, 50, A1, A2, "70°", "fg")
       + arc2(*C, 32, B2, B1, "fau") + alabel(*C, 50, B2, B1, "x", "fu")
       + dot(*C))
add("Ángulos", "Dos rectas se cortan. Halla x.",
    ["70°", "110°", "35°", "140°"], "70°",
    "Ángulos opuestos por el vértice son iguales ⇒ x = 70°.",
    "Cuando dos rectas se cortan, los ángulos opuestos por el vértice son iguales.", 16, fig)

# ---- 4. Alrededor de un punto ----
V = (165, 120)
fig = (line(*V, *pol(*V, 95, 0)) + line(*V, *pol(*V, 95, 150)) + line(*V, *pol(*V, 95, 270))
       + arc2(*V, 28, 0, 150, "fa") + alabel(*V, 50, 0, 150, "150°", "fg")
       + arc2(*V, 28, 150, 270, "fa") + alabel(*V, 50, 150, 270, "120°", "fg")
       + arc2(*V, 28, 270, 360, "fau") + alabel(*V, 50, 270, 360, "x", "fu")
       + dot(*V))
add("Ángulos", "Halla x alrededor del punto.",
    ["90°", "80°", "100°", "120°"], "90°",
    "Vuelta completa: 150° + 120° + x = 360° ⇒ x = 90°.",
    "Los ángulos alrededor de un punto suman 360°.", 18, fig)

# ---- 5. Alternos internos ----
P1 = (124, 70); P2 = (211, 160)
fig = (line(40, 70, 286, 70) + line(40, 160, 286, 160) + line(95, 40, 245, 196)
       + chevron(250, 70) + chevron(250, 160)
       + arc2(*P1, 22, -46, 0, "fa") + alabel(*P1, 40, -46, 0, "65°", "fg")
       + arc2(*P2, 22, 134, 180, "fau") + alabel(*P2, 40, 134, 180, "x", "fu")
       + dot(*P1) + dot(*P2)
       + txt(34, 66, "L₁", "fsm", "end") + txt(34, 156, "L₂", "fsm", "end"))
add("Paralelas", "L₁ ∥ L₂. Halla x.",
    ["65°", "115°", "32.5°", "130°"], "65°",
    "Alternos internos entre paralelas son iguales ⇒ x = 65°.",
    "Entre paralelas, los ángulos alternos internos son iguales. Busca la “Z”.", 18, fig)

# ---- 6. Conjugados internos ----
fig = (line(40, 70, 286, 70) + line(40, 160, 286, 160) + line(95, 40, 245, 196)
       + chevron(250, 70) + chevron(250, 160)
       + arc2(*P1, 22, -46, 0, "fa") + alabel(*P1, 40, -46, 0, "110°", "fg")
       + arc2(*P2, 24, 0, 134, "fau") + alabel(*P2, 44, 0, 134, "x", "fu")
       + dot(*P1) + dot(*P2)
       + txt(34, 66, "L₁", "fsm", "end") + txt(34, 156, "L₂", "fsm", "end"))
add("Paralelas", "L₁ ∥ L₂. Halla x.",
    ["70°", "110°", "90°", "80°"], "70°",
    "Conjugados (co-laterales) internos suman 180° ⇒ x = 180° − 110° = 70°.",
    "Entre paralelas, los conjugados internos suman 180°. Busca la “C” o “U”.", 20, fig)

# ---- 7. Serrucho ----
A = (120, 60); M = (180, 112); B = (135, 170)
fig = (line(40, 60, 280, 60) + line(40, 170, 280, 170) + line(*A, *M) + line(*M, *B)
       + chevron(252, 60) + chevron(252, 170)
       + arc2(*A, 20, -41, 0, "fa") + alabel(*A, 36, -41, 0, "40°", "fg")
       + arc2(*B, 20, 0, 52, "fa") + alabel(*B, 36, 0, 52, "30°", "fg")
       + arc2(*M, 22, 139, 232, "fau") + alabel(*M, 40, 139, 232, "x", "fu")
       + dot(*A) + dot(*M) + dot(*B))
add("Paralelas", "L₁ ∥ L₂ (serrucho). Halla x.",
    ["70°", "80°", "10°", "110°"], "70°",
    "Propiedad del serrucho: el ángulo del medio = suma de los extremos ⇒ x = 40° + 30° = 70°.",
    "Serrucho entre paralelas: el ángulo central = suma de los dos exteriores. Traza una paralela auxiliar.", 22, fig)

# ---- 8. Suma de interiores ----
A = (60, 180); B = (260, 180); C = (150, 55)
fig = (polyline([A, B, C], closed=True)
       + arc2(*A, 24, 0, 54, "fa") + alabel(*A, 40, 0, 54, "50°", "fg")
       + arc2(*B, 24, 131, 180, "fa") + alabel(*B, 42, 131, 180, "60°", "fg")
       + arc2(*C, 22, 234, 311, "fau") + alabel(*C, 40, 234, 311, "x", "fu"))
add("Triángulos", "Halla el ángulo x del triángulo.",
    ["70°", "80°", "60°", "110°"], "70°",
    "Interiores de un triángulo: 50° + 60° + x = 180° ⇒ x = 70°.",
    "Los tres ángulos interiores de un triángulo suman 180°.", 16, fig)

# ---- 9. Ángulo exterior ----
A = (55, 165); B = (215, 165); C = (120, 55); D = (292, 165)
fig = (polyline([A, C, B], closed=True) + line(*B, *D)
       + arc2(*A, 22, 0, 59, "fa") + alabel(*A, 38, 0, 59, "40°", "fg")
       + arc2(*C, 20, 239, 311, "fa") + alabel(*C, 36, 239, 311, "70°", "fg")
       + arc2(*B, 22, 0, 131, "fau") + alabel(*B, 40, 0, 131, "x", "fu")
       + dot(*B))
add("Triángulos", "Halla el ángulo exterior x.",
    ["110°", "70°", "40°", "140°"], "110°",
    "Ángulo exterior = suma de los dos interiores no adyacentes ⇒ x = 40° + 70° = 110°.",
    "El ángulo exterior de un triángulo = suma de los dos ángulos interiores no contiguos.", 18, fig)

# ---- 10. Isósceles ----
A = (160, 50); B = (85, 180); C = (235, 180)
fig = (polyline([A, B, C], closed=True) + tickmark(*A, *B) + tickmark(*A, *C)
       + arc2(*B, 22, 0, 60, "fa") + alabel(*B, 38, 0, 60, "70°", "fg")
       + arc2(*A, 22, 240, 300, "fau") + alabel(*A, 40, 240, 300, "x", "fu"))
add("Triángulos", "Triángulo isósceles (AB = AC). Halla x.",
    ["40°", "70°", "55°", "110°"], "40°",
    "Base: 70° y 70°. Vértice: x = 180° − 140° = 40°.",
    "En un isósceles, a lados iguales se oponen ángulos iguales (los de la base).", 20, fig)

# ---- 11. Notable 45-45-90 ----
A = (95, 65); C = (95, 170); B = (205, 170)
fig = (polyline([A, C, B], closed=True) + rightangle(*C, 0, 90, 14)
       + arc2(*A, 24, 270, 316, "fa") + alabel(*A, 38, 270, 316, "45°", "fg")
       + txt(80, 122, "5", "fg", "end") + txt(150, 190, "5", "fg")
       + txt(162, 108, "x", "fu"))
add("Notables", "Triángulo 45°-45°-90°. Halla la hipotenusa x.",
    ["5√2", "10", "5", "5√3"], "5√2",
    "45-45-90: hipotenusa = cateto·√2 ⇒ x = 5√2.",
    "Notable 45-45-90: catetos iguales; hipotenusa = cateto × √2.", 18, fig)

# ---- 12. Notable 30-60-90 ----
B = (95, 70); C = (95, 170); A = (245, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 90, 180, 14)
       + arc2(*A, 26, 146, 180, "fa") + alabel(*A, 42, 146, 180, "30°", "fg")
       + txt(178, 114, "8", "fg") + txt(80, 124, "x", "fu", "end"))
add("Notables", "Triángulo 30°-60°-90°. Halla x (lado opuesto a 30°).",
    ["4", "4√3", "8", "2"], "4",
    "30-60-90 → lados 1 : √3 : 2. El lado opuesto a 30° es la mitad de la hipotenusa ⇒ x = 8/2 = 4.",
    "Notable 30-60-90: lados 1 : √3 : 2. El cateto frente a 30° = mitad de la hipotenusa.", 18, fig)

# ---- 13. Pitágoras 3-4-5 ----
B = (100, 80); C = (100, 170); A = (230, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 13)
       + txt(86, 128, "3", "fg", "end") + txt(165, 190, "4", "fg") + txt(178, 112, "x", "fu"))
add("Pitágoras", "Halla la hipotenusa x.",
    ["5", "7", "6", "5√2"], "5",
    "Terna pitagórica 3-4-5 ⇒ x = 5. (También 3²+4² = 9+16 = 25 = 5².)",
    "Memoriza las ternas: 3-4-5, 6-8-10, 9-12-15…", 16, fig)

# ---- 14. Terna 5-12-13 ----
B = (90, 108); C = (90, 168); A = (252, 168)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 12)
       + txt(78, 142, "5", "fg", "end") + txt(170, 188, "12", "fg") + txt(180, 122, "x", "fu"))
add("Pitágoras", "Halla la hipotenusa x.",
    ["13", "17", "12", "11"], "13",
    "Terna 5-12-13 ⇒ x = 13.",
    "Otras ternas clave: 5-12-13, 8-15-17, 7-24-25, 20-21-29.", 16, fig)

# ---- 15. Notable 37-53 ----
B = (100, 80); C = (100, 170); A = (235, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 13)
       + arc2(*A, 26, 146, 180, "fa") + alabel(*A, 42, 146, 180, "53°", "fg")
       + txt(176, 116, "10", "fg") + txt(82, 128, "x", "fu", "end"))
add("Notables", "Triángulo 37°-53°. Halla x (lado opuesto a 53°).",
    ["8", "6", "10", "5"], "8",
    "37-53 → lados 3 : 4 : 5. Frente a 53° va el 4 ⇒ x = (4/5)·10 = 8.",
    "Notable 37-53: lados 3, 4, 5. Frente a 37°→3k, frente a 53°→4k, hipotenusa 5k.", 20, fig)

# ---- 16. Mediana a la hipotenusa ----
A = (60, 170); B = (260, 170); C = (125, 70); M = (160, 170)
dCA = ang_of(*C, *A); dCB = ang_of(*C, *B)
fig = (polyline([A, C, B], closed=True) + line(*C, *M, "fl dash")
       + rightangle(*C, dCA, dCB, 13)
       + dot(*M) + txt(160, 188, "M", "fsm")
       + txt(95, 188, "10", "fg") + txt(150, 118, "x", "fu"))
add("Líneas notables", "Triángulo rectángulo. CM es la mediana a la hipotenusa. Halla x.",
    ["5", "10", "2.5", "5√2"], "5",
    "La mediana relativa a la hipotenusa = mitad de la hipotenusa ⇒ x = 10/2 = 5.",
    "En todo triángulo rectángulo, la mediana a la hipotenusa mide la mitad de ésta (el punto medio es el circuncentro).", 20, fig)

# ---- 17. Bisectrices interiores ----
A = (160, 55); B = (75, 180); C = (245, 180); I = (160, 135)
fig = (polyline([A, B, C], closed=True) + line(*B, *I) + line(*C, *I)
       + arc2(*A, 22, 236, 304, "fa") + alabel(*A, 38, 236, 304, "40°", "fg")
       + arc2(*B, 15, 0, 27.9, "fa2") + arc2(*B, 15, 27.9, 55.8, "fa2")
       + arc2(*C, 15, 124, 152, "fa2") + arc2(*C, 15, 152, 180, "fa2")
       + arc2(*I, 20, 208, 332, "fau") + alabel(*I, 36, 208, 332, "x", "fu")
       + dot(*I) + txt(150, 132, "I", "fsm", "end"))
add("Líneas notables", "BI y CI son bisectrices interiores. Si Â = 40°, halla x = ∠BIC.",
    ["110°", "70°", "140°", "100°"], "110°",
    "Ángulo entre dos bisectrices interiores = 90° + (ángulo opuesto)/2 ⇒ x = 90° + 40°/2 = 110°.",
    "Bisectrices interiores desde B y C: el ángulo en el incentro = 90° + (Â)/2.", 22, fig)

# ---- 18. Suma interiores polígono ----
pts = [pol(160, 118, 80, 90 + 72*k) for k in range(5)]
av = ""
for v in pts:
    a0 = ang_of(*v, 160, 118)
    av += arc2(*v, 16, a0-30, a0+30, "fa2")
fig = (polyline(pts, closed=True) + av + txt(160, 124, "Σ = x", "fu"))
add("Polígonos", "¿Cuánto suman los ángulos interiores de un pentágono? (x)",
    ["540°", "360°", "720°", "450°"], "540°",
    "Suma de interiores = 180°(n − 2) = 180°·(5 − 2) = 540°.",
    "Suma de ángulos interiores de un polígono de n lados = 180°(n − 2).", 18, fig)

# ---- 19. Exterior polígono regular ----
pts = [pol(155, 118, 72, 60*k) for k in range(6)]
E = (2*pts[0][0]-pts[5][0], 2*pts[0][1]-pts[5][1])
dE = ang_of(*pts[0], *E); dN = ang_of(*pts[0], *pts[1])
fig = (polyline(pts, closed=True) + line(*pts[0], *E, "fl dash")
       + arc2(*pts[0], 20, dE, dN, "fau") + alabel(*pts[0], 36, dE, dN, "x", "fu"))
add("Polígonos", "Hexágono regular. Halla el ángulo exterior x.",
    ["60°", "120°", "45°", "72°"], "60°",
    "Exterior de un polígono regular = 360°/n = 360°/6 = 60°.",
    "Polígono regular: cada ángulo exterior = 360°/n; el interior = 180° − exterior.", 18, fig)

# ---- 20. Diagonales ----
pts = [pol(160, 118, 75, 60*k) for k in range(6)]
diag = ""
for i in range(6):
    for j in range(i+1, 6):
        if (j-i) % 6 not in (1, 5):
            diag += line(*pts[i], *pts[j], "fl2")
fig = polyline(pts, closed=True) + diag + txt(160, 124, "x = ?", "fu")
add("Polígonos", "¿Cuántas diagonales tiene un hexágono? (x)",
    ["9", "12", "6", "15"], "9",
    "Diagonales = n(n − 3)/2 = 6·3/2 = 9.",
    "Número de diagonales de un polígono = n(n − 3)/2.", 18, fig)

# ---- 21. Ángulo central ----
O = (160, 115); A = pol(*O, 75, 60); B = pol(*O, 75, -12)
fig = (circ(*O, 75) + line(*O, *A) + line(*O, *B)
       + arc2(*O, 78, -12, 60, "fhi")
       + arc2(*O, 26, -12, 60, "fau") + alabel(*O, 44, -12, 60, "x", "fu")
       + alabel(*O, 96, -12, 60, "110°", "fg")
       + dot(*O) + txt(150, 122, "O", "fsm", "end")
       + txt(A[0]+10, A[1]-2, "A", "fsm") + txt(B[0]+10, B[1]+8, "B", "fsm"))
add("Circunferencia", "El arco AB mide 110°. Halla el ángulo central x = ∠AOB.",
    ["110°", "55°", "220°", "70°"], "110°",
    "El ángulo central mide igual que el arco que abarca ⇒ x = 110°.",
    "Ángulo central = arco que abarca.", 16, fig)

# ---- 22. Ángulo inscrito ----
O = (160, 115); P = pol(*O, 75, 90); A = pol(*O, 75, 205); B = pol(*O, 75, -25)
dPA = ang_of(*P, *A); dPB = ang_of(*P, *B)
fig = (circ(*O, 75) + line(*P, *A) + line(*P, *B)
       + arc2(*O, 78, 205, 335, "fhi") + alabel(*O, 96, 205, 335, "80°", "fg")
       + arc2(*P, 24, dPA, dPB, "fau") + alabel(*P, 40, dPA, dPB, "x", "fu")
       + dot(*P) + txt(P[0], P[1]-8, "P", "fsm"))
add("Circunferencia", "El arco AB mide 80°. Halla el ángulo inscrito x.",
    ["40°", "80°", "20°", "160°"], "40°",
    "Ángulo inscrito = mitad del arco que abarca ⇒ x = 80°/2 = 40°.",
    "Ángulo inscrito = mitad del arco (o mitad del ángulo central que abarca el mismo arco).", 18, fig)

# ---- 23. Inscrito en semicircunferencia (Thales) ----
O = (160, 120); A = (82, 120); B = (238, 120); C = pol(*O, 78, 68)
dCA = ang_of(*C, *A); dCB = ang_of(*C, *B)
fig = (circ(*O, 78) + line(*A, *B, "fl dash") + line(*A, *C) + line(*B, *C)
       + arc2(*C, 24, dCA, dCB, "fau") + alabel(*C, 40, dCA, dCB, "x", "fu")
       + dot(*A) + dot(*B) + dot(*C) + dot(*O)
       + txt(A[0]-4, A[1]+16, "A", "fsm") + txt(B[0]+4, B[1]+16, "B", "fsm")
       + txt(C[0], C[1]-8, "C", "fsm") + txt(O[0], O[1]+16, "O", "fsm"))
add("Circunferencia", "AB es diámetro. Halla x = ∠ACB.",
    ["90°", "45°", "60°", "180°"], "90°",
    "Todo ángulo inscrito que abarca un diámetro es recto ⇒ x = 90° (Teorema de Thales).",
    "Si el ángulo inscrito abarca un diámetro, mide 90°. Teorema de Thales.", 16, fig)

# ---- 24. Ángulo semiinscrito ----
O = (160, 102); T = (160, 174); A = pol(*O, 72, 40)
dTA = ang_of(*T, *A)
fig = (circ(*O, 72) + line(40, 174, 280, 174) + line(*T, *A)
       + arc2(*O, 76, -90, 40, "fhi") + alabel(*O, 95, -90, 40, "120°", "fg")
       + arc2(*T, 26, 0, dTA, "fau") + alabel(*T, 42, 0, dTA, "x", "fu")
       + dot(*T) + txt(T[0]-6, T[1]+16, "T", "fsm"))
add("Circunferencia", "Ángulo semiinscrito (tangente y cuerda). El arco mide 120°. Halla x.",
    ["60°", "120°", "30°", "90°"], "60°",
    "Ángulo semiinscrito = mitad del arco que encierra ⇒ x = 120°/2 = 60°.",
    "Ángulo semiinscrito (entre tangente y cuerda) = mitad del arco que encierra.", 20, fig)

# ---- 25. Ángulo interior (dos cuerdas) ----
O = (160, 115)
A = pol(*O, 78, 158); Cc = pol(*O, 78, -12); B = pol(*O, 78, 72); D = pol(*O, 78, 212)
X = inter(A, Cc, B, D)
dXA = ang_of(*X, *A); dXB = ang_of(*X, *B)
fig = (circ(*O, 78) + line(*A, *Cc) + line(*B, *D)
       + arc2(*O, 82, 72, 158, "fhi") + alabel(*O, 96, 72, 158, "80°", "fg")
       + arc2(*O, 82, 212, 348, "fhi") + alabel(*O, 96, 212, 348, "40°", "fg")
       + arc2(*X, 18, dXB, dXA, "fau") + alabel(*X, 34, dXB, dXA, "x", "fu")
       + dot(*X))
add("Circunferencia", "Dos cuerdas se cortan dentro. Halla x.",
    ["60°", "120°", "20°", "40°"], "60°",
    "Ángulo interior = semisuma de los arcos opuestos ⇒ x = (80° + 40°)/2 = 60°.",
    "Dos cuerdas que se cortan dentro: ángulo = semisuma de los dos arcos opuestos.", 22, fig)

# ---- 26. Ángulo exterior (dos secantes) ----
O = (215, 115); E = (45, 115)
fig = (circ(*O, 60) + line(45, 115, 286, 78) + line(45, 115, 286, 152)
       + arc2(*O, 64, 158, 202, "fhi") + alabel(*O, 48, 158, 202, "30°", "fg")
       + arc2(*O, 64, -22, 22, "fhi") + alabel(*O, 82, -22, 22, "100°", "fg")
       + arc2(*E, 30, -8.8, 8.8, "fau") + alabel(*E, 46, -8.8, 8.8, "x", "fu")
       + dot(*E) + txt(E[0]-6, E[1]+5, "E", "fsm", "end"))
add("Circunferencia", "Dos secantes desde un punto exterior. Halla x.",
    ["35°", "65°", "70°", "130°"], "35°",
    "Ángulo exterior = semidiferencia de los arcos ⇒ x = (100° − 30°)/2 = 35°.",
    "Desde un punto exterior (secantes/tangentes): ángulo = semidiferencia de los arcos que abarca.", 22, fig)

# ---- 27. Tangentes desde un punto exterior ----
O = (215, 115); P = (50, 115)
aa = math.degrees(math.acos(58/165))
T1 = pol(*O, 58, 180+aa); T2 = pol(*O, 58, 180-aa)
fig = (circ(*O, 58) + line(*P, *T1) + line(*P, *T2)
       + line(*O, *T1, "fl2") + line(*O, *T2, "fl2")
       + rightangle(*T2, ang_of(*T2, *O), ang_of(*T2, *P), 10)
       + rightangle(*T1, ang_of(*T1, *O), ang_of(*T1, *P), 10)
       + txt((P[0]+T2[0])/2 - 4, (P[1]+T2[1])/2 - 6, "8", "fg")
       + txt((P[0]+T1[0])/2 - 4, (P[1]+T1[1])/2 + 14, "x", "fu")
       + dot(*P) + txt(P[0]-6, P[1]+5, "P", "fsm", "end"))
add("Circunferencia", "PA y PB son tangentes a la circunferencia. Si PA = 8, halla x = PB.",
    ["8", "16", "4", "6"], "8",
    "Las dos tangentes desde un mismo punto exterior son iguales ⇒ x = 8.",
    "Las dos tangentes trazadas desde un mismo punto exterior son congruentes.", 18, fig)

# ---- 28. Área de triángulo ----
A = (70, 175); B = (250, 175); C = (150, 60)
fig = (polyline([A, B, C], closed=True) + line(150, 60, 150, 175, "fl dash")
       + rightangle(150, 175, 0, 90, 11)
       + txt(160, 193, "10", "fg") + txt(136, 122, "6", "fu", "end"))
add("Áreas", "Halla el área del triángulo (base 10, altura 6).",
    ["30", "60", "16", "15"], "30",
    "Área = base × altura / 2 = 10 × 6 / 2 = 30.",
    "Área de un triángulo = (base × altura)/2. La altura es perpendicular a la base.", 18, fig)

# ---- 29. Área de círculo ----
O = (160, 112); R = pol(*O, 72, 35)
fig = (circ(*O, 72) + line(*O, *R, "fl") + dot(*O)
       + txt((O[0]+R[0])/2, (O[1]+R[1])/2 - 6, "4", "fg")
       + txt(O[0], O[1]+22, "A = ?", "fu"))
add("Áreas", "Halla el área del círculo (radio 4).",
    ["16π", "8π", "4π", "16"], "16π",
    "Área = πr² = π·4² = 16π.",
    "Círculo: área = πr², longitud = 2πr. No confundas radio con diámetro.", 18, fig)

# ---- 30. Área de triángulo equilátero ----
A = (160, 55); B = (80, 185); C = (240, 185)
fig = (polyline([A, B, C], closed=True)
       + tickmark(*A, *B) + tickmark(*B, *C) + tickmark(*C, *A)
       + txt(106, 116, "4", "fg", "end") + txt(160, 203, "4", "fg")
       + txt(214, 116, "4", "fg") + txt(160, 150, "x", "fu"))
add("Áreas", "Triángulo equilátero de lado 4. Halla su área x.",
    ["4√3", "16√3", "8√3", "4"], "4√3",
    "Equilátero: área = (√3/4)·L² = (√3/4)·16 = 4√3.",
    "Equilátero de lado L: área = (√3/4)L²; altura = (√3/2)L.", 20, fig)

# ---- 31. Bisectriz ----
V = (72, 176)
fig = (line(*V, *pol(*V, 198, 0)) + line(*V, *pol(*V, 150, 80)) + line(*V, *pol(*V, 168, 40))
       + arc2(*V, 88, 0, 80, "fa") + alabel(*V, 104, 0, 80, "80°", "fg")
       + arc2(*V, 50, 0, 40, "fau") + alabel(*V, 34, 0, 40, "x", "fu")
       + arc2(*V, 50, 40, 80, "fa") + dot(*V))
add("Ángulos", "OM biseca el ángulo. Si el ángulo total mide 80°, halla x.",
    ["40°", "80°", "20°", "60°"], "40°",
    "La bisectriz divide el ángulo en dos partes iguales ⇒ x = 80°/2 = 40°.",
    "La bisectriz divide un ángulo en dos ángulos congruentes.", 14, fig)

# ---- 32. x, 2x, 3x en recta ----
V = (165, 152)
fig = (line(40, 152, 290, 152) + line(*V, *pol(*V, 108, 30)) + line(*V, *pol(*V, 108, 90))
       + arc2(*V, 38, 0, 30, "fau") + alabel(*V, 54, 0, 30, "x", "fu")
       + arc2(*V, 38, 30, 90, "fa") + alabel(*V, 56, 30, 90, "2x", "fg")
       + arc2(*V, 38, 90, 180, "fa") + alabel(*V, 58, 90, 180, "3x", "fg") + dot(*V))
add("Ángulos", "Tres ángulos consecutivos sobre una recta. Halla x.",
    ["30°", "20°", "36°", "45°"], "30°",
    "Sobre una recta: x + 2x + 3x = 180° ⇒ 6x = 180° ⇒ x = 30°.",
    "Los ángulos consecutivos sobre una línea recta suman 180°.", 18, fig)

# ---- 33. Correspondientes ----
P1 = (124, 70); P2 = (211, 160)
fig = (line(40, 70, 286, 70) + line(40, 160, 286, 160) + line(95, 40, 245, 196)
       + chevron(250, 70) + chevron(250, 160)
       + arc2(*P1, 22, 134, 180, "fa") + alabel(*P1, 40, 134, 180, "75°", "fg")
       + arc2(*P2, 22, 134, 180, "fau") + alabel(*P2, 40, 134, 180, "x", "fu")
       + dot(*P1) + dot(*P2)
       + txt(34, 66, "L₁", "fsm", "end") + txt(34, 156, "L₂", "fsm", "end"))
add("Paralelas", "L₁ ∥ L₂. Halla x.",
    ["75°", "105°", "37.5°", "115°"], "75°",
    "Ángulos correspondientes entre paralelas son iguales ⇒ x = 75°.",
    "Entre paralelas, los correspondientes (misma posición) son iguales. Busca la “F”.", 18, fig)

# ---- 34. Conjugados internos con álgebra ----
fig = (line(40, 70, 286, 70) + line(40, 160, 286, 160) + line(95, 40, 245, 196)
       + chevron(250, 70) + chevron(250, 160)
       + arc2(*P1, 22, -46, 0, "fa") + alabel(*P1, 44, -46, 0, "(x+20)°", "fg")
       + arc2(*P2, 26, 0, 134, "fau") + alabel(*P2, 50, 0, 134, "(2x+10)°", "fu")
       + dot(*P1) + dot(*P2)
       + txt(34, 66, "L₁", "fsm", "end") + txt(34, 156, "L₂", "fsm", "end"))
add("Paralelas", "L₁ ∥ L₂. Halla x.",
    ["50°", "40°", "30°", "60°"], "50°",
    "Conjugados internos suman 180°: (x+20) + (2x+10) = 180 ⇒ 3x + 30 = 180 ⇒ x = 50°.",
    "Conjugados internos entre paralelas suman 180°. Plantea la ecuación y despeja.", 24, fig)

# ---- 35. Rectángulo: agudos complementarios ----
C = (95, 170); B = (95, 75); A = (240, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 13)
       + arc2(*A, 26, 146, 180, "fa") + alabel(*A, 42, 146, 180, "35°", "fg")
       + arc2(*B, 24, 270, 327, "fau") + alabel(*B, 40, 270, 327, "x", "fu"))
add("Triángulos", "En el triángulo rectángulo, halla x.",
    ["55°", "45°", "35°", "65°"], "55°",
    "Los ángulos agudos de un triángulo rectángulo son complementarios ⇒ x = 90° − 35° = 55°.",
    "En todo triángulo rectángulo, los dos ángulos agudos suman 90°.", 16, fig)

# ---- 36. Equilátero 60° ----
A = (160, 55); B = (80, 185); C = (240, 185)
fig = (polyline([A, B, C], closed=True) + tickmark(*A, *B) + tickmark(*B, *C) + tickmark(*C, *A)
       + arc2(*B, 24, 0, 60, "fau") + alabel(*B, 40, 0, 60, "x", "fu")
       + arc2(*A, 22, 240, 300, "fa") + arc2(*C, 22, 120, 180, "fa"))
add("Triángulos", "Triángulo equilátero. Halla x.",
    ["60°", "45°", "90°", "30°"], "60°",
    "En un equilátero los tres ángulos son iguales ⇒ x = 180°/3 = 60°.",
    "Triángulo equilátero: tres lados iguales y tres ángulos de 60°.", 14, fig)

# ---- 37. Exterior (inverso) ----
A = (55, 165); B = (215, 165); C = (120, 55); D = (292, 165)
fig = (polyline([A, C, B], closed=True) + line(*B, *D)
       + arc2(*A, 22, 0, 59, "fa") + alabel(*A, 38, 0, 59, "65°", "fg")
       + arc2(*B, 22, 0, 131, "fa") + alabel(*B, 40, 0, 131, "115°", "fg")
       + arc2(*C, 20, 239, 311, "fau") + alabel(*C, 36, 239, 311, "x", "fu") + dot(*B))
add("Triángulos", "El ángulo exterior mide 115°. Halla x.",
    ["50°", "65°", "115°", "25°"], "50°",
    "Ángulo exterior = suma de los dos interiores no adyacentes ⇒ 115° = 65° + x ⇒ x = 50°.",
    "Usa el teorema del ángulo exterior al revés: exterior − un interior = el otro interior.", 18, fig)

# ---- 38. 30-60-90 (cateto mayor) ----
C = (95, 170); B = (95, 55); A = (235, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 13)
       + arc2(*A, 26, 146, 180, "fa") + alabel(*A, 42, 146, 180, "60°", "fg")
       + txt(176, 116, "12", "fg") + txt(80, 118, "x", "fu", "end"))
add("Notables", "Triángulo 30°-60°-90°. Halla x (lado opuesto a 60°).",
    ["6√3", "6", "12", "3√3"], "6√3",
    "30-60-90 → 1 : √3 : 2. Hipotenusa 12 ⇒ k = 6; lado opuesto a 60° = √3·k = 6√3.",
    "30-60-90: el lado opuesto a 60° = √3 × (mitad de la hipotenusa).", 20, fig)

# ---- 39. 45-45-90 (hip → cateto) ----
A = (95, 65); C = (95, 170); B = (205, 170)
fig = (polyline([A, C, B], closed=True) + rightangle(*C, 0, 90, 14)
       + txt(80, 122, "x", "fu", "end") + txt(165, 108, "10√2", "fg"))
add("Notables", "Triángulo 45°-45°-90°. La hipotenusa es 10√2. Halla el cateto x.",
    ["10", "10√2", "5√2", "20"], "10",
    "45-45-90: hipotenusa = cateto·√2 ⇒ 10√2 = x·√2 ⇒ x = 10.",
    "45-45-90: cateto = hipotenusa / √2.", 18, fig)

# ---- 40. Terna 8-15-17 ----
B = (90, 100); C = (90, 168); A = (252, 168)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 12)
       + txt(78, 138, "8", "fg", "end") + txt(170, 188, "15", "fg") + txt(182, 120, "x", "fu"))
add("Pitágoras", "Halla la hipotenusa x.",
    ["17", "18", "16", "19"], "17",
    "Terna 8-15-17 ⇒ x = 17. (8² + 15² = 64 + 225 = 289 = 17².)",
    "Ternas útiles: 8-15-17, 7-24-25, 20-21-29, 9-40-41.", 18, fig)

# ---- 41. Cateto faltante ----
B = (100, 80); C = (100, 170); A = (230, 170)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 13)
       + txt(86, 128, "6", "fg", "end") + txt(176, 112, "10", "fg") + txt(165, 190, "x", "fu"))
add("Pitágoras", "La hipotenusa mide 10 y un cateto 6. Halla el otro cateto x.",
    ["8", "4", "16", "2√34"], "8",
    "Pitágoras: x = √(10² − 6²) = √(100 − 36) = √64 = 8. (Es la terna 6-8-10.)",
    "Para un cateto: cateto = √(hipotenusa² − otro cateto²). Reconoce 6-8-10.", 18, fig)

# ---- 42. Baricentro 2:1 ----
A = (160, 52); B = (70, 185); C = (250, 185); M = (160, 185); G = (160, 140.7)
fig = (polyline([A, B, C], closed=True) + line(*A, *M)
       + dot(*M) + dot(*G)
       + txt(150, 100, "x", "fu", "end") + txt(176, 145, "G", "fsm") + txt(160, 201, "M", "fsm"))
add("Líneas notables", "G es el baricentro. La mediana AM mide 9. Halla AG = x.",
    ["6", "3", "4.5", "9"], "6",
    "El baricentro divide cada mediana en razón 2:1 desde el vértice ⇒ AG = (2/3)·9 = 6.",
    "El baricentro divide la mediana en 2:1: el tramo desde el vértice es el doble que el del lado.", 20, fig)

# ---- 43. Poncelet (inradio) ----
C = (95, 170); B = (95, 70); A = (225, 170); I = (113, 152)
fig = (polyline([B, C, A], closed=True) + rightangle(*C, 0, 90, 12) + circ(*I, 18, "fa")
       + txt(80, 124, "6", "fg", "end") + txt(160, 188, "8", "fg") + txt(172, 110, "10", "fg")
       + txt(I[0]+1, I[1]+5, "r", "fu"))
add("Líneas notables", "Triángulo rectángulo de catetos 6 y 8 (hipotenusa 10). Halla el inradio r.",
    ["2", "4", "3", "1"], "2",
    "Teorema de Poncelet / inradio: r = (cateto + cateto − hipotenusa)/2 = (6 + 8 − 10)/2 = 2.",
    "Triángulo rectángulo: inradio r = (a + b − c)/2 (catetos menos hipotenusa, entre 2).", 22, fig)

# ---- 44. Interior de hexágono regular ----
pts = [pol(160, 118, 75, 60*k) for k in range(6)]
v = pts[0]; dprev = ang_of(*v, *pts[5]); dnxt = ang_of(*v, *pts[1])
fig = (polyline(pts, closed=True)
       + arc2(*v, 20, dnxt, dprev, "fau") + alabel(*v, 38, dnxt, dprev, "x", "fu"))
add("Polígonos", "Hexágono regular. Halla un ángulo interior x.",
    ["120°", "108°", "135°", "144°"], "120°",
    "Interior de un polígono regular = 180° − 360°/n = 180° − 60° = 120°.",
    "Ángulo interior de un polígono regular = 180° − (360°/n).", 16, fig)

# ---- 45. Nº de lados dado el exterior ----
V = (160, 150); P1 = pol(*V, 85, 215); P2 = pol(*V, 85, 325); E = pol(*V, 52, 35)
fig = (line(*V, *P1) + line(*V, *P2) + line(*V, *E, "fl dash")
       + arc2(*V, 22, 325, 35, "fa") + alabel(*V, 40, 325, 35, "36°", "fg")
       + txt(160, 120, "n = ?", "fu")
       + dot(*P1) + dot(*P2)
       + txt(P1[0]-15, P1[1]+8, "···", "fsm") + txt(P2[0]+15, P2[1]+8, "···", "fsm"))
add("Polígonos", "El ángulo exterior de un polígono regular es 36°. ¿Cuántos lados tiene? (x)",
    ["10", "8", "9", "12"], "10",
    "Exterior = 360°/n ⇒ 36° = 360°/n ⇒ n = 10.",
    "Si conoces el ángulo exterior de un polígono regular: n = 360° / (ángulo exterior).", 18, fig)

# ---- 46. Inscritos sobre el mismo arco ----
O = (160, 116)
A = pol(*O, 76, 200); B = pol(*O, 76, -20); C = pol(*O, 76, 70); D = pol(*O, 76, 110)
fig = (circ(*O, 76) + line(*A, *C) + line(*B, *C) + line(*A, *D) + line(*B, *D)
       + arc2(*C, 22, ang_of(*C, *A), ang_of(*C, *B), "fa") + alabel(*C, 38, ang_of(*C, *A), ang_of(*C, *B), "35°", "fg")
       + arc2(*D, 22, ang_of(*D, *A), ang_of(*D, *B), "fau") + alabel(*D, 40, ang_of(*D, *A), ang_of(*D, *B), "x", "fu")
       + dot(*C) + dot(*D) + txt(C[0]+8, C[1]-6, "C", "fsm") + txt(D[0]-8, D[1]-6, "D", "fsm"))
add("Circunferencia", "Los ángulos inscritos abarcan el mismo arco AB. Halla x.",
    ["35°", "70°", "17.5°", "55°"], "35°",
    "Dos ángulos inscritos que abarcan el mismo arco son iguales ⇒ x = 35°.",
    "Ángulos inscritos que abarcan el mismo arco (misma cuerda, mismo lado) son iguales.", 18, fig)

# ---- 47. Cuadrilátero inscrito ----
O = (160, 115)
A = pol(*O, 78, 110); B = pol(*O, 78, 200); C = pol(*O, 78, 310); D = pol(*O, 78, 30)
fig = (circ(*O, 78) + polyline([A, B, C, D], closed=True)
       + arc2(*A, 20, ang_of(*A, *B), ang_of(*A, *D), "fa") + alabel(*A, 36, ang_of(*A, *B), ang_of(*A, *D), "95°", "fg")
       + arc2(*C, 20, ang_of(*C, *B), ang_of(*C, *D), "fau") + alabel(*C, 36, ang_of(*C, *B), ang_of(*C, *D), "x", "fu")
       + txt(A[0], A[1]-8, "A", "fsm") + txt(C[0], C[1]+15, "C", "fsm"))
add("Circunferencia", "ABCD está inscrito en la circunferencia. Si ∠A = 95°, halla ∠C = x.",
    ["85°", "95°", "105°", "180°"], "85°",
    "En un cuadrilátero inscrito, los ángulos opuestos son suplementarios ⇒ x = 180° − 95° = 85°.",
    "Cuadrilátero inscrito (cíclico): los ángulos opuestos suman 180°.", 20, fig)

# ---- 48. Pitot (circunscrito) ----
O = (160, 116)
verts = [(62, 70), (258, 70), (248, 182), (72, 182)]
fig = (circ(*O, 46, "fa") + polyline(verts, closed=True)
       + txt(160, 62, "5", "fg") + txt(258, 128, "7", "fg")
       + txt(160, 198, "4", "fg") + txt(60, 128, "x", "fu", "end"))
add("Circunferencia", "El cuadrilátero está circunscrito a la circunferencia. Halla x.",
    ["2", "6", "8", "16"], "2",
    "Teorema de Pitot: lados opuestos suman igual ⇒ 5 + 4 = 7 + x ⇒ x = 2.",
    "Cuadrilátero circunscrito (Pitot): la suma de un par de lados opuestos = la del otro par.", 22, fig)

# ---- 49. Tangente perpendicular al radio ----
O = (150, 112); T = pol(*O, 72, -22); tdir = -22 + 90
t1 = pol(*T, 72, tdir); t2 = pol(*T, 72, tdir + 180); dTO = ang_of(*T, *O)
fig = (circ(*O, 72) + line(*O, *T, "fl") + line(*t1, *t2, "fl")
       + rightangle(*T, dTO, tdir, 12)
       + arc2(*T, 28, dTO, tdir, "fau") + alabel(*T, 46, dTO, tdir, "x", "fu")
       + dot(*O) + txt(O[0], O[1]+16, "O", "fsm") + dot(*T) + txt(T[0]+10, T[1]+2, "T", "fsm"))
add("Circunferencia", "La recta es tangente en T. Halla x (ángulo entre el radio OT y la tangente).",
    ["90°", "45°", "180°", "60°"], "90°",
    "El radio trazado al punto de tangencia es perpendicular a la tangente ⇒ x = 90°.",
    "El radio en el punto de tangencia es siempre perpendicular (90°) a la tangente.", 14, fig)

# ---- 50. Potencia (cuerdas) ----
O = (160, 115)
A = pol(*O, 80, 160); B = pol(*O, 80, -15); C = pol(*O, 80, 55); D = pol(*O, 80, 250)
X = inter(A, B, C, D)
def mid(p, q): return ((p[0]+q[0])/2, (p[1]+q[1])/2)
mA = mid(A, X); mB = mid(B, X); mC = mid(C, X); mD = mid(D, X)
fig = (circ(*O, 80) + line(*A, *B) + line(*C, *D) + dot(*X)
       + txt(mA[0]-6, mA[1]-4, "4", "fg") + txt(mB[0]+6, mB[1], "6", "fg")
       + txt(mC[0]+8, mC[1]-2, "3", "fg") + txt(mD[0]-8, mD[1]+8, "x", "fu")
       + txt(X[0]+6, X[1]+13, "P", "fsm"))
add("Circunferencia", "Dos cuerdas se cortan en P. Halla x.",
    ["8", "12", "5", "9"], "8",
    "Potencia de un punto (cuerdas): AP·PB = CP·PD ⇒ 4·6 = 3·x ⇒ x = 8.",
    "Cuerdas que se cortan: AP·PB = CP·PD (producto de los segmentos de cada cuerda es igual).", 22, fig)

# ---- 51. Área del cuadrado ----
fig = (polyline([(95, 55), (225, 55), (225, 185), (95, 185)], closed=True)
       + txt(160, 47, "6", "fg") + txt(240, 124, "6", "fg"))
add("Áreas", "Halla el área del cuadrado de lado 6.",
    ["36", "24", "12", "18"], "36",
    "Área del cuadrado = lado² = 6² = 36.",
    "Cuadrado: área = L²; perímetro = 4L; diagonal = L√2.", 14, fig)

# ---- 52. Área del sector circular ----
O = (118, 158); r = 96
A = pol(*O, r, 0); B = pol(*O, r, 90)
fig = (line(*O, *A) + line(*O, *B) + arc2(*O, r, 0, 90, "fl")
       + arc2(*O, 26, 0, 90, "fau") + alabel(*O, 44, 0, 90, "90°", "fg")
       + txt((O[0]+A[0])/2, O[1]+16, "4", "fg") + dot(*O))
add("Áreas", "Sector circular de radio 4 y ángulo 90°. Halla su área x.",
    ["4π", "16π", "8π", "2π"], "4π",
    "Área del sector = (θ/360°)·πr² = (90/360)·π·4² = (1/4)·16π = 4π.",
    "Sector circular: área = (θ/360°)·πr² (la fracción del círculo que abarca el ángulo).", 20, fig)

# ---- 53. Área del trapecio ----
fig = (polyline([(75, 180), (245, 180), (195, 70), (110, 70)], closed=True)
       + line(150, 70, 150, 180, "fl dash") + rightangle(150, 180, 0, 90, 10)
       + txt(160, 198, "8", "fg") + txt(152, 62, "4", "fg") + txt(136, 130, "3", "fu", "end"))
add("Áreas", "Trapecio de bases 8 y 4, altura 3. Halla el área.",
    ["18", "24", "36", "12"], "18",
    "Área del trapecio = (B + b)/2 · h = (8 + 4)/2 · 3 = 6·3 = 18.",
    "Trapecio: área = (semisuma de las bases) × altura = ((B + b)/2)·h.", 20, fig)

# ---- 54. Área del rombo ----
A = (160, 55); C = (160, 181); B = (95, 118); D = (225, 118)
fig = (polyline([A, B, C, D], closed=True) + line(*A, *C, "fl dash") + line(*B, *D, "fl dash")
       + rightangle(160, 118, 0, 90, 10)
       + txt(172, 92, "6", "fg") + txt(128, 110, "8", "fg"))
add("Áreas", "Rombo de diagonales 6 y 8. Halla el área.",
    ["24", "48", "14", "12"], "24",
    "Área del rombo = (D · d)/2 = (8 · 6)/2 = 24.",
    "Rombo (o cuadrilátero de diagonales perpendiculares): área = (D · d)/2.", 18, fig)

# =====================================================================
# SOLUCIONARIO GRÁFICO (Semana 4 CEPRE PUCP)
# =====================================================================
SOL = []
def addsol(pid, topic, q, ans, res, clave, steps, fig):
    SOL.append({"pid": pid, "topic": topic, "q": q, "ans": ans, "res": res,
                "clave": clave, "steps": steps, "fig": wrap(fig)})

# --- P81: diagonales del endecágono ---
O = (160, 116); R = 92
pts = [pol(*O, R, 90 + 360/11*k) for k in range(11)]
dg = "".join(line(*pts[0], *pts[j], "fl2") for j in range(2, 10))
fig81 = polyline(pts, closed=True) + dg + dot(*pts[0]) + txt(160, 14, "endecágono · n = 11", "fsm")
addsol("P 81", "Polígonos — diagonales",
    "Halla el número total de diagonales de un endecágono.", "B) 44", "D = 44",
    "Diagonales totales = n(n−3)/2. Endecágono = 11 lados. Desde cada vértice salen (n−3) diagonales.",
    [{"t": "Usa la fórmula del número de diagonales.", "m": "D = n(n−3) / 2"},
     {"t": "El endecágono tiene 11 lados.", "m": "n = 11"},
     {"t": "Reemplaza y opera.", "m": "D = 11·(11−3)/2 = 11·8/2"}], fig81)

# --- P87: pentágono, suma de ángulos ---
O = (160, 122); R = 80
pts = [pol(*O, R, 90 + 72*k) for k in range(5)]
labels = [(90, "x+40°"), (162, "x+30°"), (234, "x+40°"), (306, "x+20°"), (18, "x+50°")]
lt = "".join(txt(pol(*O, R-27, a)[0], pol(*O, R-27, a)[1]+4, s, "fg") for a, s in labels)
fig87 = polyline(pts, closed=True) + lt
addsol("P 87", "Polígonos — ángulos internos",
    "En el pentágono, los ángulos miden x+30°, x+40°, x+50°, x+40° y x+20°. Halla x.",
    "D) 72°", "x = 72°",
    "Plantea: (suma de los ángulos dados) = 180°(n−2). Luego despeja x.",
    [{"t": "Suma de ángulos interiores de un polígono.", "m": "S = 180°(n−2)"},
     {"t": "Pentágono: n = 5.", "m": "S = 180°·3 = 540°"},
     {"t": "Suma las 5 expresiones de la figura.", "m": "5x + (30+40+50+40+20) = 5x + 180"},
     {"t": "Iguala a 540° y despeja.", "m": "5x + 180 = 540 → 5x = 360"}], fig87)

# --- P85: hexágono, diagonal AC ---
O = (160, 120); R = 82
verts = [pol(*O, R, a) for a in (150, 90, 30, -30, -90, -150)]
A_, B_, C_ = verts[0], verts[1], verts[2]
fig85 = (polyline(verts, closed=True)
    + polyline([A_, B_, C_], cls="ff", closed=True)
    + line(*A_, *C_, "fhi")
    + arc2(*B_, 20, ang_of(*B_, *A_), ang_of(*B_, *C_), "fau")
    + alabel(*B_, 38, ang_of(*B_, *A_), ang_of(*B_, *C_), "120°", "fu")
    + txt(mid(A_, B_)[0]-9, mid(A_, B_)[1]-3, "L", "fg")
    + txt(mid(B_, C_)[0]+9, mid(B_, C_)[1]-3, "L", "fg")
    + txt(mid(A_, C_)[0], mid(A_, C_)[1]+19, "4√3", "fu")
    + txt(A_[0]-11, A_[1]+2, "A", "fsm") + txt(B_[0], B_[1]-9, "B", "fsm") + txt(C_[0]+11, C_[1]+2, "C", "fsm"))
addsol("P 85", "Hexágono regular",
    "En un hexágono regular ABCDEF, la diagonal AC mide 4√3 m. Halla el perímetro.",
    "A) 24 m", "P = 24 m",
    "Hexágono regular: diagonal menor = L·√3; diagonal mayor (AD) = 2L.",
    [{"t": "AC salta el vértice B: triángulo isósceles ABC con ∠B = 120°.", "m": "AB = BC = L"},
     {"t": "Esa es la diagonal menor del hexágono.", "m": "AC = L·√3"},
     {"t": "Iguala al dato y despeja L.", "m": "L√3 = 4√3 → L = 4"},
     {"t": "El perímetro son 6 lados.", "m": "P = 6·L = 6·4"}], fig85)

# --- P88: 20 diagonales -> ángulo interior ---
O = (160, 116); R = 84
pts = [pol(*O, R, 22.5 + 45*k) for k in range(8)]
v = pts[0]
fig88 = (polyline(pts, closed=True)
    + arc2(*v, 20, ang_of(*v, *pts[1]), ang_of(*v, *pts[7]), "fau")
    + alabel(*v, 38, ang_of(*v, *pts[1]), ang_of(*v, *pts[7]), "135°", "fu")
    + txt(160, 120, "n = 8", "fsm"))
addsol("P 88", "Polígonos — dos pasos",
    "Un polígono regular tiene 20 diagonales. Halla la medida de un ángulo interior.",
    "D) 135°", "i = 135°",
    "Primero halla n con las diagonales; luego interior = 180°(n−2)/n.",
    [{"t": "De las diagonales, despeja el número de lados.", "m": "n(n−3)/2 = 20 → n(n−3) = 40"},
     {"t": "Por tanteo: 8·5 = 40.", "m": "n = 8  (octágono)"},
     {"t": "Ángulo interior de un polígono regular.", "m": "i = 180°(n−2)/n = 180·6/8"}], fig88)

# --- P90: cuadrado inscrito en circunferencia ---
O = (160, 116); R = 80
sq = [pol(*O, R, a) for a in (45, 135, 225, 315)]
fig90 = (circ(*O, R) + polyline(sq, closed=True)
    + line(*sq[0], *sq[2], "fhi") + dot(*O)
    + txt(mid(sq[0], sq[2])[0]+4, mid(sq[0], sq[2])[1]-7, "8√2", "fu")
    + txt(160, sq[1][1]-9, "L", "fg"))
addsol("P 90", "Circunferencia + cuadrado",
    "El diámetro de una circunferencia mide 8√2 m. Halla el área del cuadrado inscrito.",
    "B) 64 m²", "A = 64 m²",
    "Cuadrado inscrito: su diagonal = diámetro. Y la diagonal de un cuadrado = L·√2.",
    [{"t": "La diagonal del cuadrado inscrito coincide con el diámetro.", "m": "d = 8√2"},
     {"t": "Diagonal de un cuadrado en función del lado.", "m": "d = L·√2"},
     {"t": "Iguala y despeja L.", "m": "L√2 = 8√2 → L = 8"},
     {"t": "Área del cuadrado.", "m": "A = L² = 8²"}], fig90)

# =====================================================================
HEAD = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>GeoFlash — Velocidad en Geometría</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --hue:168;
  --bg:#eef3f3;            --bg: oklch(0.965 0.006 200);
  --bg2:#ffffff;          --bg2: oklch(1 0 0);
  --panel:#ffffffb8;      --panel: oklch(1 0 0 / .70);
  --line:#dbe6e5;         --line: oklch(0.905 0.008 200);
  --fg:#10242b;           --fg: oklch(0.27 0.03 220);
  --muted:#5d7479;        --muted: oklch(0.52 0.02 215);
  --accent:#019877;       --accent: oklch(0.585 0.13 var(--hue));
  --accent-soft:#01987718;--accent-soft: oklch(0.585 0.13 var(--hue) / .11);
  --ok:#0c9c5f;           --ok: oklch(0.62 0.15 158);
  --bad:#d24a37;          --bad: oklch(0.58 0.18 28);
  --warn:#c4820e;         --warn: oklch(0.67 0.13 72);
  --fig:#33474e;          --fig: oklch(0.37 0.03 225);
  --fig-lbl:#16292f;      --fig-lbl: oklch(0.29 0.03 222);
  --radius:16px;
  --ease:cubic-bezier(.22,1,.36,1);
  --ease-out:cubic-bezier(.16,1,.3,1);
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{
  font-family:Inter,system-ui,-apple-system,sans-serif;
  background:var(--bg); color:var(--fg);
  min-height:100dvh; line-height:1.5; letter-spacing:-.01em;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
  background-image:
    radial-gradient(120% 85% at 50% -12%, color-mix(in oklch, var(--accent) 14%, transparent), transparent 55%),
    linear-gradient(180deg, #ffffff, var(--bg));
  background-attachment:fixed;
  overflow-x:hidden;
}
.wrap{max-width:680px;margin:0 auto;padding:clamp(14px,3vw,28px) clamp(14px,3.5vw,22px);min-height:100dvh;display:flex;flex-direction:column}
.mono{font-family:"Space Grotesk",Inter,sans-serif}
h1,h2,h3{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;letter-spacing:-.03em;text-wrap:balance}
.num{font-variant-numeric:tabular-nums}

.screen{display:none;flex:1;flex-direction:column;animation:screenIn .45s var(--ease) both}
.screen.active{display:flex}
@keyframes screenIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* ---------- START ---------- */
.brand{display:flex;align-items:center;gap:11px;margin-bottom:auto}
.logo{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;background:var(--accent-soft);border:1px solid color-mix(in oklch,var(--accent) 40%,transparent);box-shadow:0 0 24px -8px var(--accent)}
.logo svg{width:22px;height:22px}
.brand b{font-family:"Space Grotesk";font-size:1.05rem;letter-spacing:-.02em}
.brand span{color:var(--muted);font-size:.82rem}
.hero{padding:clamp(20px,6vh,52px) 0 8px}
.kicker{display:inline-flex;align-items:center;gap:7px;font-size:.74rem;text-transform:uppercase;letter-spacing:.16em;color:var(--accent);font-weight:600;margin-bottom:16px}
.kicker::before{content:"";width:22px;height:1px;background:var(--accent)}
.hero h1{font-size:clamp(2.1rem,8vw,3.4rem);line-height:1.02}
.hero h1 em{font-style:normal;color:var(--accent);text-shadow:0 0 40px color-mix(in oklch,var(--accent) 45%,transparent)}
.hero p{color:var(--muted);font-size:clamp(.97rem,2.4vw,1.08rem);max-width:46ch;margin-top:16px;text-wrap:pretty}

.controls{margin-top:30px;display:flex;flex-direction:column;gap:18px}
.field>label{display:block;font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:9px}
.segB{display:flex;gap:8px;flex-wrap:wrap}
.seg{flex:1;min-width:70px;font-family:"Space Grotesk";font-size:1rem;padding:13px 10px;border-radius:12px;border:1px solid var(--line);background:var(--bg2);color:var(--fg);cursor:pointer;transition:transform .12s var(--ease),border-color .18s,background .18s,color .18s}
.seg .num{font-size:1.3rem;display:block;line-height:1.1}
.seg small{color:var(--muted);font-size:.72rem;font-family:Inter}
.seg[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft);color:var(--fg)}
.seg[aria-pressed="true"] small{color:color-mix(in oklch,var(--accent) 80%,var(--fg))}
.seg:hover{border-color:color-mix(in oklch,var(--accent) 50%,var(--line))}
.seg:active{transform:scale(.97)}
.field-note{margin-top:11px;font-size:.79rem;color:var(--muted);display:flex;align-items:center;gap:8px}
.field-note b{color:var(--accent)}
.dotk{width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px var(--accent-soft);flex:none}

.cta{display:flex;gap:11px;align-items:center;margin-top:6px;flex-wrap:wrap}
.btn{font-family:"Space Grotesk";font-weight:600;font-size:1rem;border:1px solid var(--line);background:var(--bg2);color:var(--fg);padding:14px 20px;border-radius:13px;cursor:pointer;display:inline-flex;align-items:center;gap:9px;transition:transform .12s var(--ease),background .18s,border-color .18s,box-shadow .25s}
.btn:active{transform:scale(.97)}
.btn.primary{background:var(--accent);color:#062019;border-color:transparent;box-shadow:0 8px 30px -10px var(--accent)}
.btn.primary:hover{box-shadow:0 12px 38px -8px var(--accent);transform:translateY(-1px)}
.btn.ghost:hover{border-color:color-mix(in oklch,var(--accent) 45%,var(--line))}
.btn.big{flex:1;justify-content:center;padding:16px 22px;font-size:1.06rem}
.hint{margin-top:20px;color:var(--muted);font-size:.8rem;display:flex;gap:14px;flex-wrap:wrap}
.hint kbd{font-family:"Space Grotesk";background:var(--bg2);border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;padding:1px 7px;font-size:.74rem;color:var(--fg)}
.best{margin-top:22px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem;display:flex;justify-content:space-between;align-items:center}
.best b{color:var(--accent);font-family:"Space Grotesk";font-size:1.05rem}

/* ---------- HUD ---------- */
.hud{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:12px;margin-bottom:16px}
.hud-l{min-width:0}
.counter{font-family:"Space Grotesk";font-size:.85rem;color:var(--muted);margin-bottom:7px;display:block}
.counter b{color:var(--fg)}
.track{height:5px;border-radius:99px;background:var(--bg2);overflow:hidden}
.track i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,color-mix(in oklch,var(--accent) 60%,var(--bg)),var(--accent));transition:width .4s var(--ease)}
.chips{display:flex;gap:8px}
.chip{display:inline-flex;align-items:center;gap:6px;font-family:"Space Grotesk";font-size:.9rem;background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:6px 11px}
.chip b{font-variant-numeric:tabular-nums}
.chip.streak[data-on="1"]{border-color:color-mix(in oklch,var(--warn) 50%,var(--line));color:var(--warn)}
.hud-r{display:flex;align-items:center;gap:8px}
.ico{width:38px;height:38px;border-radius:10px;border:1px solid var(--line);background:var(--bg2);color:var(--muted);cursor:pointer;display:grid;place-items:center;font-size:1rem;transition:transform .12s var(--ease),color .18s,border-color .18s}
.ico:hover{color:var(--fg);border-color:color-mix(in oklch,var(--accent) 40%,var(--line))}
.ico:active{transform:scale(.92)}
.ring{position:relative;width:44px;height:44px;display:grid;place-items:center}
.ring svg{position:absolute;inset:0;transform:rotate(-90deg)}
.ring circle{fill:none;stroke-width:3.4}
.ring .bg{stroke:var(--line)}
.ring .fg{stroke:var(--accent);stroke-linecap:round;transition:stroke-dashoffset .25s linear,stroke .3s}
.ring b{font-family:"Space Grotesk";font-size:.78rem;font-variant-numeric:tabular-nums}

/* ---------- CARD ---------- */
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(15px,3vw,22px);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 18px 44px -30px color-mix(in oklch,var(--fg) 55%,transparent);display:flex;flex-direction:column}
.topic{display:inline-flex;align-self:flex-start;align-items:center;gap:7px;font-size:.72rem;text-transform:uppercase;letter-spacing:.13em;color:var(--accent);font-weight:600;margin-bottom:12px}
.topic::before{content:"◆";font-size:.6rem}
.figwrap{position:relative;background:
  linear-gradient(color-mix(in oklch,var(--line) 35%,transparent) 1px,transparent 1px) 0 0/22px 22px,
  linear-gradient(90deg,color-mix(in oklch,var(--line) 35%,transparent) 1px,transparent 1px) 0 0/22px 22px,
  radial-gradient(120% 120% at 50% 30%, var(--bg2), color-mix(in oklch,var(--bg) 70%,var(--bg2)));
  border:1px solid var(--line);border-radius:12px;padding:8px;margin-bottom:16px;overflow:hidden}
.figwrap::before,.figwrap::after{content:"";position:absolute;width:14px;height:14px;border:2px solid color-mix(in oklch,var(--accent) 55%,transparent);opacity:.6}
.figwrap::before{top:8px;left:8px;border-right:0;border-bottom:0;border-radius:4px 0 0 0}
.figwrap::after{bottom:8px;right:8px;border-left:0;border-top:0;border-radius:0 0 4px 0}
.figsvg{display:block;width:100%;height:auto;max-height:min(40vh,260px)}
/* figure primitives */
.fl{fill:none;stroke:var(--fig);stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round}
.fl.thin{stroke-width:1.5}
.fl.dash{stroke-dasharray:5 5;opacity:.7}
.fl2{fill:none;stroke:color-mix(in oklch,var(--fig) 45%,transparent);stroke-width:1.4}
.fa{fill:none;stroke:color-mix(in oklch,var(--fig) 75%,transparent);stroke-width:2;stroke-linecap:round}
.fa2{fill:none;stroke:color-mix(in oklch,var(--muted) 70%,transparent);stroke-width:1.5}
.fau{fill:none;stroke:var(--accent);stroke-width:2.6;stroke-linecap:round}
.fhi{fill:none;stroke:var(--accent);stroke-width:3.4;stroke-linecap:round;opacity:.9}
.fp{fill:var(--fig)}
.ff{fill:var(--accent-soft);stroke:none}
.flbl{fill:var(--fig-lbl);font:600 16px "Space Grotesk",sans-serif}
.fg{fill:var(--fig-lbl);font:600 17px "Space Grotesk",sans-serif}
.fu{fill:var(--accent);font:700 18px "Space Grotesk",sans-serif}
.fsm{fill:var(--muted);font:600 13px "Space Grotesk",sans-serif}
.question{font-family:"Space Grotesk";font-size:clamp(1.05rem,3vw,1.25rem);font-weight:600;line-height:1.32;margin-bottom:16px;text-wrap:pretty}

.options{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:430px){.options{grid-template-columns:1fr}}
.opt{position:relative;display:flex;align-items:center;gap:11px;text-align:left;font-family:"Space Grotesk";font-size:1.08rem;font-weight:600;padding:14px 15px;border-radius:12px;border:1px solid var(--line);background:var(--bg2);color:var(--fg);cursor:pointer;transition:transform .11s var(--ease),border-color .16s,background .16s}
.opt:hover:not(:disabled){border-color:color-mix(in oklch,var(--accent) 55%,var(--line));transform:translateY(-1px)}
.opt:active:not(:disabled){transform:scale(.98)}
.opt:disabled{cursor:default}
.opt .k{flex:none;width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-size:.82rem;background:color-mix(in oklch,var(--line) 60%,var(--bg2));color:var(--muted);transition:background .16s,color .16s}
.opt.correct{border-color:var(--ok);background:color-mix(in oklch,var(--ok) 16%,var(--bg2));color:var(--fg)}
.opt.correct .k{background:var(--ok);color:#04150d}
.opt.wrong{border-color:var(--bad);background:color-mix(in oklch,var(--bad) 14%,var(--bg2))}
.opt.wrong .k{background:var(--bad);color:#fff}
.opt .mark{margin-left:auto;font-size:1.05rem;opacity:0;transform:scale(.6);transition:opacity .2s var(--ease),transform .25s var(--ease)}
.opt.correct .mark,.opt.wrong .mark{opacity:1;transform:none}

/* ---------- FEEDBACK ---------- */
.feedback{margin-top:16px;border-top:1px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:12px}
.feedback[hidden]{display:none}
@starting-style{.feedback{opacity:0;transform:translateY(6px)}}
.feedback{animation:fbIn .32s var(--ease) both}
@keyframes fbIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.fb-head{display:flex;align-items:center;gap:10px;font-family:"Space Grotesk";font-weight:700;font-size:1.05rem}
.fb-mark{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;flex:none}
.fb-ok .fb-mark{background:var(--ok);color:#04150d}
.fb-bad .fb-mark{background:var(--bad);color:#fff}
.fb-ok .fb-head{color:var(--ok)} .fb-bad .fb-head{color:var(--bad)}
.fb-sol{font-size:.95rem;color:var(--fg)}
.fb-tip{display:flex;gap:11px;background:var(--accent-soft);border:1px solid color-mix(in oklch,var(--accent) 30%,transparent);border-radius:12px;padding:13px 14px}
.fb-tip .bulb{flex:none;font-size:1.05rem;line-height:1.4}
.fb-tip p{font-size:.92rem;color:color-mix(in oklch,var(--accent) 22%,var(--fg))}
.fb-tip b{color:var(--accent);text-transform:uppercase;font-size:.7rem;letter-spacing:.12em;display:block;margin-bottom:3px;font-family:"Space Grotesk"}

/* ---------- RESULTS ---------- */
.res-hero{text-align:center;padding:8px 0 18px}
.rating{font-family:"Space Grotesk";font-size:clamp(2rem,9vw,3rem);font-weight:700;line-height:1;color:var(--accent);text-shadow:0 0 50px color-mix(in oklch,var(--accent) 40%,transparent)}
.res-hero p{color:var(--muted);margin-top:8px}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:6px 0 18px}
.metric{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:15px 12px;text-align:center}
.metric .v{font-family:"Space Grotesk";font-size:clamp(1.4rem,5vw,1.9rem);font-weight:700;font-variant-numeric:tabular-nums;line-height:1}
.metric .l{color:var(--muted);font-size:.74rem;text-transform:uppercase;letter-spacing:.08em;margin-top:6px}
.section-t{font-family:"Space Grotesk";font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin:18px 0 11px;display:flex;align-items:center;gap:9px}
.section-t::after{content:"";flex:1;height:1px;background:var(--line)}
.tbar{display:flex;align-items:center;gap:11px;margin-bottom:9px}
.tbar .nm{width:108px;flex:none;font-size:.84rem;font-weight:500}
.tbar .bar{flex:1;height:8px;border-radius:99px;background:var(--bg2);overflow:hidden}
.tbar .bar i{display:block;height:100%;border-radius:99px;background:var(--accent);transition:width .7s var(--ease)}
.tbar .bar i.low{background:var(--bad)} .tbar .bar i.mid{background:var(--warn)}
.tbar .pc{width:42px;text-align:right;font-family:"Space Grotesk";font-size:.82rem;font-variant-numeric:tabular-nums;color:var(--muted)}
.miss{display:flex;flex-direction:column;gap:9px;margin-bottom:8px}
.missc{display:flex;gap:13px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:11px 13px}
.missc .mfig{width:62px;height:50px;flex:none;border-radius:8px;background:var(--bg2);border:1px solid var(--line);overflow:hidden;display:grid;place-items:center}
.missc .mfig svg{width:100%;height:100%}
.missc .mq{font-size:.86rem;line-height:1.3}
.missc .ma{font-size:.8rem;color:var(--accent);font-weight:600;margin-top:3px;font-family:"Space Grotesk"}
.empty-good{text-align:center;color:var(--ok);padding:6px 0 12px;font-weight:600}

/* ---------- SOLUCIONARIO ---------- */
.sol-top{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.sol-top h2{font-size:clamp(1.3rem,4.4vw,1.75rem)}
.sol-intro{color:var(--muted);font-size:.9rem;margin-bottom:18px;text-wrap:pretty}
.sol-card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(15px,3vw,20px);margin-bottom:16px;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 14px 40px -32px color-mix(in oklch,var(--fg) 55%,transparent);animation:screenIn .5s var(--ease) both}
.sol-head{display:flex;align-items:center;gap:10px;margin-bottom:11px;flex-wrap:wrap}
.sol-pid{font-family:"Space Grotesk";font-weight:700;font-size:.82rem;background:var(--fg);color:var(--bg2);padding:3px 10px;border-radius:7px}
.sol-topic{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:600}
.sol-ans{margin-left:auto;font-family:"Space Grotesk";font-weight:700;font-size:.85rem;color:var(--ok);background:color-mix(in oklch,var(--ok) 13%,transparent);border:1px solid color-mix(in oklch,var(--ok) 35%,transparent);padding:4px 11px;border-radius:9px}
.sol-q{font-size:.93rem;line-height:1.4;color:var(--fg);margin-bottom:14px;text-wrap:pretty}
.sol-fig{margin-bottom:15px}
.sol-fig .figsvg{max-height:min(38vh,232px)}
.sol-steps{display:flex;flex-direction:column;gap:12px}
.step{display:flex;gap:12px;align-items:flex-start}
.step .sn{flex:none;width:25px;height:25px;border-radius:50%;display:grid;place-items:center;font-family:"Space Grotesk";font-weight:700;font-size:.8rem;background:var(--accent-soft);color:var(--accent);border:1px solid color-mix(in oklch,var(--accent) 35%,transparent)}
.step .sb{display:flex;flex-direction:column;gap:6px;padding-top:2px;min-width:0}
.step .st{font-size:.9rem;line-height:1.35}
.step .sm{align-self:flex-start;max-width:100%;font-family:"Space Grotesk";font-weight:600;font-size:.95rem;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:9px;padding:6px 12px;font-variant-numeric:tabular-nums}
.sol-res{display:flex;align-items:center;gap:12px;margin-top:15px;background:var(--accent-soft);border:1px solid color-mix(in oklch,var(--accent) 35%,transparent);border-radius:12px;padding:11px 16px}
.sol-res span{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);font-weight:600;font-family:"Space Grotesk"}
.sol-res b{margin-left:auto;font-family:"Space Grotesk";font-size:1.28rem;color:var(--accent)}
.sol-clave{display:flex;gap:11px;margin-top:11px;border-top:1px solid var(--line);padding-top:12px}
.sol-clave .bulb{flex:none;font-size:1rem}
.sol-clave p{font-size:.86rem;color:var(--muted);text-wrap:pretty}
.sol-clave b{display:block;color:var(--fg);font-family:"Space Grotesk";font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px}

/* ---------- MODAL ---------- */
.modal{position:fixed;inset:0;z-index:30;display:none;background:color-mix(in oklch,#000 60%,transparent);backdrop-filter:blur(4px);padding:18px;overflow:auto}
.modal.open{display:grid;place-items:start center;animation:screenIn .3s var(--ease)}
.sheet{background:var(--bg2);border:1px solid var(--line);border-radius:18px;max-width:560px;width:100%;margin:max(20px,6vh) 0;padding:22px}
.sheet h2{font-size:1.3rem;margin-bottom:4px}
.sheet .sub{color:var(--muted);font-size:.86rem;margin-bottom:16px}
.cheat-i{display:flex;gap:12px;padding:11px 0;border-top:1px solid var(--line)}
.cheat-i .ci-t{flex:none;width:96px;font-family:"Space Grotesk";font-size:.78rem;color:var(--accent);font-weight:600;text-transform:uppercase;letter-spacing:.04em;padding-top:1px}
.cheat-i p{font-size:.88rem;color:var(--fg)}
.sheet .close{position:sticky;top:0;float:right;margin:-6px -6px 0 0}

/* ---------- PAUSE ---------- */
.pause{position:fixed;inset:0;z-index:25;display:none;place-items:center;background:color-mix(in oklch,var(--bg) 80%,transparent);backdrop-filter:blur(8px)}
.pause.open{display:grid;animation:screenIn .3s var(--ease)}
.pause .box{text-align:center}
.pause h2{font-size:1.8rem;margin-bottom:16px}

:focus-visible{outline:none;box-shadow:0 0 0 2px var(--bg),0 0 0 4px var(--accent);border-radius:10px}
.foot{margin-top:18px;text-align:center;color:var(--muted);font-size:.74rem;opacity:.7}
@media(prefers-reduced-motion:reduce){*{animation-duration:.001ms!important;transition-duration:.001ms!important}}
</style>
</head>
'''

BODY = r'''<body>
<div class="wrap">

  <!-- ============ START ============ -->
  <section id="start" class="screen active">
    <div class="brand">
      <span class="logo" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M3 20 L12 4 L21 20 Z" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13.5" r="2.4" fill="var(--accent)"/></svg></span>
      <div><b>GeoFlash</b><br><span>Entrenador de velocidad · Geometría</span></div>
    </div>

    <div class="hero">
      <span class="kicker">Criterio + velocidad</span>
      <h1>Domina las <em>bases</em><br>y resuelve a la <em>velocidad</em> del rayo.</h1>
      <p>30 casos gráficos esenciales en modo flash. Cada respuesta trae el criterio rápido para que reconozcas el patrón al instante y ataques cualquier problema complejo con seguridad.</p>
    </div>

    <div class="controls">
      <div class="field">
        <label>¿Cuántas preguntas?</label>
        <div class="segB" id="countSel" role="group" aria-label="Número de preguntas">
          <button class="seg" data-n="10" aria-pressed="false"><span class="num">10</span><small>rápido</small></button>
          <button class="seg" data-n="20" aria-pressed="false"><span class="num">20</span><small>medio</small></button>
          <button class="seg" data-n="30" aria-pressed="true"><span class="num">30</span><small>completo</small></button>
        </div>
        <p class="field-note"><span class="dotk"></span>Selección equilibrada por tema · <b id="poolN" class="num">54</b> casos disponibles</p>
      </div>
      <div class="cta">
        <button class="btn primary big" id="startBtn">▶ Empezar drill</button>
      </div>
      <div class="cta" style="margin-top:10px">
        <button class="btn ghost" id="cheatBtn" style="flex:1;justify-content:center">📋 Chuleta</button>
        <button class="btn ghost" id="solBtn" style="flex:1;justify-content:center">📐 Solucionario</button>
      </div>
      <div class="hint">
        <span><kbd>1</kbd>–<kbd>4</kbd> responder</span>
        <span><kbd>Espacio</kbd> siguiente</span>
        <span><kbd>Esc</kbd> pausa</span>
      </div>
    </div>

    <div class="best">
      <span>Tu mejor puntaje</span>
      <b id="bestScore" class="num">—</b>
    </div>
    <p class="foot">Hecho para Alejandro · GEN+ · 100% offline</p>
  </section>

  <!-- ============ GAME ============ -->
  <section id="game" class="screen">
    <header class="hud">
      <div class="hud-l">
        <span class="counter mono"><b id="counter" class="num">01</b> / <span id="total" class="num">30</span></span>
        <div class="track"><i id="bar"></i></div>
      </div>
      <div class="chips">
        <span class="chip streak" id="streakChip" data-on="0">🔥 <b id="streak" class="num">0</b></span>
        <span class="chip">★ <b id="score" class="num">0</b></span>
      </div>
      <div class="hud-r">
        <button class="ico" id="muteBtn" aria-label="Activar o silenciar sonido">🔊</button>
        <div class="ring" aria-hidden="true">
          <svg viewBox="0 0 44 44"><circle class="bg" cx="22" cy="22" r="18"/><circle class="fg" id="ringfg" cx="22" cy="22" r="18"/></svg>
          <b id="elapsed" class="num">0s</b>
        </div>
        <button class="ico" id="pauseBtn" aria-label="Pausar">⏸</button>
      </div>
    </header>

    <div class="card">
      <span class="topic" id="topic">Ángulos</span>
      <div class="figwrap"><div id="fig" role="img" aria-label=""></div></div>
      <p class="question" id="question"></p>
      <div class="options" id="options" role="group" aria-label="Opciones"></div>
      <div class="feedback" id="feedback" hidden>
        <div class="fb-head"><span class="fb-mark" id="fbMark"></span><span id="fbTitle"></span><span id="fbTime" style="margin-left:auto;font-size:.85rem;color:var(--muted);font-weight:500"></span></div>
        <p class="fb-sol" id="fbSol"></p>
        <div class="fb-tip"><span class="bulb">💡</span><p><b>Criterio rápido</b><span id="fbTip"></span></p></div>
        <button class="btn primary" id="nextBtn">Siguiente →</button>
      </div>
    </div>
    <p class="foot" id="gameHint">Toca una opción o usa <kbd style="font-family:Space Grotesk">1-4</kbd></p>
  </section>

  <!-- ============ RESULTS ============ -->
  <section id="results" class="screen">
    <div class="res-hero">
      <div class="rating" id="rating">Relámpago</div>
      <p id="ratingSub">Velocidad de élite</p>
    </div>
    <div class="metrics">
      <div class="metric"><div class="v" id="mAcc">—</div><div class="l">Aciertos</div></div>
      <div class="metric"><div class="v num" id="mSpeed">—</div><div class="l">seg/carta</div></div>
      <div class="metric"><div class="v num" id="mScore">—</div><div class="l">Puntaje</div></div>
    </div>
    <div class="section-t">Dominio por tema</div>
    <div id="topics"></div>
    <div class="section-t">Para reforzar</div>
    <div class="miss" id="missList"></div>
    <div class="cta" style="margin-top:14px">
      <button class="btn primary big" id="againBtn">↻ Jugar de nuevo</button>
      <button class="btn ghost" id="retryWrongBtn" hidden>Repasar falladas</button>
    </div>
    <p class="foot">GeoFlash · sigue practicando para subir tu velocidad</p>
  </section>

  <!-- ============ SOLUCIONARIO ============ -->
  <section id="solucionario" class="screen">
    <div class="sol-top">
      <button class="btn ghost" id="solBack" aria-label="Volver">←</button>
      <h2>Solucionario gráfico</h2>
    </div>
    <p class="sol-intro">5 problemas de geometría resueltos paso a paso — como en el examen. Fíjate en el patrón y la fórmula clave, no memorices el número.</p>
    <div id="solList"></div>
    <p class="foot">GeoFlash · Practiquemos Semana 4 · CEPRE PUCP</p>
  </section>

  <!-- Pause overlay -->
  <div class="pause" id="pauseOv"><div class="box"><h2>⏸ En pausa</h2><button class="btn primary" id="resumeBtn">Continuar</button></div></div>

  <!-- Cheat sheet -->
  <div class="modal" id="cheat"><div class="sheet">
    <button class="btn ghost close" id="cheatClose" aria-label="Cerrar">✕ Cerrar</button>
    <h2>Chuleta de criterios</h2>
    <p class="sub">Los atajos mentales de toda la geometría básica.</p>
    <div id="cheatList"></div>
  </div></div>

</div>
'''

JS = r'''<script>
const CARDS = __CARDS__;
const SOL = __SOL__;
const $ = s => document.querySelector(s);
const pad = n => (n<10?'0':'') + n;
const shuffle = a => { a = a.slice(); for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]];} return a; };
const LS = {
  get best(){ return +localStorage.getItem('gf_best') || 0; },
  set best(v){ localStorage.setItem('gf_best', v); },
  get muted(){ return localStorage.getItem('gf_muted') === '1'; },
  set muted(v){ localStorage.setItem('gf_muted', v ? '1' : '0'); }
};

/* ---------- audio ---------- */
let actx;
function beep(kind){
  if(LS.muted) return;
  try{
    actx = actx || new (window.AudioContext||window.webkitAudioContext)();
    const o = actx.createOscillator(), g = actx.createGain();
    o.connect(g); g.connect(actx.destination);
    const t = actx.currentTime;
    if(kind==='ok'){ o.type='triangle'; o.frequency.setValueAtTime(620,t); o.frequency.exponentialRampToValueAtTime(1040,t+.09); }
    else if(kind==='bad'){ o.type='sawtooth'; o.frequency.setValueAtTime(220,t); o.frequency.exponentialRampToValueAtTime(110,t+.16); }
    else { o.type='sine'; o.frequency.setValueAtTime(880,t); }
    g.gain.setValueAtTime(.0001,t);
    g.gain.exponentialRampToValueAtTime(kind==='bad'?.14:.16,t+.012);
    g.gain.exponentialRampToValueAtTime(.0001,t+.24);
    o.start(t); o.stop(t+.26);
  }catch(e){}
}

const RING_C = 2*Math.PI*18;
let S = null, raf = 0, pausedAt = 0;

/* ---------- screens ---------- */
function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active', s.id===id));
  window.scrollTo(0,0);
}

/* ---------- start ---------- */
let chosen = 30;
$('#countSel').addEventListener('click', e=>{
  const b = e.target.closest('.seg'); if(!b) return;
  chosen = +b.dataset.n;
  [...$('#countSel').children].forEach(s=>s.setAttribute('aria-pressed', s===b));
});

function start(order){
  S = { order, i:0, score:0, streak:0, correct:0, results:[], answered:false, t0:0 };
  $('#total').textContent = order.length;
  document.getElementById('ringfg').style.strokeDasharray = RING_C;
  show('game');
  render();
}

function newGame(){
  // balanced selection: round-robin across topics so every tanda is diversa
  const byTopic = {};
  CARDS.forEach((c,i)=>{ (byTopic[c.topic] = byTopic[c.topic] || []).push(i); });
  const buckets = Object.values(byTopic).map(a=>shuffle(a));
  const order = [];
  let progress = true;
  while(order.length < chosen && progress){
    progress = false;
    for(const b of shuffle(buckets)){
      if(b.length){ order.push(b.pop()); progress = true; if(order.length >= chosen) break; }
    }
  }
  start(shuffle(order));
}

/* ---------- render card ---------- */
function render(){
  const c = CARDS[S.order[S.i]];
  S.answered = false;
  $('#counter').textContent = pad(S.i+1);
  $('#bar').style.width = (S.i/S.order.length*100) + '%';
  $('#topic').textContent = c.topic;
  $('#fig').innerHTML = c.fig;
  $('#fig').setAttribute('aria-label', c.q);
  $('#question').textContent = c.q;
  $('#feedback').hidden = true;

  const opts = shuffle(c.options);
  const box = $('#options'); box.innerHTML = '';
  opts.forEach((o,k)=>{
    const b = document.createElement('button');
    b.className = 'opt'; b.type = 'button';
    b.innerHTML = `<span class="k">${k+1}</span><span class="ov">${o}</span><span class="mark"></span>`;
    b.addEventListener('click', ()=>answer(b, o, c));
    box.appendChild(b);
  });
  // timer
  S.t0 = performance.now(); pausedAt = 0;
  setRing(0, c.t);
  cancelAnimationFrame(raf);
  const loop = ()=>{
    if(S.answered) return;
    const el = (performance.now()-S.t0)/1000;
    $('#elapsed').textContent = el<60 ? Math.floor(el)+'s' : Math.floor(el/60)+':'+pad(Math.floor(el%60));
    setRing(el, c.t);
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);
}

function setRing(el, target){
  const frac = Math.min(el/target, 1);
  const r = document.getElementById('ringfg');
  r.style.strokeDashoffset = RING_C*frac;
  r.style.stroke = frac<0.7 ? 'var(--accent)' : frac<1 ? 'var(--warn)' : 'var(--bad)';
}

/* ---------- answer ---------- */
function answer(btn, val, c){
  if(S.answered) return;
  S.answered = true;
  cancelAnimationFrame(raf);
  const el = (performance.now()-S.t0)/1000;
  const ok = val === c.answer;
  [...$('#options').children].forEach(b=>{
    b.disabled = true;
    const v = b.querySelector('.ov').textContent;
    if(v === c.answer){ b.classList.add('correct'); b.querySelector('.mark').textContent='✓'; }
    else if(b===btn){ b.classList.add('wrong'); b.querySelector('.mark').textContent='✕'; }
  });
  // score
  let gained = 0;
  if(ok){
    S.correct++; S.streak++;
    const speed = Math.max(0, Math.round(50*(1 - Math.min(el/c.t,1))));
    gained = 100 + speed + (S.streak-1)*10;
    beep('ok');
  } else { S.streak = 0; beep('bad'); }
  S.score += gained;
  S.results.push({ idx:S.order[S.i], ok, time:el });
  // hud
  $('#score').textContent = S.score;
  $('#streak').textContent = S.streak;
  $('#streakChip').dataset.on = S.streak>=2 ? '1':'0';
  // feedback
  const fb = $('#feedback');
  fb.className = 'feedback ' + (ok?'fb-ok':'fb-bad');
  $('#fbMark').textContent = ok?'✓':'✕';
  $('#fbTitle').textContent = ok ? (gained>=150?'¡Perfecto y veloz!':'¡Correcto!') : 'Casi — fíjate:';
  $('#fbTime').textContent = '⏱ ' + el.toFixed(1) + 's' + (ok && gained>=150 ? ' · +'+gained : '');
  $('#fbSol').textContent = c.sol;
  $('#fbTip').textContent = ' ' + c.tip;
  fb.hidden = false;
  requestAnimationFrame(()=>$('#nextBtn').focus());
}

function next(){
  if(!S.answered) return;
  if(S.i < S.order.length-1){ S.i++; render(); }
  else finish();
}

/* ---------- finish ---------- */
function finish(){
  cancelAnimationFrame(raf);
  $('#bar').style.width = '100%';
  const n = S.results.length;
  const acc = Math.round(S.correct/n*100);
  const totT = S.results.reduce((s,r)=>s+r.time,0);
  const avg = totT/n;
  if(S.score > LS.best) LS.best = S.score;

  const tiers = [
    {min:90, fast:9,  t:'Relámpago', s:'Velocidad y criterio de élite ⚡'},
    {min:75, fast:14, t:'Veloz',     s:'Muy bien — afina los temas flojos'},
    {min:55, fast:99, t:'En ritmo',  s:'Buena base, ahora gana velocidad'},
    {min:0,  fast:99, t:'Calentando',s:'Repasa los criterios y vuelve a intentarlo'}
  ];
  let tier = tiers.find(x=>acc>=x.min && avg<=x.fast) || tiers.find(x=>acc>=x.min);
  $('#rating').textContent = tier.t;
  $('#ratingSub').textContent = tier.s;
  $('#mAcc').textContent = acc + '%';
  $('#mSpeed').textContent = avg.toFixed(1);
  $('#mScore').textContent = S.score;

  // topics
  const tg = {};
  S.results.forEach(r=>{
    const t = CARDS[r.idx].topic;
    (tg[t] = tg[t] || {ok:0,n:0,time:0});
    tg[t].n++; tg[t].time += r.time; if(r.ok) tg[t].ok++;
  });
  const tbox = $('#topics'); tbox.innerHTML = '';
  Object.entries(tg).sort((a,b)=>a[1].ok/a[1].n - b[1].ok/b[1].n).forEach(([name,d])=>{
    const pc = Math.round(d.ok/d.n*100);
    const cls = pc<50?'low':pc<80?'mid':'';
    const row = document.createElement('div');
    row.className = 'tbar';
    row.innerHTML = `<span class="nm">${name}</span><span class="bar"><i class="${cls}" style="width:0"></i></span><span class="pc">${d.ok}/${d.n}</span>`;
    tbox.appendChild(row);
    requestAnimationFrame(()=>row.querySelector('i').style.width = pc+'%');
  });

  // missed
  const wrong = S.results.filter(r=>!r.ok);
  const ml = $('#missList'); ml.innerHTML = '';
  if(!wrong.length){
    ml.innerHTML = '<div class="empty-good">✓ ¡Sin errores! Dominio total de esta tanda.</div>';
    $('#retryWrongBtn').hidden = true;
  } else {
    wrong.forEach(r=>{
      const c = CARDS[r.idx];
      const el = document.createElement('div');
      el.className = 'missc';
      el.innerHTML = `<span class="mfig">${c.fig}</span><div><div class="mq">${c.q}</div><div class="ma">→ ${c.answer} · ${c.tip}</div></div>`;
      ml.appendChild(el);
    });
    const ids = wrong.map(r=>r.idx);
    $('#retryWrongBtn').hidden = false;
    $('#retryWrongBtn').onclick = ()=>start(shuffle(ids));
  }
  show('results');
}

/* ---------- pause ---------- */
function setPause(on){
  const ov = $('#pauseOv');
  if(on){
    if(S && !S.answered){ pausedAt = performance.now(); cancelAnimationFrame(raf); }
    ov.classList.add('open');
  } else {
    if(S && !S.answered && pausedAt){
      S.t0 += performance.now() - pausedAt; pausedAt = 0;
      const c = CARDS[S.order[S.i]];
      const loop = ()=>{ if(S.answered) return; const e=(performance.now()-S.t0)/1000;
        $('#elapsed').textContent = e<60?Math.floor(e)+'s':Math.floor(e/60)+':'+pad(Math.floor(e%60));
        setRing(e,c.t); raf=requestAnimationFrame(loop); };
      raf = requestAnimationFrame(loop);
    }
    ov.classList.remove('open');
  }
}

/* ---------- solucionario ---------- */
function renderSol(){
  const box = $('#solList');
  if(box.dataset.done) return; box.dataset.done = '1';
  box.innerHTML = SOL.map(s=>`
    <article class="sol-card">
      <div class="sol-head"><span class="sol-pid">${s.pid}</span><span class="sol-topic">${s.topic}</span><span class="sol-ans">✓ ${s.ans}</span></div>
      <p class="sol-q">${s.q}</p>
      <div class="figwrap sol-fig"><div role="img" aria-label="${s.q}">${s.fig}</div></div>
      <div class="sol-steps">
        ${s.steps.map((st,i)=>`<div class="step"><span class="sn">${i+1}</span><div class="sb"><span class="st">${st.t}</span>${st.m?`<span class="sm">${st.m}</span>`:''}</div></div>`).join('')}
      </div>
      <div class="sol-res"><span>Resultado</span><b>${s.res}</b></div>
      <div class="sol-clave"><span class="bulb">🎯</span><p><b>Clave para el examen</b>${s.clave}</p></div>
    </article>`).join('');
}

/* ---------- wiring ---------- */
$('#startBtn').addEventListener('click', newGame);
$('#solBtn').addEventListener('click', ()=>{ renderSol(); show('solucionario'); });
$('#solBack').addEventListener('click', ()=>show('start'));
$('#againBtn').addEventListener('click', ()=>show('start'));
$('#nextBtn').addEventListener('click', next);
$('#pauseBtn').addEventListener('click', ()=>setPause(true));
$('#resumeBtn').addEventListener('click', ()=>setPause(false));
$('#muteBtn').addEventListener('click', ()=>{ LS.muted = !LS.muted; syncMute(); if(!LS.muted) beep('tick'); });
function syncMute(){ $('#muteBtn').textContent = LS.muted ? '🔇' : '🔊'; }

$('#cheatBtn').addEventListener('click', ()=>$('#cheat').classList.add('open'));
$('#cheatClose').addEventListener('click', ()=>$('#cheat').classList.remove('open'));
$('#cheat').addEventListener('click', e=>{ if(e.target.id==='cheat') $('#cheat').classList.remove('open'); });

document.addEventListener('keydown', e=>{
  if($('#cheat').classList.contains('open')){ if(e.key==='Escape') $('#cheat').classList.remove('open'); return; }
  if($('#solucionario').classList.contains('active')){ if(e.key==='Escape') show('start'); return; }
  if($('#game').classList.contains('active')){
    if(e.key==='Escape'){ setPause(!$('#pauseOv').classList.contains('open')); return; }
    if($('#pauseOv').classList.contains('open')) return;
    if(['1','2','3','4'].includes(e.key) && !S.answered){
      const b = $('#options').children[+e.key-1]; if(b) b.click();
    } else if((e.key===' '||e.key==='Enter'||e.key==='ArrowRight') && S.answered){
      e.preventDefault(); next();
    } else if(e.key.toLowerCase()==='m'){ LS.muted=!LS.muted; syncMute(); }
  } else if($('#start').classList.contains('active') && (e.key==='Enter')){ newGame(); }
});

/* ---------- cheat sheet build ---------- */
(function(){
  const seen = new Set(); const list = $('#cheatList');
  CARDS.forEach(c=>{
    if(seen.has(c.tip)) return; seen.add(c.tip);
    const d = document.createElement('div');
    d.className = 'cheat-i';
    d.innerHTML = `<span class="ci-t">${c.topic}</span><p>${c.tip}</p>`;
    list.appendChild(d);
  });
})();

/* ---------- init ---------- */
syncMute();
$('#poolN').textContent = CARDS.length;
const b = LS.best; $('#bestScore').textContent = b ? b.toLocaleString('es') : '—';
</script>
</body>
</html>
'''

import os
js = JS.replace('__CARDS__', json.dumps(cards, ensure_ascii=False))
js = js.replace('__SOL__', json.dumps(SOL, ensure_ascii=False))
html = HEAD + BODY + js
os.makedirs('geoflash', exist_ok=True)
for path in ('GeoFlash.html', os.path.join('geoflash', 'index.html')):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
print('OK ->', len(cards), 'cards,', len(SOL), 'soluciones,', len(html), 'bytes')


