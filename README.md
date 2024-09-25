# serverAndClientWithSocket

Este proyecto implementa un sistema de comunicación entre un servidor y múltiples clientes utilizando sockets en Python. Los clientes pueden enviar comandos al servidor para realizar diversas operaciones, como listar archivos en el servidor o descargar un archivo específico.

## Características

- **Comando `lsFiles`**: Permite listar los archivos en la carpeta `Files` del servidor.
- **Comando `get <archivo>`**: Permite a un cliente descargar un archivo desde el servidor y guardarlo localmente en una carpeta llamada `download`.
- **Soporte para múltiples clientes**: Varios clientes pueden conectarse al servidor de manera simultánea.
- **Comunicaciones seguras**: Las comunicaciones entre cliente y servidor utilizan serialización con `pickle` para enviar y recibir datos.
