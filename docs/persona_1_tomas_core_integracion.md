# Persona 1 - Tomas - Core, arquitectura ECS e integracion

## Proposito del rol

Este rol tiene la responsabilidad principal de que el proyecto sea aceptable desde el punto de vista arquitectonico. La rubrica exige que ECS sea la base del juego; por eso esta persona debe actuar como integrador tecnico, mantener el game loop estable, cuidar que los sistemas no se vuelvan clases monoliticas y asegurar que las demas partes puedan conectarse sin romper escenas, servicios o configuraciones.

Este rol queda intencionalmente un poco mas cargado porque sera iterado rapido por Tomas. Las tareas incluyen codigo, documentacion tecnica, criterios de integracion y revision de completitud contra el enunciado.

## Objetivos evaluables cubiertos

- Arquitectura ECS obligatoria.
- Game loop.
- Patron Scene.
- Patron Service Locator.
- Archivos de configuracion.
- Pausa global.
- Wraparound base.
- Camara del jugador, al menos en version MVP centrada.
- Integracion de sistemas de jugador, enemigos, astronautas, HUD, audio y escenas.
- Preparacion de publicacion junto con Persona 4.
- Evidencia tecnica para documento grupal y video.

## Rutas bajo responsabilidad principal

Estas rutas son propiedad principal de Persona 1. Otros integrantes pueden tocarlas solo coordinando antes:

```text
main.py
src/core/
src/engine/service_locator.py
src/engine/services/
src/scenes/
src/states/
src/systems/wraparound_system.py
src/systems/movement_system.py
src/systems/player_movement_system.py
src/systems/background_system.py
src/systems/planet_system.py
config/window.json
config/world.json
config/player.json
config/controls.json
config/debug.json
docs/PRD_Defender_ECS_Pygame.md
```

## Rutas compartidas con revision obligatoria

```text
src/factories/entity_factory.py
src/systems/render_system.py
src/systems/hud_system.py
src/systems/audio_system.py
config/scoring.json
config/waves.json
README.md
```

## Entregables de codigo

### 1. Game loop estable

Debe asegurar que `GameEngine`:

- Inicialice Pygame y servicios una sola vez.
- Use resolucion logica `320x256` y escalado pixel-perfect.
- Calcule `dt` a partir del reloj.
- Delegue eventos, update y render a la escena activa.
- Permita transiciones limpias entre menu, juego, game over y victoria.
- No deje escenas antiguas actualizando luego del cambio.

### 2. ECS real y defendible

Debe garantizar que:

- Las entidades sean IDs de `esper`, no clases con logica.
- Los componentes sean datos simples.
- La logica viva en sistemas.
- Las fabricas solo creen entidades y ensamblen componentes.
- Los sistemas puedan explicarse en el video y documento.
- Ninguna entidad principal tenga metodos tipo `update()` con logica completa.

Checklist minimo de entidades ECS:

- PlayerShip.
- Lander.
- Mutant.
- Astronaut.
- PlayerLaser.
- EnemyBullet.
- EnemyMissile.
- Particle.
- Star.
- Planet/terrain data.
- Indicators o minimap markers.

### 3. Escenas y flujo de juego

Debe mantener estas escenas:

- `MenuScene`: titulo, instrucciones, iniciar con Enter.
- `PlayScene`: partida activa, pausa, gameplay.
- `GameOverScene`: derrota por jugador o astronautas.
- `WinScene`: victoria del nivel.

Si se implementa bono de high score o modo atraccion, coordinar con Persona 4 para agregar:

- `HighScoreScene`.
- `AttractScene`.

### 4. Pausa global

Debe implementar o validar:

- Tecla `P` para alternar pausa.
- Texto `PAUSED` parpadeante.
- Fondo visible durante pausa.
- Jugador, enemigos y proyectiles invisibles durante pausa.
- Sistemas de jugador, enemigos, proyectiles, colision y lifetime congelados.
- Audio de pausa opcional sin parpadeos de pantalla completa.

### 5. Mundo, camara y wraparound

Debe dejar listo:

- Mundo horizontal finito definido por config.
- Wraparound horizontal para jugador, enemigos, astronautas y proyectiles.
- Wraparound vertical para enemigos.
- Bloqueo vertical para jugador.
- Camara MVP centrada en jugador o jugador centrado en pantalla.
- Preparacion para camara bono: offset segun direccion del jugador.
- Render sin saltos visuales fuertes cerca de bordes del mundo.

### 6. Configuracion transversal

Debe mantener estos archivos de configuracion cargables desde `ServiceLocator.config`:

```text
config/window.json
config/world.json
config/player.json
config/controls.json
config/debug.json
```

Debe revisar que los demas roles usen configuracion en vez de numeros magicos cuando aplique.

## Entregables documentales

Persona 1 debe mantener en el PRD o README:

- Diagrama o descripcion de flujo: Engine -> Scene -> Systems -> ECSWorld.
- Lista final de componentes.
- Lista final de sistemas.
- Explicacion de patrones: ECS, Game Loop, Scene, Service Locator, Command, State.
- Riesgos abiertos y estado de cumplimiento de la rubrica.
- Instrucciones locales para ejecutar el juego.

## Criterios de aceptacion propios

Una tarea de este rol se considera terminada cuando:

- El juego abre desde `python main.py`.
- Se puede ir de menu a juego.
- Se puede pausar y reanudar.
- Se puede volver a menu desde game over o victoria.
- El juego no rompe por ausencia de configs nuevas.
- La arquitectura puede explicarse sin contradicciones con el codigo.
- La matriz de rubrica no tiene requisitos sin dueño.

## Dependencias con otros roles

- Persona 2 necesita que el loop y escenas esten estables para probar jugador, laser, colisiones y HUD.
- Persona 3 necesita fabricas y sistemas conectados para Landers, Mutants y astronautas.
- Persona 4 necesita acceso claro a render, audio, assets, minimapa y publicacion.

## Reglas de coordinacion

- Si otro rol necesita modificar `PlayScene`, debe avisar que sistema va a registrar y que orden de update necesita.
- Si un componente nuevo se comparte entre dos roles, Persona 1 valida nombre, datos y ubicacion.
- Si hay un valor de gameplay que se ajusta mas de una vez, debe moverse a `config/*.json`.
- Si una mecanica se implementa fuera de ECS por urgencia, debe quedar marcada como deuda y corregirse antes de entrega.

## Checklist de rubrica asignada

- [ ] ECS aplicado en la mayoria del proyecto.
- [ ] Game loop estable.
- [ ] Patron Scene implementado.
- [ ] Service Locator activo para configs, imagenes, sonidos y textos.
- [ ] Configuraciones JSON utilizadas.
- [ ] Menu principal funcional.
- [ ] Pausa funcional con invisibilidad de entidades requeridas.
- [ ] Wraparound correcto.
- [ ] Camara MVP o bono.
- [ ] README con ejecucion y controles.
- [ ] Documento grupal con arquitectura.
- [ ] Evidencia para video de presentacion.

