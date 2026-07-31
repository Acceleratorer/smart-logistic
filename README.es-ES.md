

#  Smart Logistics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Open In Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/code/trnchtng/notebook6d375cdcf5)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-FD971F?style=for-the-badge&logo=gradio&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Maps-77B829?style=for-the-badge&logo=leaflet&logoColor=white)
![OSRM](https://img.shields.io/badge/OSRM-Routing-blue?style=for-the-badge&logo=openstreetmap&logoColor=white)

##  Arquitectura del Sistema y Análisis del Flujo de Trabajo

### 1. Proceso Empresarial (Análisis del Diagrama de Flujo)
El sistema sigue un exhaustivo **Diagrama de Flujos Transversal (Cross-functional Swimlane Diagram)**, delineando claramente las responsabilidades entre cuatro partes interesadas clave: **Transportista (Proveedor Logístico)**, **Tienda (Comerciante)**, **Plataforma de Comercio Electrónico** y **Cliente**.

> **Nota:** Consulte la imagen del diagrama de flujo del sistema en la carpeta `docs/` para una representación visual.

** Fortalezas Clave**
* **Separación Clara de Responsabilidades:** Cuadrantes distintos para *Flujo de Información* (actualizaciones de API, sincronización de estado) frente a *Flujo Físico* (envío, almacenamiento).
* **Manejo de Excepciones:** El flujo de trabajo contempla tanto los "Flujos Exitosos" (entregas completadas) como escenarios complejos de **Logística Inversa** (fracaso en la entrega $\rightarrow$ almacenamiento $\rightarrow$ devolución a la tienda).
* **Conciliación Financiera:** La lógica distingue entre pedidos **Prepagados** y **COD** (Pago contra entrega), un requisito crítico para el mercado vietnamita.

** Áreas de Mejora**
* [ ] **Lógica de Reintento:** Las futuras iteraciones incluirán un bucle específico para "Intentos de reentrega" (típicamente 3 intentos) antes de iniciar el proceso de devolución.
* [ ] **Cancelación Anticipada:** Manejo de casos límite como "Cancelación por el Usuario" o eventos de "Sin Stock" previos a la fase de envío.

---

### 2. Implementación Técnica (POC)
El código actual funciona como una **Prueba de Concepto (POC)** centrada en el módulo de **Planificación de Transporte** dentro del cuadrante "Transportista". Puede ejecutar la demostración en vivo directamente en Kaggle:

[**Haga clic aquí para ejecutar el Notebook**](https://www.kaggle.com/code/trnchtng/notebook6d375cdcf5)

####  Pila Tecnológica
| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Lenguaje** | `Python` | Lógica central y procesamiento de backend. |
| **Interfaz** | `Gradio` | Desarrollo rápido de UI con Bloques responsivos. |
| **Mapeo** | `Folium` | Renderizado de mapas interactivos. |
| **Enrutamiento** | `OSRM` | Open Source Routing Machine para distancias reales. |
| **Datos** | `Pandas` | Manipulación de datos y manejo tabular. |

####  Funcionalidades Principales y Aspectos Técnicos Destacados
* **UI/UX Avanzada (Mapa Bidireccional):** Utiliza un puente JavaScript personalizado `postMessage` para capturar coordenadas desde el iframe de `Folium` e inyectarlas de nuevo en el backend de Python. Esto resuelve un gran punto de dolor en la UX relacionado con la entrada precisa de direcciones.
* **Enrutamiento en el Mundo Real:** Integra **OSRM** para calcular distancias basadas en redes viales reales (distancia conduccible), con una alternativa defensiva a la distancia de Haversine para garantizar fiabilidad.
* **Motor de Costos Dinámico:** La función `rule_cost` modela con precisión los precios logísticos, teniendo en cuenta:
    * Métricas de volumen ($L \times W \times H$)
    * Tipos de carga (Frágil, Cadena de frío, Alto valor)

####  Limitaciones Actuales y Hoja de Ruta
* **Geocodificación:** Actualmente depende de `Nominatim` (OpenStreetMap), que tiene límites de tasa estrictos.
    * *Hoja de Ruta:* El despliegue en producción requerirá una API de pago robusta (p. ej., Google Maps API) o almacenamiento en caché local.
* **Algoritmo de Optimización:** Utiliza un enfoque de **Vecino Más Cercano (Greedy)**.
    * *Hoja de Ruta:* Las futuras versiones migrarán a **Google OR-Tools** para manejar restricciones complejas de **VRP (Problema de Enrutamiento de Vehículos)** como la capacidad del vehículo y las ventanas de tiempo.
