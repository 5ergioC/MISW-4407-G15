# PRD de Software — Clon de Defender con Pygame + ECS

## 1. Resumen ejecutivo

El proyecto consiste en desarrollar una reproducción fiel del videojuego arcade **Defender** usando **Python, Pygame y arquitectura ECS**. El foco principal no es crear un juego inspirado en Defender, sino una aproximación lo más exacta posible dentro del alcance académico: resolución original, comportamiento de entidades, movimiento con inercia, wraparound, rescate de astronautas, Landers, Mutants, disparos, partículas, sonido, puntaje, pausa, menú, game over, pantalla de victoria y publicación en un portal como itch.io.

La arquitectura ECS es un requisito obligatorio de aceptación. El proyecto debe estar diseñado para que la lógica de juego se distribuya entre entidades, componentes y sistemas, evitando una implementación monolítica basada en herencia profunda o clases gigantes.

---

## 2. Objetivos del producto

### 2.1 Objetivo principal

Construir un clon jugable de Defender en Pygame que cumpla todos los requerimientos obligatorios de la rúbrica y que esté preparado para bonificaciones mediante una arquitectura extensible basada en ECS, archivos de configuración y escenas.

### 2.2 Objetivos académicos

El proyecto debe demostrar dominio de:

- Game loop.
- Arquitectura ECS.
- Matemáticas aplicadas a videojuegos.
- Colisiones básicas.
- Patrón Command para input.
- Game feel.
- Sprites, texturas y animación 2D cuadro a cuadro.
- Patrón State para IA de entidades.
- Administración de recursos con Service Locator.
- Escenas de juego.
- Despliegue web o escritorio.

### 2.3 Objetivos de fidelidad

El juego debe parecerse a Defender en:

- Resolución base de 320x256 píxeles.
- Movimiento horizontal con mundo largo y wraparound.
- Nave con inercia.
- Láser horizontal que atraviesa enemigos visibles.
- Fondo de estrellas con paralaje.
- Planeta procedural hecho con líneas.
- Landers que raptan astronautas.
- Mutants derivados de Landers que completan el rapto.
- HUD superior con puntaje, vidas y/o indicadores.
- Sonidos, explosiones y animaciones de estilo arcade.

---

## 3. Alcance del producto

### 3.1 Alcance obligatorio — MVP evaluable al 100%

El MVP debe incluir:

1. Menú principal con título e instrucciones.
2. Game loop estable.
3. Arquitectura ECS aplicada en la mayoría del proyecto.
4. Sistema de escenas.
5. Sistema de recursos mediante Service Locator.
6. Sistema de input basado en Command.
7. Sistema de fondo de estrellas animadas.
8. Planeta procedural de líneas.
9. Paralaje entre estrellas, mundo y planeta.
10. Nave del jugador con movimiento por teclado y/o mouse, con inercia.
11. Disparo láser del jugador con teclado.
12. Láser que atraviesa enemigos en pantalla, sin afectar entidades fuera de cámara.
13. Astronautas en el suelo que se desplazan levemente.
14. Landers con movimiento, disparo ocasional y captura de astronautas.
15. Mutants creados cuando un Lander completa el rapto.
16. Sistema de wraparound horizontal para mundo, jugador, enemigos y personajes.
17. Wraparound vertical para enemigos, no para jugador.
18. Rescate de astronautas cuando el Lander muere.
19. Astronautas que caen por gravedad y pueden morir al impactar desde gran altura.
20. Entrega de astronautas en el suelo con puntaje.
21. Balas enemigas y misiles pequeños ocasionales.
22. Colisiones entre:
    - Láser del jugador y enemigos.
    - Láser del jugador y balas enemigas.
    - Láser del jugador y astronautas.
    - Balas enemigas y jugador.
23. Pausa con tecla, texto PAUSED parpadeante y ocultamiento de jugador, enemigos y proyectiles.
24. Fanfare inicial al comenzar el juego.
25. Explosiones de partículas para entidades destruidas.
26. HUD con puntaje y vidas.
27. Game Over cuando muere el jugador o cuando no quedan astronautas.
28. Pantalla de victoria al completar el nivel.
29. Sonidos y animaciones requeridas.
30. Publicación en itch.io, GameJolt, Newgrounds o equivalente.
31. Repositorio GitHub público con tag final.
32. Código fuente coherente con la versión publicada.

### 3.2 Alcance recomendado de bonificación

Se recomienda priorizar estas bonificaciones porque elevan la nota y fortalecen la arquitectura:

1. Minimapa superior.
2. Cámara correcta del jugador.
3. Sistema de vidas configurable.
4. Smart bomb configurable.
5. High score persistente.
6. Múltiples olas configurables en JSON.
7. Texto dinámico a colores.
8. Modo atracción.
9. Vista de depuración.
10. Inputs con gamepad.

### 3.3 Fuera de alcance inicial

No se considera necesario para la primera versión:

- Reproducir parpadeos de pantalla completa por seguridad.
- Implementar absolutamente todos los enemigos del Defender original.
- Juego a dos jugadores.
- Editor de niveles completo.
- Fase dos del mundo destruido.
- Ejecutables para macOS.

Estos elementos pueden implementarse solo si el MVP obligatorio está completo.

### 3.4 Complemento operativo para equipo de 4 personas

La ejecucion del proyecto queda dividida en cuatro frentes de trabajo. Cada frente tiene un markdown propio con responsabilidades, rutas principales, rutas compartidas, criterios de aceptacion y checklist de rubrica.

| Persona | Documento | Responsabilidad principal |
|---|---|---|
| Persona 1 - Tomas | `docs/persona_1_tomas_core_integracion.md` | Core, arquitectura ECS, escenas, game loop, integracion, configuracion, pausa, wraparound y control de completitud |
| Persona 2 | `docs/persona_2_gameplay_jugador_colisiones_hud.md` | Jugador, input Command, laser, colisiones, puntaje, HUD, Game Over y victoria |
| Persona 3 | `docs/persona_3_enemigos_astronautas_ia.md` | Landers, Mutants, astronautas, rapto, IA con State, proyectiles enemigos y spawn por olas |
| Persona 4 | `docs/persona_4_assets_audio_minimapa_publicacion_bonos.md` | Assets, audio, particulas, minimapa, bonos, README, publicacion y material visual |

Regla de trabajo: cada integrante debe programar y dejar evidencia en Git. El documento individual no reemplaza commits, issues ni pruebas manuales; sirve como contrato de ownership para evitar choques y asegurar que cada aspecto del enunciado tenga responsable.

### 3.5 Fuentes y referencias del enunciado

Estas referencias deben usarse durante implementacion, ajuste de game feel y defensa del proyecto:

- Emulador recomendado para jugar y analizar Defender: `https://online-emulators.com/snes/Williams_Arcade's_Greatest_Hits_(USA)`
- Guia de mecanicas base: `https://gamefaqs.gamespot.com/arcade/584162-defender/faqs/25139`
- Recursos oficiales del curso: `https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/`
- Generador recomendado de sonidos sencillos: `https://sfxr.me/`

Los parpadeos de pantalla completa no deben implementarse. Si se necesitan efectos de impacto, deben limitarse a entidades, particulas, audio o efectos visuales localizados.

---

## 4. Usuarios objetivo

### 4.1 Evaluadores del curso

Necesitan verificar rápidamente que el proyecto cumple el enunciado, la arquitectura, la rúbrica y los patrones solicitados.

### 4.2 Jugadores casuales

Necesitan entender cómo iniciar, moverse, disparar, rescatar astronautas y reconocer el estado del juego.

### 4.3 Equipo desarrollador

Necesita una arquitectura clara, modular y extensible para dividir trabajo entre integrantes y mantener trazabilidad en GitHub.

---

## 5. Requisitos funcionales detallados

## RF-01 — Menú principal

**Descripción:** El juego debe iniciar en una escena de menú con título, logo o texto principal e instrucciones para comenzar.

**Criterios de aceptación:**

- Se muestra el título del juego.
- Se muestran instrucciones de input básico.
- El jugador puede iniciar una partida con una tecla definida, por ejemplo ENTER.
- El menú usa fuente pixel o estética arcade.
- Desde Game Over o victoria se puede volver al menú.

**Prioridad:** Obligatoria.

---

## RF-02 — Game loop

**Descripción:** El juego debe implementar un loop principal que gestione eventos, input, actualización, renderizado, audio y cambio de escenas.

**Criterios de aceptación:**

- El juego corre a FPS estable definido por configuración.
- El delta time se usa para movimiento independiente del rendimiento.
- La escena activa recibe update y render.
- El loop puede pausar la actualización de sistemas activos cuando el juego está pausado.

**Prioridad:** Obligatoria.

---

## RF-03 — Arquitectura ECS

**Descripción:** La mayoría de entidades del juego deben componerse mediante componentes de datos y procesarse mediante sistemas.

**Criterios de aceptación:**

- Existen entidades para jugador, Landers, Mutants, astronautas, proyectiles, partículas, estrellas, planeta y efectos.
- Los componentes almacenan datos, no lógica compleja.
- Los sistemas ejecutan la lógica de movimiento, render, colisión, IA, input, audio, partículas, cámara, HUD y escenas.
- El código evita clases monolíticas como `Player.update_all_game_logic()`.
- La documentación final explica componentes, sistemas y decisiones.

**Prioridad:** Bloqueante.

---

## RF-04 — Fondo de estrellas animado

**Descripción:** El fondo debe contener estrellas dibujadas y animadas que se mueven con sensación de profundidad.

**Criterios de aceptación:**

- Hay varias estrellas distribuidas en el mundo.
- Las estrellas se mueven con paralaje respecto a la cámara.
- El movimiento recuerda al juego original.
- Las estrellas no afectan colisiones.

**Prioridad:** Obligatoria.

---

## RF-05 — Planeta procedural de líneas

**Descripción:** El terreno del planeta debe generarse mediante líneas, con variación aleatoria por partida.

**Criterios de aceptación:**

- El planeta se dibuja como una polilínea.
- Cada nueva partida genera una silueta distinta.
- El planeta se mueve con paralaje diferente al fondo.
- Jugador y enemigos no colisionan con el planeta.
- Los astronautas usan la línea del planeta como suelo.

**Prioridad:** Obligatoria.

---

## RF-06 — Movimiento de jugador con inercia

**Descripción:** La nave del jugador debe moverse usando teclado y/o mouse, con aceleración, desaceleración e inercia.

**Criterios de aceptación:**

- El jugador puede moverse en X e Y.
- El movimiento no es instantáneo; usa aceleración y fricción.
- El jugador no hace wrap vertical.
- Si no se implementa cámara avanzada, la nave se mantiene cerca del centro de pantalla.
- La dirección visual del sprite coincide con la dirección de movimiento horizontal.

**Prioridad:** Obligatoria.

---

## RF-07 — Disparo láser del jugador

**Descripción:** El jugador dispara un láser horizontal con teclado.

**Criterios de aceptación:**

- El láser atraviesa todos los enemigos visibles en pantalla.
- El láser no afecta entidades fuera de pantalla.
- El láser puede destruir enemigos, balas enemigas y astronautas accidentalmente.
- El disparo tiene sonido.
- El disparo tiene duración corta o cooldown configurable.

**Prioridad:** Obligatoria.

---

## RF-08 — Astronautas

**Descripción:** Deben existir astronautas en el suelo, con movimiento leve y posibilidad de ser capturados, rescatados o muertos.

**Criterios de aceptación:**

- Los astronautas aparecen bajo la línea del planeta.
- Se desplazan levemente en el suelo.
- Pueden ser capturados por Landers.
- Pueden caer con gravedad si el Lander muere.
- Mueren si caen desde una altura excesiva.
- El jugador puede recogerlos y devolverlos al suelo para ganar puntos.

**Prioridad:** Obligatoria.

---

## RF-09 — Lander

**Descripción:** El Lander es el enemigo base. Debe moverse, disparar ocasionalmente y capturar astronautas.

**Criterios de aceptación:**

- Aparece progresivamente según el nivel.
- Se mueve de forma autónoma.
- Dispara al jugador si está en pantalla.
- Lanza balas y ocasionalmente misiles pequeños.
- Busca astronautas disponibles.
- Captura un astronauta y asciende.
- Al llegar arriba con astronauta, desaparece el astronauta y el Lander se transforma en Mutant.

**Prioridad:** Obligatoria.

---

## RF-10 — Mutant

**Descripción:** El Mutant es un enemigo agresivo generado tras un rapto exitoso.

**Criterios de aceptación:**

- Se crea cuando un Lander llega arriba con un astronauta.
- Persigue o presiona más agresivamente al jugador.
- Puede disparar.
- Usa wraparound horizontal y vertical.
- Puede ser destruido por el láser del jugador.

**Prioridad:** Obligatoria.

---

## RF-11 — Sistema de rapto y alerta

**Descripción:** Cuando un Lander captura un astronauta, el juego debe alertar al jugador.

**Criterios de aceptación:**

- Se reproduce un sonido de alerta.
- El estado del astronauta cambia a capturado.
- El Lander asciende con el astronauta.
- Se muestra flecha de dirección hacia el rapto o minimapa.
- Existe contador de enemigos si no se implementa minimapa.

**Prioridad:** Obligatoria.

---

## RF-12 — Wraparound

**Descripción:** El mundo debe ser largo pero finito, con repetición horizontal.

**Criterios de aceptación:**

- El jugador reaparece al otro lado al cruzar límites horizontales del mundo.
- Enemigos, astronautas, proyectiles y partículas relevantes usan wraparound horizontal.
- Enemigos también usan wraparound vertical.
- El jugador no usa wraparound vertical.
- La cámara y el render evitan saltos visuales bruscos.

**Prioridad:** Obligatoria.

---

## RF-13 — Proyectiles enemigos

**Descripción:** Los enemigos disparan balas y ocasionalmente misiles pequeños.

**Criterios de aceptación:**

- Las balas enemigas aparecen ocasionalmente durante el comportamiento base.
- Los misiles pequeños aparecen con menor frecuencia.
- Las balas colisionan con el jugador.
- Las balas pueden ser destruidas por el láser del jugador.
- Los proyectiles tienen vida útil o se eliminan al salir de rango.

**Prioridad:** Obligatoria.

---

## RF-14 — Colisiones

**Descripción:** El juego debe incluir colisiones funcionales entre proyectiles, enemigos, jugador y astronautas.

**Criterios de aceptación:**

- Láser del jugador impacta enemigos visibles.
- Láser del jugador impacta balas enemigas.
- Láser del jugador puede matar astronautas.
- Balas enemigas matan al jugador.
- El sistema genera eventos de daño, muerte, puntaje y partículas.

**Prioridad:** Obligatoria.

---

## RF-15 — Pausa

**Descripción:** El jugador puede pausar la partida con una tecla.

**Criterios de aceptación:**

- La tecla de pausa cambia entre juego activo y pausado.
- En pausa no se actualizan jugador, enemigos ni proyectiles.
- Jugador, enemigos y proyectiles se vuelven invisibles.
- El fondo permanece visible.
- Se muestra texto PAUSED parpadeante en el centro.

**Prioridad:** Obligatoria.

---

## RF-16 — Audio

**Descripción:** El juego debe reproducir sonidos coherentes con acciones importantes.

**Criterios de aceptación:**

- Hay fanfare al iniciar el nivel.
- Hay sonido de disparo del jugador.
- Hay sonido de disparo enemigo.
- Hay alerta de rapto.
- Hay sonido de explosión.
- Los sonidos funcionan en la versión publicada.
- Se recomienda formato OGG para web.

**Prioridad:** Obligatoria.

---

## RF-17 — Explosiones de partículas

**Descripción:** Las entidades destruidas deben generar explosiones de partículas.

**Criterios de aceptación:**

- Enemigos explotan con partículas usando colores asociados a cada enemigo.
- El jugador explota con partículas que inician blancas y cambian/funden a colores.
- Las partículas tienen velocidad, tiempo de vida y desvanecimiento.
- El sistema de partículas está implementado con ECS.

**Prioridad:** Obligatoria.

---

## RF-18 — HUD

**Descripción:** La parte superior de pantalla debe mostrar puntaje, vidas y estado necesario.

**Criterios de aceptación:**

- Se muestra puntaje actual.
- Se muestran vidas o estado del jugador.
- Se muestra contador de enemigos si no hay minimapa.
- El HUD no interfiere con el gameplay.
- Usa estética arcade/pixel.

**Prioridad:** Obligatoria.

---

## RF-19 — Game Over

**Descripción:** El juego debe mostrar Game Over cuando se cumplan condiciones de derrota.

**Criterios de aceptación:**

- Hay Game Over si el jugador muere por bala y no quedan vidas.
- Hay Game Over si todos los astronautas están muertos, desaparecidos o raptados.
- La escena permite reiniciar o volver al menú.
- Si hay sistema de vidas, se respeta antes de terminar la partida.

**Prioridad:** Obligatoria.

---

## RF-20 — Victoria

**Descripción:** El juego debe mostrar una pantalla de victoria al terminar el nivel implementado.

**Criterios de aceptación:**

- Se detecta cuando no quedan enemigos activos de la ola/nivel.
- Se muestra una escena o mensaje de victoria.
- El jugador puede continuar, reiniciar o volver al menú.

**Prioridad:** Obligatoria.

---

## RF-21 — Publicación

**Descripción:** El juego debe estar publicado en un portal web de juegos.

**Criterios de aceptación:**

- Existe URL pública del juego.
- El portal muestra descripción.
- El portal muestra pantallazo.
- La versión publicada coincide con el código fuente entregado.

**Prioridad:** Obligatoria.

---

## 6. Requisitos no funcionales

### 6.1 Rendimiento

- El juego debe apuntar a 60 FPS.
- Debe evitar caídas severas durante explosiones o muchos proyectiles.
- El número de entidades debe mantenerse controlado mediante pooling o eliminación por vida útil.

### 6.2 Resolución y escalado

- Resolución lógica base: 320x256.
- El juego puede escalarse a 2x, 3x o pantalla completa, pero el render interno debe conservar la lógica original.
- El escalado debe preservar estética pixel art.

### 6.3 Configurabilidad

Deben existir archivos de configuración para:

- Ventana y resolución.
- Vidas iniciales.
- Puntaje máximo inicial.
- Olas o niveles.
- Parámetros de enemigos.
- Parámetros del jugador.
- Parámetros de audio.
- Controles.

### 6.4 Seguridad visual

- No se implementarán parpadeos de pantalla completa.
- Los efectos de flash deben limitarse a entidades, partículas o audio.

### 6.5 Mantenibilidad

- El código debe estar separado por módulos.
- Cada sistema debe tener responsabilidad clara.
- Las configuraciones deben evitar valores mágicos en el código.
- Debe existir README con instrucciones de ejecución y controles.

### 6.6 Portabilidad

- El juego debe correr en escritorio con Python.
- La publicación ideal es web usando `pygbag`.
- Los sonidos deben estar en formato compatible con web, preferiblemente OGG.

---

## 7. Arquitectura propuesta

### 7.1 Estructura de carpetas sugerida

```text
project/
  main.py
  requirements.txt
  README.md
  pyproject.toml
  assets/
    sprites/
    audio/
    fonts/
  config/
    window.json
    player.json
    enemies.json
    waves.json
    scoring.json
    controls.json
    highscore.json
  src/
    core/
      game.py
      scene_manager.py
      service_locator.py
      event_bus.py
      resource_manager.py
      config_loader.py
    ecs/
      world.py
      entity.py
      component.py
      system.py
    components/
      transform.py
      velocity.py
      sprite.py
      animation.py
      collider.py
      health.py
      player_control.py
      enemy_ai.py
      astronaut.py
      projectile.py
      laser.py
      particle.py
      score_value.py
      wraparound.py
      camera_target.py
      audio_source.py
      state.py
    systems/
      input_system.py
      command_system.py
      movement_system.py
      camera_system.py
      wraparound_system.py
      render_system.py
      animation_system.py
      collision_system.py
      laser_system.py
      enemy_ai_system.py
      astronaut_system.py
      projectile_system.py
      particle_system.py
      hud_system.py
      audio_system.py
      pause_system.py
      spawn_system.py
      scoring_system.py
      minimap_system.py
      debug_system.py
    scenes/
      menu_scene.py
      gameplay_scene.py
      pause_overlay.py
      game_over_scene.py
      victory_scene.py
      high_score_scene.py
    commands/
      move_command.py
      fire_command.py
      pause_command.py
      smart_bomb_command.py
```

### 7.2 Entidades principales

#### PlayerShip

Componentes:

- TransformComponent
- VelocityComponent
- SpriteComponent
- AnimationComponent
- ColliderComponent
- PlayerControlComponent
- HealthComponent
- WraparoundComponent
- CameraTargetComponent
- AudioSourceComponent

#### Lander

Componentes:

- TransformComponent
- VelocityComponent
- SpriteComponent
- AnimationComponent
- ColliderComponent
- EnemyAIComponent
- HealthComponent
- WraparoundComponent
- ScoreValueComponent
- StateComponent

#### Mutant

Componentes:

- TransformComponent
- VelocityComponent
- SpriteComponent
- AnimationComponent
- ColliderComponent
- EnemyAIComponent
- HealthComponent
- WraparoundComponent
- ScoreValueComponent
- StateComponent

#### Astronaut

Componentes:

- TransformComponent
- VelocityComponent
- SpriteComponent
- AnimationComponent
- ColliderComponent
- AstronautComponent
- WraparoundComponent
- ScoreValueComponent
- StateComponent

#### PlayerLaser

Componentes:

- TransformComponent
- LaserComponent
- ColliderComponent
- LifetimeComponent
- OwnerComponent

#### EnemyBullet / EnemyMissile

Componentes:

- TransformComponent
- VelocityComponent
- SpriteComponent
- ColliderComponent
- ProjectileComponent
- LifetimeComponent
- WraparoundComponent

#### Particle

Componentes:

- TransformComponent
- VelocityComponent
- ParticleComponent
- LifetimeComponent
- ColorComponent

#### Star

Componentes:

- TransformComponent
- StarComponent
- ParallaxComponent
- RenderLayerComponent

#### PlanetSegment

Componentes:

- PlanetLineComponent
- ParallaxComponent
- RenderLayerComponent

### 7.3 Sistemas principales

#### InputSystem

Lee eventos de Pygame y traduce entradas a comandos.

#### CommandSystem

Ejecuta comandos como mover, disparar, pausar, smart bomb o confirmar menú.

#### MovementSystem

Actualiza posiciones usando velocidad, aceleración y delta time.

#### PlayerControlSystem

Aplica inercia, aceleración, fricción y límites verticales al jugador.

#### CameraSystem

Controla la posición de cámara. En MVP puede mantener al jugador centrado; como bono, desplaza al jugador según dirección.

#### WraparoundSystem

Aplica repetición horizontal y vertical según entidad.

#### RenderSystem

Dibuja estrellas, planeta, sprites, láser, partículas, HUD y overlays.

#### AnimationSystem

Actualiza frames de sprites animados.

#### CollisionSystem

Detecta y emite eventos de colisión.

#### LaserSystem

Gestiona el disparo láser, duración, cooldown e impactos visibles.

#### EnemyAISystem

Controla Landers y Mutants mediante estados.

#### AstronautSystem

Controla estados del astronauta: caminando, capturado, cayendo, rescatado, depositado, muerto.

#### ProjectileSystem

Gestiona balas, misiles, vida útil y daño.

#### ParticleSystem

Actualiza partículas, color, vida útil y desaparición.

#### ScoringSystem

Suma puntos por destruir enemigos, rescatar astronautas y completar eventos.

#### SpawnSystem

Crea enemigos progresivamente según configuración de ola.

#### AudioSystem

Reproduce fanfare, disparos, explosiones y alertas.

#### PauseSystem

Congela sistemas activos y controla parpadeo del texto PAUSED.

#### HUDSystem

Renderiza puntaje, vidas, contador de enemigos y/o minimapa.

### 7.4 Estados de IA

#### Estados del Lander

```text
Patrol -> SeekAstronaut -> Abducting -> Ascending -> TransformToMutant
                  |              |
                  v              v
              AttackPlayer     DropAstronautOnDeath
```

#### Estados del Mutant

```text
Spawn -> ChasePlayer -> AttackPlayer -> EvadeOrReposition
```

#### Estados del Astronauta

```text
Walking -> Captured -> Falling -> CarriedByPlayer -> Deposited
       \                                      /
        -> Dead -----------------------------
```

---

## 8. Diseño de gameplay

### 8.1 Controles propuestos

| Acción | Tecla |
|---|---|
| Mover arriba | Flecha arriba / W |
| Mover abajo | Flecha abajo / S |
| Mover izquierda | Flecha izquierda / A |
| Mover derecha | Flecha derecha / D |
| Disparar láser | Espacio |
| Pausar | P |
| Smart bomb | B |
| Iniciar / confirmar | Enter |
| Volver / salir | Escape |
| Debug overlay | F1 |

### 8.2 Reglas de puntaje sugeridas

Los valores deben quedar en `config/scoring.json` para poder ajustarlos.

| Evento | Puntos sugeridos |
|---|---:|
| Destruir Lander | 150 |
| Destruir Mutant | 150 |
| Rescatar astronauta cayendo | 500 |
| Depositar astronauta en suelo | 500 |
| Completar nivel con astronautas vivos | Bonus configurable |

### 8.3 Condiciones de derrota

- El jugador recibe impacto de una bala o misil enemigo y no tiene vidas restantes.
- Todos los astronautas están muertos, desaparecidos o raptados.

### 8.4 Condiciones de victoria

- Se eliminan todos los enemigos requeridos de la ola/nivel.
- No hay eventos obligatorios pendientes que bloqueen el cierre de nivel.

---

## 9. Configuraciones requeridas

La carpeta `config/` debe mantenerse como fuente principal de parametros ajustables. Los archivos base quedan asi:

| Archivo | Responsable principal | Uso |
|---|---|---|
| `window.json` | Persona 1 | Resolucion, escalado, FPS y color base |
| `world.json` | Persona 1 / Persona 3 | Tamano de mundo, estrellas, planeta y limites |
| `player.json` | Persona 1 / Persona 2 / Persona 4 | Movimiento, vidas, laser y smart bombs |
| `controls.json` | Persona 1 / Persona 2 | Teclado, mouse opcional, gamepad opcional |
| `enemies.json` | Persona 3 | Parametros de Landers, Mutants, balas y misiles |
| `waves.json` | Persona 3 / Persona 4 | Olas configurables y dificultad |
| `scoring.json` | Persona 2 / Persona 3 | Puntajes por eventos |
| `interface.json` | Persona 4 | Fuente y colores del HUD |
| `audio.json` | Persona 4 | Mapeo de sonidos y volumenes |
| `highscore.json` | Persona 4 | Puntaje maximo inicial y tabla |
| `debug.json` | Persona 1 / Persona 4 | Overlays y accesos de prueba |
| `deployment.json` | Persona 4 / Persona 1 | Portal, build y evidencias de publicacion |

No se deben borrar llaves existentes en configs sin revisar el codigo actual que las consume. Si una mecanica nueva requiere ajuste frecuente, debe agregarse aqui antes de quedar hardcodeada.

### 9.1 `window.json`

```json
{
  "logical_width": 320,
  "logical_height": 256,
  "scale": 3,
  "fps": 60,
  "title": "Defender ECS"
}
```

### 9.2 `player.json`

```json
{
  "lives": 2,
  "acceleration": 520,
  "max_speed_x": 130,
  "max_speed_y": 100,
  "friction": 0.88,
  "laser_cooldown": 0.18,
  "smart_bombs": 3,
  "extra_life_score_interval": 10000
}
```

### 9.3 `waves.json`

```json
{
  "waves": [
    {
      "id": 1,
      "landers": 6,
      "mutants": 0,
      "astronauts": 10,
      "spawn_interval": 2.0,
      "enemy_fire_rate": 0.8,
      "missile_chance": 0.08
    }
  ]
}
```

### 9.4 `highscore.json`

```json
{
  "initial_high_score": 21270,
  "scores": [
    {
      "name": "AAA",
      "score": 21270
    }
  ]
}
```

---

## 10. Criterios de aceptación globales

El proyecto se considera listo para entrega cuando:

1. La versión publicada funciona sin errores bloqueantes.
2. El enlace público abre el juego o descarga correctamente el ejecutable.
3. El portal contiene descripción y pantallazo.
4. El repositorio GitHub tiene código actualizado y tag final.
5. El README explica instalación, ejecución, controles, cheats/debug y publicación.
6. La arquitectura ECS está presente y documentada.
7. El juego cumple todos los requerimientos obligatorios de la rúbrica.
8. El post-mortem grupal contiene resumen semanal, arquitectura, patrones y reflexión.
9. Cada integrante puede explicar su contribución técnica.
10. El video de presentación cubre juego, equipo, roles, ECS, componentes, sistemas, configuraciones y patrones.

---

## 11. Matriz de trazabilidad contra rúbrica

| Rúbrica / requisito | Implementación propuesta | Prioridad |
|---|---|---|
| Juego publicado con descripción y pantalla | Deploy en itch.io con README y capturas | Obligatoria |
| Menú principal | MenuScene | Obligatoria |
| Fondo de estrellas y planeta | StarSystem + PlanetSystem | Obligatoria |
| Movimiento y disparo | PlayerControlSystem + LaserSystem | Obligatoria |
| Spawn Landers y astronautas | SpawnSystem + AstronautSystem | Obligatoria |
| Wraparound | WraparoundSystem | Obligatoria |
| Rapto + Mutant | EnemyAISystem + StateComponent | Obligatoria |
| Balas enemigas | ProjectileSystem | Obligatoria |
| Colisiones | CollisionSystem | Obligatoria |
| Pausa | PauseSystem + PauseOverlay | Obligatoria |
| Fanfare | AudioSystem | Obligatoria |
| Puntaje | HUDSystem + ScoringSystem | Obligatoria |
| Contador/flecha o minimapa | HUDSystem o MinimapSystem | Obligatoria / Bono |
| Explosiones | ParticleSystem | Obligatoria |
| Game Over | GameOverScene | Obligatoria |
| Animaciones y sonidos | AnimationSystem + AudioSystem | Obligatoria |
| ECS | World + Components + Systems | Bloqueante |
| Game loop | Game core | Obligatoria |
| Command | commands/ + CommandSystem | Obligatoria |
| State | StateComponent + AI states | Obligatoria |
| Service Locator | service_locator.py | Obligatoria |
| Escenas | SceneManager | Obligatoria |
| Configuración | config/*.json | Obligatoria |

---

## 12. Roadmap de desarrollo recomendado

### Semana 1 — Base técnica y vertical slice

**Objetivo:** tener una escena jugable mínima.

Tareas:

- Crear estructura del proyecto.
- Implementar game loop.
- Implementar ECS básico.
- Implementar SceneManager.
- Implementar Service Locator.
- Cargar configuración de ventana.
- Dibujar fondo de estrellas.
- Crear jugador con movimiento inercial.
- Implementar disparo básico.
- Crear README inicial.

**Resultado esperado:**

- Se puede abrir el juego, ver menú, iniciar partida, mover nave y disparar.

### Semana 2 — Mundo, enemigos y colisiones

**Objetivo:** convertir el prototipo en gameplay Defender básico.

Tareas:

- Planeta procedural.
- Wraparound horizontal.
- Landers con IA básica.
- Astronautas en suelo.
- Colisiones de láser contra enemigos.
- Balas enemigas contra jugador.
- Explosiones de partículas.
- HUD de puntaje.

**Resultado esperado:**

- Se puede jugar una ola simple con enemigos, puntaje y muerte.

### Semana 3 — Rapto, Mutants, pausa y audio

**Objetivo:** completar mecánicas obligatorias complejas.

Tareas:

- IA del Lander para buscar y capturar astronautas.
- Transformación a Mutant.
- Astronautas cayendo y rescatables.
- Flecha de rapto o minimapa.
- Pausa con texto parpadeante.
- Fanfare y sonidos principales.
- Game Over y victoria.

**Resultado esperado:**

- El juego cumple el flujo principal obligatorio.

### Semana 4 — Pulido, publicación y documentación

**Objetivo:** cerrar entrega calificable.

Tareas:

- Animaciones finales.
- Ajuste de game feel.
- Configuración de olas.
- Bonos priorizados.
- Deploy en itch.io.
- Tag final en GitHub.
- Documento de arquitectura y post-mortem grupal.
- Post-mortems individuales.
- Video de presentación.

**Resultado esperado:**

- Entrega completa, publicada, documentada y defendible.

---

## 13. Priorización de backlog

### P0 — Bloqueante

- ECS real.
- Game loop.
- Menú.
- Jugador con movimiento y disparo.
- Landers.
- Astronautas.
- Wraparound.
- Colisiones.
- Game Over.
- Publicación.

### P1 — Obligatorio alto valor

- Rapto completo.
- Mutants.
- Partículas.
- Audio.
- Pausa.
- HUD.
- Planeta procedural.
- Paralaje.

### P2 — Bonos recomendados

- Minimapa.
- Cámara correcta.
- Vidas configurables.
- Smart bomb.
- High score.
- Varias olas configurables.

### P3 — Bonos avanzados

- Todos los enemigos.
- Fase dos.
- Modo atracción.
- Editor de niveles.
- Dos jugadores.
- Gamepad.

---

## 14. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| ECS superficial o mal aplicado | Proyecto puede no ser aceptado | Definir desde el inicio componentes y sistemas; documentar arquitectura |
| Scope creep por bonificaciones | No terminar MVP | Cerrar primero P0 y P1 |
| Movimiento poco fiel | Pérdida de puntos de fidelidad | Ajustar aceleración/fricción desde config |
| Rapto complejo | Retrasos | Implementar primero estados simples y luego pulir |
| Publicación web falla | Pérdida de puntos de entrega | Probar pygbag o ejecutable Windows con anticipación |
| Falta de contribución visible | Penalización grupal | Usar issues, commits y roles claros |
| Audio incompatible en web | Sonidos no funcionan | Usar OGG y probar build publicada |
| Explosiones costosas | Bajones de FPS | Limitar partículas y usar lifetime |

---

## 15. Roles sugeridos para equipo de 3 o 4 personas

### Equipo de 3

#### Integrante 1 — Core, ECS y escenas

- Game loop.
- ECS World.
- SceneManager.
- Service Locator.
- Config loader.
- Pausa.
- Deploy.

#### Integrante 2 — Gameplay jugador, colisiones y HUD

- Movimiento de jugador.
- Input Command.
- Láser.
- Colisiones.
- Puntaje.
- HUD.
- Game Over / victoria.

#### Integrante 3 — Enemigos, astronautas y efectos

- Landers.
- Mutants.
- Astronautas.
- Rapto.
- Partículas.
- Sonidos.
- Animaciones.

### Equipo de 4

Agregar un cuarto rol:

#### Integrante 4 — Pulido, herramientas y bonos

- Minimapa.
- Cámara correcta.
- Smart bomb.
- High score.
- Debug view.
- Modo atracción.
- Documentación visual y video.

---

## 16. Checklist final de entrega

### Juego publicado

- [ ] URL pública funcional.
- [ ] Descripción del juego en el portal.
- [ ] Pantallazo publicado.
- [ ] Juego corre desde el portal o descarga.
- [ ] Bonificaciones mencionadas en la descripción.

### Código fuente

- [ ] GitHub público.
- [ ] Tag final.
- [ ] README completo.
- [ ] Instrucciones de ejecución.
- [ ] Controles documentados.
- [ ] Cheats/debug documentados si existen.
- [ ] Configuraciones incluidas.
- [ ] Código corresponde a la versión publicada.

### Documento grupal

- [ ] Resumen semanal del proceso.
- [ ] Análisis arquitectónico.
- [ ] Componentes y sistemas explicados.
- [ ] Diagramas si es posible.
- [ ] Patrones usados.
- [ ] Reflexión: qué salió bien, mal y qué cambiaría.

### Documento individual

- [ ] Rol individual.
- [ ] Tareas específicas realizadas.
- [ ] Qué salió bien.
- [ ] Qué salió mal.
- [ ] Qué cambiaría.
- [ ] Aprendizajes sobre videojuegos.

### Presentación / video

- [ ] Presentación del juego.
- [ ] Presentación de integrantes.
- [ ] Roles individuales.
- [ ] Explicación ECS.
- [ ] Componentes creados.
- [ ] Sistemas creados.
- [ ] Configuraciones usadas.
- [ ] Patrones adicionales.
- [ ] Gameplay visible.

---

## 17. Definición de terminado

Una funcionalidad se considera terminada cuando:

1. Está implementada en una rama integrada a `main`.
2. Tiene configuración externa cuando aplica.
3. Funciona en build local.
4. No rompe otras escenas.
5. Está probada manualmente.
6. Está documentada en README o documento técnico si afecta arquitectura.
7. Se puede mostrar en el video final.

---

## 18. Recomendación estratégica

La estrategia más segura para maximizar nota es:

1. No iniciar bonos hasta que ECS, gameplay base, rapto, colisiones, pausa, HUD, audio, partículas, Game Over y publicación estén completos.
2. Implementar minimapa como primer bono, porque reemplaza contador/flecha y suma bonificación.
3. Implementar vidas configurables y smart bomb como segundo bloque de bonos, porque son contenidos acotados y visibles.
4. Implementar olas configurables si queda tiempo, porque refuerza configuración y presentación arquitectónica.
5. Preparar desde temprano el documento de arquitectura, no al final.

---

## 19. Glosario

- **ECS:** Entity Component System, arquitectura donde las entidades son identificadores, los componentes son datos y los sistemas procesan lógica.
- **Game loop:** ciclo principal que procesa eventos, actualiza estado y renderiza.
- **Command:** patrón para traducir inputs a acciones desacopladas.
- **State:** patrón para representar comportamientos como patrullar, capturar, caer o perseguir.
- **Service Locator:** patrón para acceder a servicios compartidos como recursos, audio y configuración.
- **Wraparound:** efecto donde una entidad reaparece por el lado opuesto del mundo al cruzar un límite.
- **Parallax:** movimiento relativo de capas para simular profundidad.
- **Fanfare:** sonido musical corto de inicio.
- **Mutant:** enemigo generado cuando un Lander completa el rapto de un astronauta.

---

## 20. Instrucción sugerida para agente de desarrollo

Usa este PRD como fuente principal de verdad para implementar el proyecto. Prioriza siempre los elementos P0 y P1 antes de trabajar en bonificaciones. Toda implementación debe respetar la arquitectura ECS, mantener configuraciones fuera del código cuando sea posible, y facilitar que el equipo pueda explicar componentes, sistemas, patrones y decisiones en el documento final y video de presentación.

Cuando generes código:

1. Mantén los componentes como estructuras de datos simples.
2. Coloca la lógica en sistemas.
3. Evita clases gigantes con demasiadas responsabilidades.
4. Usa archivos JSON de configuración.
5. Documenta decisiones relevantes en README o comentarios breves.
6. Asegura que el juego pueda ejecutarse localmente y prepararse para publicación.
7. No avances a bonos si hay requisitos obligatorios incompletos.
