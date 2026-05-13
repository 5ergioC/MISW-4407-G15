# Persona 4 - Assets, audio, minimapa, publicacion y bonos

## Proposito del rol

Este rol se encarga de que el juego se vea, suene y se entregue como proyecto final. Tambien lidera los bonos mas visibles y acotados: minimapa, smart bomb, high score, texto dinamico, modo atraccion, debug view y publicacion web o descargable.

La responsabilidad principal es transformar el prototipo funcional en una entrega presentable, verificable y publicable.

## Objetivos evaluables cubiertos

- Estrellas y planeta con presentacion fiel, coordinado con Persona 1.
- Sonidos implementados.
- Fanfare al iniciar nivel.
- Explosiones de particulas con colores correctos.
- Animaciones de sprites donde aplique.
- Minimapa superior como bono y reemplazo de contador/flecha.
- Smart bomb como bono.
- High score persistente como bono.
- Texto dinamico a colores como bono.
- Varias olas configurables como bono, coordinado con Persona 3.
- Modo atraccion como bono si hay tiempo.
- Vista de depuracion como bono.
- Publicacion en itch.io, GameJolt, Newgrounds o equivalente.
- Descripcion, pantallazo y evidencia para entrega.
- Apoyo fuerte al README, video y post-mortem grupal.

## Rutas bajo responsabilidad principal

```text
assets/
src/components/audio_event.py
src/components/particle.py
src/components/renderable.py
src/systems/audio_system.py
src/systems/particle_system.py
src/systems/render_system.py
src/systems/background_system.py
src/systems/planet_system.py
src/systems/hud_system.py
config/audio.json
config/interface.json
config/highscore.json
config/deployment.json
config/debug.json
README.md
```

## Rutas para bonos

Estas rutas pueden crearse o ampliarse:

```text
src/commands/smart_bomb_command.py
src/scenes/high_score_scene.py
src/scenes/attract_scene.py
src/systems/minimap_system.py
src/systems/debug_system.py
src/systems/animation_system.py
src/systems/smart_bomb_system.py
src/systems/high_score_system.py
```

## Rutas compartidas con revision obligatoria

```text
src/scenes/play_scene.py
src/factories/entity_factory.py
src/systems/collision_system.py
src/systems/enemy_spawn_system.py
config/waves.json
config/player.json
config/scoring.json
```

## Entregables de codigo

### 1. Assets y render

Debe garantizar:

- Uso de sprites disponibles en `assets/img`.
- Uso de fuente pixel en `assets/fnt`.
- Render interno en `320x256`.
- HUD legible.
- Planeta de lineas visible.
- Estrellas animadas con paralaje.
- Sprites o formas temporales reemplazables sin romper ECS.
- Animaciones frame a frame cuando existan frames o sprites.

Si un sprite no esta listo, puede quedar una forma geometrica temporal, pero debe registrarse como deuda visual.

### 2. Audio

Debe implementar:

- Fanfare al iniciar nivel: `game_start.ogg`.
- Disparo del jugador: `player_shoot.ogg`.
- Disparo enemigo si se agrega asset o se reutiliza uno temporal.
- Alerta de captura: `lander_capture_astronaut.ogg`.
- Mutacion: `lander_mutate_astronaut.ogg`.
- Explosion enemigo: `enemy_die.ogg`.
- Muerte jugador: `player_die.ogg`.
- Game Over: `game_over.ogg`.
- Pausa: `game_paused.ogg`.

Los sonidos deben mapearse en:

```text
config/audio.json
```

Para publicacion web, priorizar OGG.

### 3. Particulas y explosiones

Debe implementar particulas para:

- Lander destruido.
- Mutant destruido.
- Bala o misil destruido si aplica.
- Astronauta muerto si aplica.
- Jugador destruido.

Criterios:

- Enemigos explotan con colores asociados a su sprite o tipo.
- Jugador empieza con particulas blancas y cambia/funde a colores.
- Particulas tienen velocidad, lifetime y desaparicion.
- No deben bajar FPS de forma severa.

### 4. Minimapa

Primer bono recomendado.

Debe mostrar:

- Posicion del jugador.
- Landers.
- Mutants.
- Astronautas.
- Astronautas capturados o en peligro.
- Mundo horizontal completo reducido en la parte superior.

Esto cubre tambien el requisito obligatorio de contador/flecha de rapto. Si no se termina minimapa, debe existir flecha de rapto o contador entregado por Personas 2 y 3.

### 5. Smart bomb

Bono recomendado.

Debe implementar:

- Tecla `B`.
- Cantidad inicial desde `config/player.json`.
- Elimina enemigos visibles en pantalla.
- No afecta enemigos fuera de camara.
- No debe matar astronautas, salvo que el equipo decida lo contrario y lo documente.
- Particulas y sonido.
- Recuperacion al alcanzar intervalos de 10000 puntos si se implementa.

### 6. High score

Bono recomendado.

Debe implementar:

- Puntaje maximo inicial 21270.
- Persistencia en `config/highscore.json` o archivo de usuario separado.
- Pantalla final para ingresar nombre si supera tabla.
- Visualizacion clara de tabla.

Nota tecnica: si la publicacion web limita escritura de archivos, documentar alternativa de persistencia por sesion o almacenamiento soportado.

### 7. Olas configurables

Debe apoyar a Persona 3 para tener al menos:

- Una ola obligatoria funcional.
- Cinco olas si se busca bono.
- O modo infinito con dificultad dinamica si el equipo decide perseguir ese bono adicional.

La fuente de verdad sera:

```text
config/waves.json
```

### 8. Publicacion

Debe preparar:

- Build web con `pygbag` o alternativa acordada.
- Publicacion en itch.io, GameJolt, Newgrounds o equivalente.
- Descripcion del juego en portal.
- Pantallazo.
- URL final.
- Confirmacion de que codigo fuente corresponde a lo publicado.
- Tag final de GitHub coordinado con Persona 1.

## Entregables documentales

Persona 4 debe liderar:

- Seccion de controles y assets del README.
- Seccion de publicacion.
- Capturas para portal y documento.
- Evidencia de bonos implementados.
- Guion visual del video.
- Checklist final de entrega.

## Criterios de aceptacion propios

Una tarea de este rol esta terminada cuando:

- El sonido asociado se reproduce en el evento correcto.
- Los assets cargan desde servicios, no con rutas sueltas por todo el codigo.
- Las particulas se ven y desaparecen correctamente.
- El minimapa o indicador obligatorio funciona.
- La publicacion abre o descarga correctamente.
- El portal tiene descripcion y pantallazo.
- Los bonos implementados son demostrables en gameplay.

## Dependencias con otros roles

- Persona 1 expone servicios, escenas, camara y config.
- Persona 2 genera eventos de disparo, colision, puntaje y muerte.
- Persona 3 genera eventos de rapto, mutacion, enemigos y estados de astronautas.

## Reglas de coordinacion

- No reemplazar assets sin revisar nombres usados por configs.
- No meter sonidos directamente en sistemas de gameplay si pueden pasar por `AudioEvent`.
- No activar bonos que rompan el MVP obligatorio.
- Documentar todo bono implementado en README y portal.
- Si una publicacion falla, dejar ruta alternativa descargable.

## Checklist de rubrica asignada

- [ ] Fanfare inicial.
- [ ] Sonidos principales.
- [ ] Animaciones o sprites donde aplique.
- [ ] Explosiones de particulas.
- [ ] Estrellas y planeta se ven pulidos.
- [ ] Minimapa o soporte visual equivalente.
- [ ] Smart bomb si hay tiempo.
- [ ] High score si hay tiempo.
- [ ] Texto dinamico a colores si hay tiempo.
- [ ] Cinco olas o modo infinito si hay tiempo.
- [ ] Debug view si hay tiempo.
- [ ] Modo atraccion si hay tiempo.
- [ ] Publicacion en portal.
- [ ] Descripcion y pantallazo del juego.
- [ ] README completo para entrega.
- [ ] Material visual para presentacion.

