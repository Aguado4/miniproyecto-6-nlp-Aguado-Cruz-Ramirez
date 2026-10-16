# EXPERIMENTS - Bitácora de resultados

> **Regla:** solo números efectivamente ejecutados. **Estado:** corrida de referencia completa.
> Las cifras vienen de las salidas versionadas del notebook y de `results/metrics/*.csv`.

| Campo | Valor |
|---|---|
| Fecha | 2026-10-16 |
| Plataforma | Linux, Python 3.12.14, torch 2.14.1 (CPU) |
| GPU | no usada (`MP6_SOLO_CPU=1`, D-607) |
| Ollama / modelo | 0.34.0 / `llama3.2:3b` |
| Temperatura del agente | 0.0 |
| Semilla | 42 |
| Ejecución | `jupyter nbconvert --execute` desde cero (sin cachés de datos ni de índice): **31,8 min**, sin errores, puertos libres al terminar |

## 1. El corpus que ven las herramientas

| Métrica | Valor |
|---|---:|
| Reseñas cargadas | 208.051 |
| Destinos | 40 |
| Estados | 19 |
| Fichas de destino | 40 (131.920 palabras) |
| Reseñas en el índice de búsqueda | 27.400 (13,2 %, D-605) |
| Tiempo de codificación del índice (CPU) | 524 s |
| Fragmentos de fichas en el RAG de §9 | 1.120 |

## 2. Las herramientas, probadas una por una (§4)

Ida y vuelta completa por MCP (transporte HTTP, sesión, `call_tool`).

| Herramienta | Entrada de prueba | ¿Responde? | ms |
|---|---|---|---:|
| `estadisticas_destino` | `destino="San Cristóbal de las Casas"` | sí | 55 |
| `comparar_destinos` | `n=3, tipo="Restaurant"` | sí | 45 |
| `buscar_resenas` | quejas de limpieza, Tulum, Hotel, ≤2 estrellas | sí | 41 |
| `ficha_destino` | `destino="Real de Catorce"` | sí | 21 |

Arranque de los dos servidores: 10,0 s.

## 3. H1 · Agregación: tres caminos (§5, §7, §9)

| Pregunta de agregación | Valor real | Modelo solo | RAG puro | Agente con herramientas |
|---|---:|---|---|---|
| A01 reseñas de Bacalar | 10.822 | «no tengo información» | «5 reseñas» | 10.822 ✔ |
| A02 media de Palenque | 4,44 | «varía según la fuente» | «5 estrellas» | 4,44 ✔ |
| A03 reseñas de 1★ de Tulum | 798 | «aproximadamente 2.500» | «todos son de 5 estrellas» | 798 ✔ |
| A04 reseñas de hoteles de Valladolid | 2.673 | «más de 2.500» | «5 reseñas» | 11.637 ✘ (copió el total) |
| A05 media de Isla Mujeres | 4,52 | «4,8 o 5» | «5 estrellas» | 4,52 ✔ |
| A06 reseñas de restaurantes de San Cristóbal | 6.260 | «alrededor de 2.500» | «3 opiniones» | 6.260 ✔ |
| A07 reseñas de 5★ de Real de Catorce | 463 | «2 reseñas» | «3 reseñas» | 463 ✔ |
| A08 media de atracciones de Taxco | 4,46 | «4,5» ✔ (por suerte) | «5 estrellas» | 4,46 ✔ |
| A09 reseñas de Teotihuacan | 5.810 | «más de 22.000» | «3 reseñas» | 5.810 ✔ |
| A10 mejor valorado | Teotihuacan | San Miguel de Allende (no está en el corpus) | Cuetzalan | Teotihuacan ✔ |
| A11 mejores restaurantes | Tulum | Ciudad de México (no está en el corpus) | Tulum ✔ | Tulum ✔ |
| A12 peores hoteles | Taxco | Cancún (no está en el corpus) | Tepoztlán | Taxco ✔ |
| **Aciertos** | | **1 / 12** | **1 / 12** | **11 / 12** |

El RAG tiende a responder con **el número de documentos recuperados** («5 reseñas», «3 opiniones»).

## 4. H2 · ¿Elige bien? (§7, 26 preguntas, 4 herramientas)

| Métrica | Agregación | Experiencia | Hecho | Total |
|---|---:|---:|---:|---:|
| Selección correcta de herramienta | 1,00 | 1,00 | 1,00 | **1,00** (26/26) |
| Argumentos correctos | 1,00 | 0,88 | 1,00 | 0,96 (25/26) |
| Preguntas con llamadas innecesarias | 0 | 0 | 0 | 0 |
| Preguntas sin ninguna llamada cuando hacía falta | 0 | 0 | 0 | 0 |
| Respuesta correcta | 0,92 | n/a | 1,00 | 0,94 |
| Precisión de la evidencia | n/a | 0,88 | n/a | n/a |
| Segundos por pregunta | 7,4 | 21,7 | 10,0 | 12,4 |

Fallos: **A04** (herramienta y argumentos bien, cifra mal leída de la salida) y **E07** (argumento
inventado: `destino="Barrancas del Cobre"`).

## 5. H3 · Menú de herramientas y calidad de las descripciones (§8)

Mismas 17 preguntas (9 de agregación con `estadisticas_destino`, 8 de experiencia con
`buscar_resenas`).

| Configuración | Selección correcta | Argumentos correctos | Llamadas innecesarias | Cifra exacta | Evidencia |
|---|---:|---:|---:|---:|---:|
| 2 herramientas | 0,94 | 0,88 | 0,06 | 0,78 | 0,88 |
| 4 herramientas | **1,00** | 0,94 | 0,00 | 0,89 | 0,88 |
| 4 con descripciones de una línea | 0,47 | 0,06 | 0,53 | 0,00 | 0,68 |

Con descripciones de una línea, el agente llamó `buscar_resenas` en las 17 preguntas.

## 6. Comparación con el RAG de MP5 (§9)

| Tipo de pregunta | Modelo solo | RAG puro | Agente con herramientas |
|---|---:|---:|---:|
| agregación (cifra exacta) | 0,08 | 0,08 | **0,92** |
| experiencia (precisión de evidencia) | n/a | 0,70 | **0,88** |
| hecho (estado correcto) | 0,67 | **1,00** | **1,00** |

En experiencia, el RAG cae en las dos preguntas de quejas (E01: 0,2; E06: 0,0) porque no filtra
por polaridad; el agente obtiene 1,0 en ambas con `estrellas_max=2`.

## 7. Costo

| Etapa | Valor |
|---|---:|
| Arranque de los servidores | 10,0 s |
| Ida y vuelta por MCP | 21 a 55 ms |
| Pregunta al modelo solo | 1,9 s de media |
| Pregunta al RAG puro (solo generación) | 14,3 s de media |
| Pregunta al agente (decisión, llamada y redacción) | 12,4 s de media (7,4 en agregación, 21,7 en experiencia) |

## 8. Veredicto de hipótesis

| Hipótesis | Veredicto |
|---|---|
| **H1** · la agregación necesita herramienta | **Confirmada**: 11/12 frente a 1/12 del modelo solo y del RAG |
| **H2** · el cuello de botella es la elección, no la herramienta | **Parcial**: la herramienta nunca falló, pero la elección tampoco (26/26); los errores fueron de argumentos, de lectura y de contrato (D-610) |
| **H3** · más herramientas, peor elección | **Refutada tal como se planteó**: 2 → 4 herramientas no empeora (0,94 → 1,00); lo que hunde la elección son las descripciones (1,00 → 0,47) |

## 9. Corridas previas

- **Corrida 1** (descartada): se cortó en §9 por un nombre de columna y reveló que el esquema de
  `buscar_resenas` rechazaba `k: null` (D-610). Sus métricas de §7 y §8 no se reportan.

## 10. Video

`results/video/demo_chatbot_mcp.mp4`: 1 min 12 s, grabado sobre JupyterLab con Playwright (D-609),
CPU. Muestra la ejecución de la celda de Gradio, «¿Cuántas reseñas de 1 estrella tiene Tulum?»
(respuesta en 10 s, cita `estadisticas_destino` y sus cifras) y «¿De qué se quejan los turistas en
los hoteles de Tulum?» (respuesta en 18 s, cita ocho reseñas con destino, tipo y estrellas).
