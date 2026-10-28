# Channel Manifest — Historia de Usuario

## Problema

FLIK arrancaba directamente sobre un catálogo semilla sin una unidad de entrada. Sin un modelo de canal, la pantalla de entrada tendría que inventar campos, y el estado «sin conectar» no existiría como concepto.

## Actores

- **Usuario:** no interactúa con este componente, pero lo percibe como el origen de sus canales.
- **Pantalla de Canales (`CMP-33`):** consume la lista.
- **Tarjeta de canal (`CMP-34`):** consume un canal.

## Historia

> **Como** usuario,
> **quiero** que la aplicación tenga canales desde el primer arranque,
> **para** poder entrar en uno sin configurar nada y sin conexión.

## Criterios de negocio

- `US-01`: existen exactamente cinco canales por defecto al arrancar.
- `US-02`: todos nacen sin fuente conectada y se muestran como tales.
- `US-03`: cada canal por defecto tiene un arte distinto y declarado.
- `US-04`: el orden de los canales es estable entre arranques.
- `US-05`: la lista se obtiene sin red y sin base de datos.
- `US-06`: un canal sin fuente declara cero títulos, no un valor desconocido.

## Fuera de alcance

- Crear, editar o borrar canales.
- Conectar listas locales o remotas.
- Persistir el último canal abierto.
- Portadas remotas.
