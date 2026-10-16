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

## D-605 · El índice de búsqueda es una muestra estratificada; el cálculo usa el corpus completo

**Estado:** aceptada · 2026-10-16

**Contexto.** Codificar las 208.051 reseñas con `multilingual-e5-small` en CPU toma cerca de
media hora, y la reproducibilidad pide que «Restart & Run All» termine en un tiempo razonable.

**Decisión.** `buscar_resenas` busca sobre una muestra de **hasta 250 reseñas por destino y
tipo** (semilla 42), que conserva los 120 grupos y toma completos los pequeños. Las herramientas de
cálculo leen siempre el corpus completo.

**Alternativas.** (a) Codificar todo: media hora extra en cada ejecución desde cero. (b) Muestra
aleatoria simple: los grupos pequeños (Cholula hoteles tiene 15 reseñas) quedarían vacíos y el
filtro por destino y tipo devolvería nada.

**Consecuencias.** La asimetría es deliberada y refuerza la tesis: el índice ve una fracción del
corpus y **no puede contar**, lo que §9 mide.

---

## D-606 · `comparar_destinos` recibe `peores: bool` en lugar de un `n` negativo

**Estado:** aceptada · 2026-10-16

**Contexto.** El primer diseño pedía un `n` negativo para el ranking de peor valorados. Es una
convención que un modelo de 3B no descubre leyendo el esquema.

**Decisión.** Un argumento explícito `peores: bool = False`, documentado en el docstring.

**Consecuencias.** El contrato de `mcp_servers/README.md` se actualiza. La pregunta A12 del banco
mide si el agente lo usa.

---

## D-607 · La corrida de referencia es solo CPU

**Estado:** aceptada · 2026-10-16

**Contexto.** La GPU de la máquina de referencia se usa para otras tareas y no se ocupa sin
confirmación.

**Decisión.** `MP6_SOLO_CPU=1` pasa `num_gpu=0` a Ollama y el codificador corre en CPU. Sin la
variable, Ollama decide como siempre, de modo que en otra máquina la GPU se aprovecha sola.

**Consecuencias.** Las latencias reportadas son de CPU y son una cota superior.

---

## D-608 · La ablación de descripciones se hace en el cliente, no con otro servidor

**Estado:** aceptada · 2026-10-16

**Contexto.** Para medir cuánto del acierto de selección se debe a los docstrings hace falta una
versión de las herramientas con descripciones pobres.

**Decisión.** Copiar las herramientas descubiertas por MCP y sustituir solo su `description` por
una frase de dos o tres palabras. El esquema de argumentos y el servidor no cambian.

**Alternativas.** Un tercer servidor con docstrings cortos: duplica código y un tercer puerto que
apagar, para cambiar exactamente el mismo texto que el modelo lee.

**Consecuencias.** Se aísla la variable que interesa: la descripción que llega al modelo.

---

## D-609 · El video se graba automatizando JupyterLab con Playwright

**Estado:** aceptada · 2026-10-16

**Contexto.** La consigna exige un video con la ejecución de la celda de Gradio y dos
interacciones con referencias.

**Decisión.** Las celdas previas se ejecutan en un contexto de navegador sin grabar; un segundo
contexto, grabado, se conecta al mismo kernel, ejecuta la celda de Gradio y hace dos preguntas
dentro de la interfaz incrustada. El video queda en `results/video/`.

**Consecuencias.** Lo que se ve es la ejecución real, con latencias reales de CPU. Si la espera
hace que pase de dos minutos, solo se aceleran los tramos de espera y se indica en el video.

---

## D-610 · Los argumentos numéricos opcionales aceptan `null`

**Estado:** aceptada · 2026-10-16

**Contexto.** En la primera corrida, `llama3.2:3b` llamó `buscar_resenas` con `k: null` y
`estrellas_max: null`. Con `k: int = 5` el esquema rechazaba el `null`, la herramienta devolvía un
error de validación y el modelo respondió con conocimiento propio («cochinita pibil») creyendo
que no tenía la herramienta. Es un fallo de **contrato**, no de elección.

**Decisión.** Declarar `k`, `n`, `min_resenas` y `peores` como opcionales (`int | None`,
`bool | None`); el servidor ya convertía los vacíos al valor por omisión.

**Consecuencias.** Los esquemas MCP deben ser tolerantes con lo que un modelo pequeño escribe de
verdad. Las cifras reportadas son de la corrida posterior a este cambio.

---

## Plantilla para nuevas entradas

## D-6NN · Título breve

**Estado:** aceptada | revisada | descartada · fecha

**Contexto.** Qué problema había.

**Decisión.** Qué se hizo.

**Alternativas.** Qué se descartó y por qué.

**Consecuencias.** Qué implica, incluido lo que empeora.
