### Authors:
* Massiel Paz Otaño
* Marlon Díaz Pérez
* Álvaro Suárez Valdés

# Recommender System

## Descripción

Este proyecto es un sistema de recomendación que combina técnicas de filtrado colaborativo y basado en contenido para proporcionar recomendaciones personalizadas de productos. El sistema emplea filtrado colaborativo para evaluar la similitud entre usuarios basada en sus interacciones con los productos, y filtrado basado en contenido para mejorar la precisión de las recomendaciones al considerar las características similares entre productos.

## Estructura del Proyecto

El proyecto está organizado en varios módulos clave:

- **Filters**: Implementa diferentes estrategias de recomendación mediante filtros. Cada filtro aplica criterios específicos para generar recomendaciones.
- **Data Access**: Maneja la comunicación con la base de datos, incluyendo la recuperación y gestión de datos de productos y usuarios.
- **Models**: Define los modelos de datos utilizados en el sistema, incluyendo contextos de recomendación y resultados de filtros.
- **Services**: Proporciona servicios adicionales como la funcionalidad de registro de actividades.
- **Presentation**: Incluye archivos Jupyter para interactuar de manera intuitiva con el sistema y visualizar resultados.

## Componentes Clave

### Filters

Los filtros aplican criterios diversos para generar recomendaciones personalizadas. Implementan la interfaz `FilterBase` y tienen el método `apply_filter` que acepta un `Context` y devuelve un `FilterResultModel`. Los filtros disponibles son:

- **CollaborativeFilter**: Genera recomendaciones basadas en la similitud de interacciones entre usuarios.
- **ContentBasedFilter**: Ofrece recomendaciones basadas en la similitud entre productos interactuados anteriormente por el usuario.

### Data Access

Maneja la comunicación con la base de datos a través de repositorios:

- **ProductRepository**: Gestiona los datos de los productos.
- **CustomerRepository**: Gestiona los datos de los clientes.
- **InteractionRepository**: Gestiona las interacciones entre usuarios y productos.

### Models

Define los modelos utilizados en el sistema:

- **Context**: Contiene la información necesaria para aplicar filtros, como el ID del usuario, los productos relevantes y el límite de recomendaciones.
- **FilterResultModel**: Representa el resultado de aplicar un filtro, incluyendo una lista de recomendaciones.
- **RecommendationModel**: Representa una recomendación individual con el ID del producto y el score de similitud.

### Services

- **Logger**: Proporciona funcionalidades para registrar y rastrear actividades del sistema, facilitando el seguimiento y la depuración.

### Main

- **FilterPipe**: Coordina la aplicación de filtros en secuencia, combina los resultados y calcula scores combinados para cada producto. Devuelve los resultados finales ordenados por score.

## Uso

### Configuración

1. **Instalación**: Clona el repositorio y asegúrate de tener todas las dependencias instaladas. Utiliza `pip` para instalar las dependencias requeridas.

   ```bash
   pip install -r requirements.txt
   ```

2. **Infrastructura**: Levanta la base de datos del proyecto utilizando Docker. Ejecuta el siguiente comando para iniciar los servicios definidos en el archivo `docker-compose.yml`:

   ```bash
   docker-compose up
   ```

3. **Ejecución**: Una vez que la infraestructura esté en funcionamiento, puedes iniciar la aplicación y comenzar a aplicar filtros y generar recomendaciones utilizando las interfaces proporcionadas.

### Ejemplos de Uso

- **Aplicar Filtros**: Utiliza el `FilterPipe` para aplicar una serie de filtros en secuencia y obtener recomendaciones personalizadas.
- **Visualizar Resultados**: Usa los archivos Jupyter incluidos en la carpeta `Presentation` para interactuar con el sistema y visualizar los resultados de las recomendaciones.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Por favor, sigue las siguientes pautas para contribuir:

1. **Fork del Repositorio**: Realiza un fork del repositorio para trabajar en tus cambios.
2. **Crea una Rama**: Crea una rama para tus cambios y realiza commits de forma clara y descriptiva.
3. **Envía un Pull Request**: Envía un pull request para que tus cambios sean revisados y fusionados con la rama principal.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE). Consulta el archivo `LICENSE` para obtener más información.