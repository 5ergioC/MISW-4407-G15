# Persona 2 - Gameplay del jugador, disparos, colisiones y HUD

## Proposito del rol

Este rol se encarga de que el juego se sienta jugable y evaluable en pantalla. Debe implementar el movimiento de la nave, el laser del jugador, colisiones, puntaje, vidas, HUD, condiciones de derrota/victoria y parte importante del game feel.

La responsabilidad principal es que el evaluador pueda iniciar una partida, mover la nave con inercia, disparar, destruir o impactar entidades, ver puntaje/vidas y entender claramente el estado del juego.

## Objetivos evaluables cubiertos

- Movimiento de nave con teclado y/o mouse con inercia.
- Disparo laser con teclado.
- Laser que atraviesa enemigos visibles.
- Laser sin efecto fuera de pantalla.
- Colision de laser con enemigos, balas enemigas y astronautas.
- Colision de balas enemigas con jugador.
- HUD superior con puntaje, vidas y contador/minimapa segun integracion.
- Game Over cuando muere el jugador sin vidas.
- Game Over cuando todos los astronautas mueren o desaparecen, coordinado con Persona 3.
- Pantalla de victoria al completar nivel.
- Explosiones basicas al destruir entidades, coordinado con Persona 4.
- Patron Command aplicado a input.

## Rutas bajo responsabilidad principal

```text
src/commands/
src/components/player.py
src/components/laser.py
src/components/projectile.py
src/components/collider.py
src/components/score_value.py
src/components/lifetime.py
src/systems/input_command_system.py
src/systems/shooting_system.py
src/systems/collision_system.py
src/systems/projectile_system.py
src/systems/hud_system.py
src/systems/lifetime_system.py
src/scenes/game_over_scene.py
src/scenes/win_scene.py
config/player.json
config/scoring.json
config/controls.json
```

## Rutas compartidas con revision obligatoria

```text
src/scenes/play_scene.py
src/factories/entity_factory.py
src/systems/particle_system.py
src/systems/audio_system.py
src/components/astronaut.py
src/components/enemy.py
```

## Entregables de codigo

### 1. Input mediante Command

Debe garantizar que:

- Flechas y WASD puedan mapear movimiento.
- Espacio dispare laser.
- `P` pause usando comando existente.
- `Enter` confirme en menu.
- `Escape` vuelva o salga segun escena.
- Las teclas esten documentadas en `config/controls.json` y README.

El input no debe modificar entidades directamente desde el evento si puede evitarse. La intencion debe pasar por comandos y sistemas.

### 2. Movimiento del jugador con inercia

Debe implementar o ajustar:

- Aceleracion.
- Friccion/drag.
- Velocidad maxima.
- Movimiento en X e Y.
- Limite vertical para no hacer wrap vertical.
- Direccion visual segun movimiento horizontal.
- Sensacion de deslizamiento similar a Defender.

Valores ajustables:

```text
config/player.json
```

### 3. Laser del jugador

Debe implementar:

- Disparo con cooldown configurable.
- Direccion segun orientacion de nave.
- Laser horizontal o proyectil de duracion corta.
- Capacidad de atravesar varios enemigos visibles.
- Restriccion: no debe afectar entidades fuera de camara.
- Sonido `player_shoot`.
- Eliminacion por lifetime o fin de efecto.

Punto critico de rubrica: el laser puede destruir enemigos, balas enemigas y astronautas accidentalmente.

### 4. Sistema de colisiones

Debe cubrir como minimo:

- Laser del jugador contra Lander.
- Laser del jugador contra Mutant.
- Laser del jugador contra balas enemigas.
- Laser del jugador contra misiles enemigos.
- Laser del jugador contra astronautas.
- Bala/misil enemigo contra jugador.
- Jugador rescatando astronauta cayendo o depositable, coordinado con Persona 3.

Al detectar colision debe generar efectos segun corresponda:

- Puntaje.
- Audio.
- Particulas.
- Cambio de vida o Game Over.
- Eliminacion de entidad.
- Actualizacion de estado de astronauta o enemigo.

### 5. HUD y puntaje

Debe mostrar en la parte superior:

- Puntaje actual.
- Vidas.
- Contador de enemigos si no hay minimapa.
- Indicadores relevantes de smart bomb si Persona 4 implementa bono.
- Mensajes limpios sin tapar gameplay.

Valores de puntaje en:

```text
config/scoring.json
```

Eventos minimos:

- Destruir Lander.
- Destruir Mutant.
- Rescatar astronauta.
- Depositar astronauta.
- Bonus de nivel si aplica.

### 6. Game Over y victoria

Debe conectar:

- Derrota por impacto al jugador sin vidas restantes.
- Derrota cuando no quedan astronautas vivos/rescatables, coordinado con Persona 3.
- Victoria cuando no quedan enemigos activos ni pendientes de la ola, coordinado con Persona 3 y Persona 1.
- Escenas `GameOverScene` y `WinScene` con reinicio o retorno a menu.

Si se implementan vidas:

- La muerte del jugador reinicia el nivel o reposiciona jugador si quedan vidas.
- Al perder todas las vidas vuelve a Game Over y luego menu.

## Criterios de aceptacion propios

Una tarea de este rol esta terminada cuando:

- El jugador se mueve con inercia y no se siente instantaneo.
- El jugador dispara con cooldown.
- El laser afecta multiples objetivos visibles.
- Las colisiones principales se pueden demostrar manualmente.
- El HUD refleja puntaje y vidas reales.
- Game Over y victoria se disparan por condiciones reales, no por teclas de prueba.
- No hay logica pesada metida en componentes.

## Dependencias con otros roles

- Persona 1 define escena, loop, pausa, wraparound y camara.
- Persona 3 provee componentes/estados de enemigos y astronautas para colisionar.
- Persona 4 provee assets, audio, particulas pulidas y minimapa si se implementa.

## Reglas de coordinacion

- No cambiar nombres de componentes compartidos sin avisar.
- No borrar campos de config usados por codigo actual.
- Si se agrega un tipo de colision, documentarlo en este archivo y en la matriz de cumplimiento.
- Si se crea un evento de gameplay, dejar claro que sistema lo consume.

## Checklist de rubrica asignada

- [ ] Movimiento de nave con inercia.
- [ ] Disparo del jugador.
- [ ] Laser atraviesa enemigos visibles.
- [ ] Laser no afecta fuera de pantalla.
- [ ] Colisiones de laser con enemigos.
- [ ] Colisiones de laser con balas/misiles.
- [ ] Colisiones de laser con astronautas.
- [ ] Colisiones de balas enemigas con jugador.
- [ ] Puntaje visible.
- [ ] Vidas visibles.
- [ ] Game Over por muerte del jugador.
- [ ] Game Over por perdida total de astronautas, integrado con Persona 3.
- [ ] Victoria por completar nivel.
- [ ] Command usado para input.

