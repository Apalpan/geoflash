# GeoFlash ▲

**Entrenador de velocidad en geometría básica.** Tarjetas tipo flashcard con figuras, cronómetro y el *criterio rápido* de cada caso — para reconocer el patrón al instante y resolver cualquier problema con seguridad.

### ▶ [Abrir GeoFlash](https://apalpan.github.io/geoflash/)

---

## Qué incluye

- **54 casos gráficos** repartidos en 9 temas; cada tanda se arma con **selección equilibrada por tema**, así siempre practicas diverso.
- Elige al inicio **10 / 20 / 30** preguntas.
- Cada carta: **figura SVG** + 4 opciones + solución + **criterio rápido** (el atajo mental).
- **Modo flash:** presupuesto de tiempo por carta (anillo), racha 🔥, puntaje con bono de velocidad.
- **Resultados con análisis:** velocidad, aciertos y **dominio por tema** (detecta qué va lento) + repaso de falladas.
- **Chuleta** con todos los criterios y **mejor puntaje** guardado localmente.
- 100% offline, sin build, archivo único.

## Temas

Ángulos · Paralelas · Triángulos · Triángulos notables (45-45-90, 30-60-90, 37-53) ·
Pitágoras y ternas · Líneas notables (mediana, bisectrices, baricentro, Poncelet) ·
Polígonos · Circunferencia (central, inscrito, semiinscrito, Thales, Pitot, potencia, tangentes) · Áreas.

## Controles

| Tecla | Acción |
|-------|--------|
| `1`–`4` | Responder |
| `Espacio` / `Enter` | Siguiente |
| `Esc` | Pausa |
| `M` | Silenciar |

## Desarrollo

`index.html` es un artefacto generado. Para editar el contenido o el estilo, modifica
`build_geoflash.py` (incluye un mini-DSL de SVG para dibujar las figuras) y regenera:

```bash
python build_geoflash.py
```

**Stack:** HTML/CSS/JS vanilla · tokens OKLCH (paleta AECODE teal, tema light) ·
Space Grotesk + Inter · figuras SVG generadas en Python · sin dependencias.

---

Hecho para práctica CEPRE · GEN+
