# DECISIONS - Registro de decisiones

> Una entrada por decisión que un lector podría cuestionar. Formato fijo: contexto, decisión,
> alternativas descartadas y consecuencias. Numeración desde D-601.

---

## D-601 · Las herramientas operan sobre nuestro corpus, no sobre una calculadora

**Estado:** aceptada · 2026-10-11

**Contexto.** El guía expone dos herramientas por MCP: una calculadora aritmética y una consulta
de clima a una API pública. Son buenos ejemplos didácticos y la consigna prohíbe reutilizarlos.

**Decisión.** Las cuatro herramientas consultan el **corpus de las entregas anteriores**: dos
calculan agregaciones sobre las reseñas de Rest-Mex y dos recuperan texto (reseñas y fichas de
destino de Wikipedia).

**Por qué, más allá de que la consigna lo pida.** Con una calculadora, la respuesta correcta la
sabe cualquiera y no hay nada que medir más allá de si el agente llamó la herramienta. Con
nuestro corpus, **la respuesta correcta se puede calcular por un camino independiente** (un
`groupby` sobre el `DataFrame`) y compararla con lo que dijo el agente. Eso convierte la
evaluación en algo automático, que es lo que hizo fuerte al Miniproyecto 5.

**Alternativas.** (a) Herramientas sobre una API externa: la respuesta cambia con el tiempo y el
notebook deja de ser reproducible. (b) Herramientas de juguete sobre datos inventados: no hay EDA
ni continuidad con la serie.

**Consecuencias.** Hay que cargar el corpus dentro de los servidores, lo que los hace más lentos
de arrancar que los del guía, y obliga a cargarlo una sola vez al inicio y no por llamada.

---

## D-602 · Se reutilizan el corpus y las fichas de MP5, sin heredar celdas

**Estado:** aceptada · 2026-10-11

**Contexto.** MP2, MP3 y MP4 copiaban sin modificar un bloque de 63 celdas del notebook de MP1.
MP5 rompió con eso (su D-502) porque no tenía tarea de clasificación y el bloque habría sido
código muerto.

**Decisión.** Igual que MP5: **se reutilizan los datos, no las celdas**. El corpus de reseñas se
descarga del mismo identificador de HuggingFace y las fichas de destino se copian del archivo
`data/fichas_destino.json` que construyó MP5, con su procedencia y su licencia.

**Alternativas.** Heredar el bloque de MP1: aquí no se clasifica nada, así que serían 63 celdas
sin uso en un notebook que ya tiene once secciones, y la retroalimentación del MP1 pidió
exactamente lo contrario.

**Consecuencias.** El EDA de esta entrega es mínimo y solo cubre lo que las herramientas
necesitan (qué destinos existen, cuántas reseñas tiene cada uno, cómo se reparten las estrellas).
No se pretende comparar números con MP1 a MP4.

---

## D-603 · Transporte HTTP y puertos 9090 y 9091

**Estado:** aceptada · 2026-10-11

**Contexto.** MCP admite `stdio` y HTTP. El guía usa `streamable-http` en los puertos 9080 y 9081
porque `stdio` da problemas en Colab.

**Decisión.** Mantener `streamable-http` y usar **9090 y 9091**, de modo que los servidores del
guía y los nuestros puedan convivir sin chocar durante las pruebas.

**Consecuencias.** Hay procesos de servidor que **hay que apagar**. Un servidor olvidado deja el
puerto ocupado y hace fallar la siguiente ejecución, lo que golpea el criterio de reproducibilidad
(2 de 7 puntos). La celda de apagado es obligatoria y tiene que poder ejecutarse dos veces sin
error.

---

## D-604 · La selección de herramienta se mide leyendo la traza

**Estado:** aceptada · 2026-10-11

**Contexto.** El guía evalúa el comportamiento del agente leyendo la traza y comentándola. Es
suficiente para una clase, pero no permite comparar configuraciones ni detectar una degradación.

**Decisión.** El banco de preguntas declara, para cada pregunta, **qué herramienta debería
llamarse y con qué argumentos**, y la evaluación compara eso con lo que aparece en la traza del
agente. Las métricas son tasa de selección correcta, argumentos correctos y llamadas innecesarias.

**Alternativas.** (a) Juzgar a ojo, como el guía: no se puede comparar dos herramientas contra
cuatro, que es el experimento de H3. (b) Usar un LLM como juez: es el mismo modelo que decide, con
la circularidad que eso implica; la lección la dejó §12 del Miniproyecto 4.

**Consecuencias.** Mide **la elección**, no la calidad de la redacción final. Esa última queda
declarada como cualitativa.

---

## Plantilla para nuevas entradas

## D-6NN · Título breve

**Estado:** aceptada | revisada | descartada · fecha

**Contexto.** Qué problema había.

**Decisión.** Qué se hizo.

**Alternativas.** Qué se descartó y por qué.

**Consecuencias.** Qué implica, incluido lo que empeora.
