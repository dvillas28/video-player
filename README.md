# Video Selector Player :tv:
- Carga una playlist de videos que pueden ser reproducidos y cambiar de uno a otro con solo presionar una tecla :keyboard:

- Necesita un archivo `.txt` que contiene los *paths* de los videos a cargar. El path a este archivo debe ser ingresado como argumento

## Ejecución
```
python3 video_selector_player.py <path/to/playlist.txt>
```
## Controles
- Reproducir videos presionando una tecla numerica (`0`-`9`)

- `X` : para pausar reproductor
- `C` : para reanudar reproductor
- `space` : el video y cerrar el reproductor
- `Z` : cerrar programa

## TODOs ordenados por prioridad
- Capacidad de reproducir un video predeterminado de fondo
- Hasta el momento solo se pueden acceder los primeros 10 videos (teclas 0-9)
- Mantener Focus en el central Widget

## TODOs Listos
- Hacerlo frameless de algun modo ✅
- Colocar imagen predeterminada de fondo ✅
- Cuando un video termina, el reproductor se cierra ✅
