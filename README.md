# Video Selector Player
- Carga una playlist de videos que pueden ser reproducidos y cambiar de uno a otro con solo presionar una tecla

- Necesita un archivo `.txt` que contiene los *paths* de los videos a cargar. El path a este archivo debe ser ingresado como argumento

## Ejecución
```
python3 video_selector_player.py <path/to/playlist.txt>
```
## Controles
- Reproducir videos presionando una tecla numerica (`0`-`9`)

- `X` para pausar, `C` para reanudar y `Z` para cerrar programa

## TODOs
- Colocar imagen predeterminada de fondo
- Capacidad de reproducir un video predeterminado de fondo
- Hacerlo frameless de algun modo
- Hasta el momento solo se pueden acceder los primeros 10 videos (teclas 0-9)