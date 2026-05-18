# Persona 3 - Enemigos, astronautas, IA y rapto

## Proposito del rol

Este rol implementa el nucleo dramatico de Defender: Landers que buscan astronautas, los capturan, ascienden, mutan si completan el rapto y generan presion constante sobre el jugador. Tambien se encarga de los astronautas en suelo, su caida, rescate, muerte y deposito.

La responsabilidad principal es que el mundo tenga comportamiento autonomo y que las entidades usen estados claros, explicables y evaluables.

## Objetivos evaluables cubiertos

- Generacion progresiva de enemigos segun nivel u ola.
- Astronautas en el suelo con movimiento leve.
- Lander con movimiento autonomo.
- Lander disparando al jugador si esta en pantalla.
- Lander capturando astronautas.
- Alerta de rapto mediante sonido y flecha/minimapa.
- Transformacion de Lander a Mutant al completar rapto.
- Mutant como enemigo agresivo.
- Balas enemigas ocasionales.
- Misiles pequenos menos frecuentes.
- Wraparound vertical de enemigos, coordinado con Persona 1.
- Astronauta cae con gravedad si muere el Lander.
- Astronauta muere si cae desde muy alto.
- Astronauta puede ser rescatado y depositado para puntaje.
- Patron State aplicado a IA.

## Rutas bajo responsabilidad principal

```text
src/components/enemy.py
src/components/astronaut.py
src/components/indicator.py
src/components/projectile.py
src/components/velocity.py
src/components/wraparound.py
src/systems/enemy_spawn_system.py
src/systems/lander_ai_system.py
src/systems/mutant_ai_system.py
src/systems/abduction_system.py
src/systems/astronaut_system.py
src/systems/gravity_system.py
src/systems/projectile_system.py
config/enemies.json
config/waves.json
config/world.json
```

## Rutas compartidas con revision obligatoria

```text
src/factories/entity_factory.py
src/systems/collision_system.py
src/systems/hud_system.py
src/systems/audio_system.py
src/systems/particle_system.py
src/scenes/play_scene.py
config/scoring.json
config/audio.json
```

## Entregables de codigo

### 1. Astronautas

Debe implementar:

- Creacion de astronautas bajo la linea del planeta.
- Posicion inicial distribuida por el mundo.
- Movimiento leve horizontal en el suelo.
- Estado `walking`.
- Estado `captured`.
- Estado `falling`.
- Estado `carried_by_player`.
- Estado `deposited`.
- Estado `dead`.
- Uso de suelo del planeta como referencia.
- Muerte por caida alta.
- Rescate por jugador.
- Deposito en suelo con puntaje.

El astronauta no debe colisionar con la linea del planeta como si fuera pared; esa linea solo define suelo para astronautas.

### 2. Lander

Debe implementar estados:

```text
patrol -> seek_astronaut -> abducting -> ascending -> transform_to_mutant
```

Tambien debe poder atacar:

```text
patrol -> attack_player -> patrol
seek_astronaut -> attack_player -> seek_astronaut
```

Criterios minimos:

- Aparece progresivamente segun `config/waves.json`.
- Se mueve de forma autonoma.
- Busca astronautas disponibles.
- Si esta en pantalla puede disparar al jugador.
- Dispara balas ocasionales.
- Dispara misiles con menor probabilidad.
- Al capturar astronauta reproduce alerta.
- Mientras asciende, astronauta lo sigue visualmente.
- Si llega arriba, elimina astronauta y crea Mutant.
- Si muere durante rapto, suelta astronauta en caida.

### 3. Mutant

Debe implementar:

- Creacion al completar rapto.
- Movimiento mas agresivo que Lander.
- Persecucion o presion hacia jugador.
- Disparo ocasional.
- Wraparound horizontal y vertical.
- Colision con laser del jugador.
- Particulas y puntaje al morir.

### 4. Proyectiles enemigos

Debe implementar o coordinar:

- Balas enemigas ocasionales.
- Misiles pequenos menos frecuentes.
- Owner/enemy type para que colision no mate al emisor incorrecto.
- Lifetime o eliminacion por distancia.
- Sonido de disparo enemigo.

### 5. Indicador de rapto

Debe entregar al menos uno:

- Flecha en HUD apuntando hacia Lander que rapta.
- O datos suficientes para que Persona 4 renderice minimapa.

Si se implementa minimapa, el requisito obligatorio de contador/flecha queda cubierto y ademas cuenta como bono.

## Datos y configuracion

Debe trabajar principalmente en:

```text
config/enemies.json
config/waves.json
config/world.json
config/scoring.json
```

No dejar hardcodeados:

- Numero de Landers por ola.
- Numero de Mutants iniciales.
- Numero de astronautas.
- Intervalo de spawn.
- Tasa de disparo.
- Probabilidad de misil.
- Velocidad de ascenso de rapto.
- Altura maxima segura de caida.
- Puntos por rescate y deposito.

## Criterios de aceptacion propios

Una tarea de este rol esta terminada cuando:

- Hay Landers visibles y activos.
- Hay astronautas en suelo.
- Un Lander puede capturar un astronauta.
- El jugador recibe alerta del rapto.
- Si el Lander llega arriba, aparece Mutant.
- Si el Lander muere durante rapto, el astronauta cae.
- El astronauta puede morir por caida alta.
- El astronauta puede rescatarse y depositarse.
- Los enemigos disparan balas y misiles.
- Los estados pueden explicarse en el video.

## Dependencias con otros roles

- Persona 1 define mundo, wraparound, escenas y orden de sistemas.
- Persona 2 define colisiones, puntaje final y muerte del jugador.
- Persona 4 define assets, audio final, minimapa e indicadores visuales.

## Reglas de coordinacion

- No implementar IA dentro de componentes.
- Cada enemigo debe tener estado explicito y datos suficientes para depuracion.
- Si se agrega un nuevo enemigo bono, debe estar aislado para no romper Lander/Mutant.
- Las entidades creadas por spawn deben usar fabricas compartidas.
- Todo comportamiento que dependa de numeros ajustables debe ir a config.

## Checklist de rubrica asignada

- [x] Astronautas en el suelo.
- [x] Astronautas se desplazan levemente.
- [x] Landers generados progresivamente.
- [x] Landers se mueven.
- [x] Landers disparan.
- [x] Landers capturan astronautas.
- [x] Alerta de captura.
- [x] Flecha de rapto o datos para minimapa.
- [x] Lander asciende con astronauta.
- [x] Lander se transforma en Mutant.
- [x] Astronauta cae si Lander muere.
- [x] Astronauta muere por caida alta.
- [x] Astronauta rescatable y depositable.
- [x] Mutant implementado.
- [x] Balas enemigas ocasionales.
- [x] Misiles enemigos menos frecuentes.
- [x] State aplicado a IA.

## Estado actual de Persona 3

La parte asignada a Persona 3 se considera implementada y conectada al flujo principal.

Cobertura actual:

- Landers y Mutants activos con estados explicitos.
- Rapto, ascenso, mutacion y liberacion del astronauta.
- Astronautas en suelo, caida, muerte, rescate y deposito.
- Balas enemigas y misiles activos en olas.
- Flecha de rapto y contador visual resumido en HUD.
- Ajustes recientes de UX: mundo horizontal mas corto y navegacion con wraparound real.

Validacion manual recomendada antes del merge final:

- rescatar un astronauta cerca de los bordes del mundo
- verificar que el paso fin-inicio de nave y enemigos se sienta continuo
- confirmar que el HUD derecho muestra `ENEMIES` total y astronauta con icono

Riesgos residuales razonables para la entrega:

- Los comportamientos son simplificados frente al arcade original para mantener explicacion clara.
- El ajuste fino de velocidades y frecuencias puede pulirse en integracion final sin cambiar la arquitectura.

