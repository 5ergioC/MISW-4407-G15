# Defender - Grupo 15

Proyecto final de MISW-4407. El objetivo es construir un clon funcional de Defender en Python, usando Pygame y una arquitectura ECS como base principal del codigo.

## Ejecucion local

Requisitos:

- Python 3.11 o superior.
- `pygame-ce`.
- `esper`.

Instalacion:

```bash
pip install -r requirements.txt
```

Ejecucion:

```bash
python main.py
```

## Controles

| Accion | Tecla |
|---|---|
| Mover nave | Flechas / WASD |
| Disparar laser | Espacio |
| Smart bomb | B |
| Pausar | P |
| Debug overlay | F1 |
| Volver al menu | Escape |
| Iniciar partida | Enter / Espacio |

Los controles se configuran en `config/controls.json`.

## Decisiones tecnicas

- El render interno usa una resolucion virtual de `320x256`, escalada por ventana.
- La logica del juego se organiza mediante ECS: entidades como IDs, componentes como datos y sistemas como comportamiento.
- Las escenas controlan el flujo general: menu, juego, game over y victoria.
- Los recursos compartidos se acceden mediante `ServiceLocator`.
- Los parametros de gameplay viven en JSON dentro de `config/`.
- Los bonos viven separados en subcarpetas `bonus/` para no mezclar el MVP obligatorio con extras.

## Estructura del proyecto

```text
main.py
requirements.txt
assets/
  fnt/
  img/
  snd/
config/
docs/
src/
  commands/
  components/
  core/
  engine/
  factories/
  scenes/
  systems/
```

## Estado del cascaron

El proyecto ya cuenta con:

- Game loop principal.
- Escenas base.
- Servicio de configuracion, imagenes, sonidos y textos.
- Componentes ECS iniciales.
- Sistemas base conectados en la escena de juego.
- Configuraciones para ventana, mundo, jugador, enemigos, olas, audio, puntaje, debug y publicacion.
- Assets base de imagenes, fuentes y sonidos.

Varias mecanicas avanzadas estan marcadas con `TODO(P1)`, `TODO(P2)`, `TODO(P3)` o `TODO(P4)` para facilitar el trabajo por responsabilidades.

## Bonos implementados

- **Minimapa** — barra superior muestra jugador, enemigos y astronautas en tiempo real. Astronautas capturados parpadean en rojo.
- **Flecha de captura** — flecha roja aparece en el borde de pantalla apuntando al astronauta capturado fuera de camara.
- **Smart bomb** — tecla B elimina todos los enemigos visibles. Se recupera una bomba cada 10 000 puntos.
- **Vidas extra** — se otorga una vida adicional cada 10 000 puntos (maximo 5).
- **High score persistente** — tabla de 5 entradas guardada en `config/highscore.json`. Puntaje inicial: 21 270.
- **Nombre en tabla** — entrada estilo arcade (3 caracteres, flechas arriba/abajo para letras) al superar la tabla.
- **Texto dinamico a colores** — score, titulos y textos de escena cambian de color ciclicamente.
- **Modo atraccion** — tras 15 segundos en el menu aparece una pantalla animada con instrucciones. Cualquier tecla regresa al menu.
- **Vista de depuracion** — F1 activa overlay con colisiones, estados de IA y posicion de camara.

## Assets

```
assets/
  fnt/  — fuentes pixel (defender.ttf, PressStart2P.ttf)
  img/  — sprites del juego (jugador, enemigos, astronauta, HUD, flash de explosion)
  snd/  — sonidos en formato OGG
```

Los volumenes se configuran en `config/audio.json` (`master_volume`, `sfx_volume`).

## Configuracion rapida

| Archivo | Que controla |
|---|---|
| `config/window.json` | Resolucion, framerate, titulo |
| `config/player.json` | Fisica, vidas, bombas, velocidad laser |
| `config/enemies.json` | Velocidad y comportamiento de enemigos |
| `config/waves.json` | Olas y spawn de enemigos por nivel |
| `config/scoring.json` | Puntos por evento |
| `config/audio.json` | Rutas de sonido y volumen |
| `config/highscore.json` | Tabla de puntajes maximos |
| `config/debug.json` | Opciones de depuracion y trampa |

## Modo depuracion

Con F1 durante el juego se activa el overlay de debug:

- **Verde** — colisiones de enemigos
- **Rojo** — colision del jugador
- **Cyan** — estado de IA sobre cada entidad (e.g. `LAN idle`, `AST captured`)
- Posicion de camara en esquina superior izquierda

Trampa adicional disponible en `config/debug.json` (`cheats.enabled`).

## Publicacion

Pendiente — se publicara en itch.io al finalizar el proyecto.
URL: TBD

## Equipo - Grupo 15

| Nombre | Correo |
|---|---|
| Tomas Velasquez | t.velasquezd@uniandes.edu.co |
| Sergio Castano | sa.castanoa1@uniandes.edu.co |
| John Casallas | j.casallasp@uniandes.edu.co |

Actualizar esta tabla cuando quede registrado el cuarto integrante.
