# Inventario de Productos

Aplicación web empresarial para el módulo de registro de productos en un sistema de inventario.

## Estructura del proyecto
----------------------------
/project-root
├── /frontend
│   ├── index.html
│   ├── /css
│   ├── /js
│   └── /assets
├── /backend
│   ├── server.js
│   ├── /routes
│   ├── /controllers
│   ├── /models
│   ├── /config
│   └── /middlewares
├── package.json
└── README.md
------------------------

## Instalación

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
npm install
```

## Ejecución

Inicia el servidor:

```bash
npm run dev
```

Luego abre tu navegador en:

```text
http://localhost:3000
```

## Qué incluye esta primera fase

- Formulario profesional para registrar productos.
- Validación en frontend y backend.
- Catálogo dinámico de productos en memoria.
- API RESTful con endpoints:
  - `GET /productos`
  - `POST /productos`
- Arquitectura preparada para conectar con base de datos relacional.

