---
name: leetcode-notes-processor
description: Procesa entradas en sucio del inbox de notas de LeetCode y las organiza en la estructura reviewed/. Úsalo siempre que el usuario diga "procesa el inbox", "organiza mis notas", "procesa mis apuntes", o cuando haya archivos nuevos en la carpeta inbox/ que no estén en processed/. También úsalo cuando el usuario pida actualizar, complementar o revisar notas existentes.
---

# LeetCode Notes Processor

Sistema de notas para consolidar aprendizajes de LeetCode. El usuario escribe en sucio en `inbox/` y Claude organiza, complementa y mueve a `reviewed/`.

## Estructura del repo

```
leetcode-notes/
├── SKILL.md                  ← este archivo
├── README.md
├── inbox/                    ← el usuario dump aquí en sucio
│   └── processed/            ← archivos ya procesados se mueven aquí
└── reviewed/
    ├── diario/               ← YYYY-MM-DD.md por día
    ├── temas/                ← stack.md, linked-list.md, etc.
    └── problemas/            ← basic-calculator.md, etc.
```

## Flujo al procesar

1. Leer TODOS los archivos en `inbox/` que NO estén en `inbox/processed/`
2. Por cada archivo:
   a. Identificar qué problemas se mencionan
   b. Identificar qué temas se tocan
   c. Extraer: aprendizajes conceptuales, código de referencia, errores cometidos, tiempos
   d. Actualizar o crear archivos en `reviewed/` (ver formatos abajo)
   e. Mover el archivo original a `inbox/processed/`
3. Reportar al usuario qué archivos se procesaron y qué se creó/actualizó

## Formato: reviewed/diario/YYYY-MM-DD.md

```markdown
# YYYY-MM-DD

## Resumen del día
[2-3 oraciones sobre qué se hizo]

## Problemas trabajados
- [Nombre del problema] — [Easy/Medium/Hard] — [tiempo aproximado]

## Temas tocados
- [tema1], [tema2]

## Feelings / estado
[cómo se sintió el usuario ese día, directo y sin filtro]

## Links
- [links a problemas si los hay]
```

## Formato: reviewed/temas/[tema].md

Nombrar el archivo en kebab-case: `linked-list.md`, `dynamic-programming.md`, etc.

```markdown
# [Nombre del Tema]

## Conceptos clave
[aprendizajes conceptuales organizados, no repetir si ya existen, complementar]

## Patrones recurrentes
[patrones de solución que aplican a este tema]

## Código de referencia
```cpp
// descripción del patrón
[código limpio y canónico]
```

## Errores comunes
- [error] → [cómo evitarlo]

## Problemas relacionados
- [nombre] — [dificultad]
```

## Formato: reviewed/problemas/[nombre-del-problema].md

Nombrar en kebab-case: `basic-calculator.md`, `min-stack.md`, etc.

```markdown
# [Nombre del Problema]

**Dificultad:** Easy / Medium / Hard  
**Tema(s):** [tema1], [tema2]  
**Tiempo invertido:** [X horas / X minutos]  
**URL:** [link si está disponible]

## Descripción breve
[1-2 oraciones de qué pide el problema]

## Enfoque de solución
[explicación del approach, no el código completo]

## Código final
```cpp
[solución canónica]
```

## Errores cometidos
- [qué salió mal y por qué]

## Aprendizajes clave
- [insight 1]
- [insight 2]

## Notas adicionales
[edge cases, optimizaciones posibles, variantes del problema]
```

## Reglas de procesamiento

- **No sobreescribir**: si ya existe un archivo en `reviewed/`, hacer APPEND o complementar, nunca borrar contenido previo
- **No inventar**: si el usuario no menciona algo (ej. no dio el código), no inventarlo
- **Complementar con criterio**: puedes agregar contexto técnico relevante que el usuario no mencionó (ej. nombre del patrón, complejidad O(n)), siempre que sea correcto y útil
- **Tono**: directo, técnico, sin relleno
- **Idioma**: español, código en inglés (nombres de variables, comentarios)
- **Código**: si el usuario pegó código, incluirlo. Si mencionó el approach pero no el código, describir el approach sin inventar código
- **Fechas**: inferir la fecha del nombre del archivo inbox o de menciones en el texto. Si no hay fecha clara, usar la fecha de hoy

## Qué hacer si el inbox está vacío

Decirle al usuario que no hay archivos nuevos en `inbox/` y sugerir que agregue sus notas del día.

## Qué hacer si hay ambigüedad

Si algo no está claro (ej. no se sabe a qué problema corresponde un código), procesar lo que se pueda y preguntar al usuario solo lo estrictamente necesario para completar.
