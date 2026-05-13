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

## Controles base

| Accion | Tecla |
|---|---|
| Mover | Flechas |
| Disparar | Espacio |
| Pausar | P |
| Volver al menu | Escape |
| Iniciar partida | Enter |

Los controles extendidos se configuran en `config/controls.json`.

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

## Equipo - Grupo 15

| Nombre | Correo |
|---|---|
| Tomas Velasquez | t.velasquezd@uniandes.edu.co |
| Sergio Castano | sa.castanoa1@uniandes.edu.co |
| John Casallas | j.casallasp@uniandes.edu.co |

Actualizar esta tabla cuando quede registrado el cuarto integrante.
