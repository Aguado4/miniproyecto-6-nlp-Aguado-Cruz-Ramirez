# EXPERIMENTS - Bitácora de resultados

> **Regla:** solo números efectivamente ejecutados. **Estado:** sin ejecutar.

| Campo | Valor |
|---|---|
| Fecha | — |
| Plataforma / GPU | — |
| Ollama / modelo | — / `llama3.2:3b` |
| Temperatura del agente | — |
| Semilla | 42 |
| Ejecución | — |

## 1. El corpus que ven las herramientas

| Métrica | Valor |
|---|---:|
| Reseñas cargadas | |
| Destinos | |
| Fichas de destino | |

## 2. Las herramientas, probadas una por una (§4)

| Herramienta | Entrada de prueba | ¿Responde? | ms |
|---|---|---|---:|
| `estadisticas_destino` | | | |
| `comparar_destinos` | | | |
| `buscar_resenas` | | | |
| `ficha_destino` | | | |

## 3. H1 · Agregación: agente con herramientas frente al modelo solo (§5, §7)

| Pregunta de agregación | Valor real | Modelo solo | Agente con herramientas |
|---|---:|---:|---:|

## 4. H2 · ¿Elige bien? (§7)

| Métrica | Valor |
|---|---:|
| Selección correcta de herramienta | |
| Argumentos correctos | |
| Llamadas innecesarias | |
| Preguntas sin ninguna llamada cuando hacía falta | |

## 5. H3 · Dos herramientas frente a cuatro (§8)

| Herramientas disponibles | Selección correcta | Argumentos correctos | Llamadas innecesarias |
|---:|---:|---:|---:|
| 2 | | | |
| 4 | | | |

## 6. Comparación con el RAG de MP5 (§9)

| Tipo de pregunta | RAG de MP5 | Agente con herramientas |
|---|---:|---:|
| agregación | | |
| experiencia | | |
| hecho | | |

## 7. Costo

| Etapa | ms |
|---|---:|
| Arranque de los servidores | |
| Ida y vuelta por MCP | |
| Decisión del agente | |
| Redacción final | |

## 8. Veredicto de hipótesis

| Hipótesis | Veredicto |
|---|---|
| **H1** · la agregación necesita herramienta | pendiente |
| **H2** · el cuello de botella es la elección, no la herramienta | pendiente |
| **H3** · más herramientas, peor elección | pendiente |
