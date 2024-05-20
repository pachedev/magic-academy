# Magic Academy

## Caso Práctico

En el Reino del Trébol, el Rey Mago necesita un sistema para la academia de magia que administre el registro de solicitud de estudiantes y la asignación aleatoria de sus Grimorios.
Los Grimorios se clasifican según el tipo de trébol en la portada, y los estudiantes según sus afinidades mágicas específicas.

## Endpoints Requeridos

- **POST /solicitud:** Envía solicitud de ingreso.
- **PUT /solicitud/{id}:** Actualiza solicitud de ingreso.
- **PATCH /solicitud/{id}/estatus:** Actualiza estatus de solicitud.
- **GET /solicitudes:** Consulta todas las solicitudes.
- **GET /asignaciones:** Consulta asignaciones de Grimorios.
- **DELETE /solicitud/{id}:** Elimina solicitud de ingreso.

## Datos Requeridos en la Solicitud

- **Nombre:** solo letras, máximo 20 caracteres.
- **Apellido:** solo letras, máximo 20 caracteres.
- **Identificación:** números y letras, máximo 10 caracteres.
- **Edad:** solo números, 2 dígitos.
- **Afinidad Mágica:** Una única opción entre Oscuridad, Luz, Fuego, Agua, Viento o Tierra.

## Notas Importantes

Las solicitudes que no cumplan con los criterios establecidos deben ser automáticamente rechazadas y no se les debe asignar un Grimorio. La asignación de Grimorios debe ser aleatoria cuando se apruebe la solicitud.

Opcionalmente sumas puntos si consideras un sistema de asignación con una ponderación que hable de la rareza de la portada asignada, por ejemplo, un trébol de una o dos hojas es común, uno de tres es poco habitual, uno de cuatro es inusual, y uno de cinco hojas muy raro.

## Arquitectura del proyecto

Utiliza una base de datos relacional [PostgreSQL](https://www.postgresql.org) para el almacenamiento de los datos de las solicitudes, asignaciones y el catálogo de Grimorios disponibles. PostgreSQL es una opción robusta y confiable para gestionar datos relacionales.

Para el desarrollo del backend, se utilizará el framework [Flask](https://flask.palletsprojects.com/en/3.0.x) en conjunto con [SQLAlchemy](https://www.sqlalchemy.org), conocido por su simplicidad y flexibilidad en la construcción de aplicaciones web en Python. Flask permite crear APIs RESTful de manera rápida y eficiente, mientras que SQLAlchemy proporciona una capa de abstracción para interactuar con la base de datos PostgreSQL de forma intuitiva.

El frontend se desarrolló utilizando [Next.js](https://nextjs.org), un framework de React que facilita la creación de aplicaciones web modernas y rápidas. Next.js ofrece características como renderizado del lado del servidor (SSR) y generación de sitios estáticos (SSG), lo que mejora el rendimiento y la experiencia del usuario.

Para facilitar el despliegue y la gestión del entorno de desarrollo, se utilizó Docker y Docker Compose. Docker permite encapsular la aplicación y sus dependencias en contenedores, garantizando la portabilidad y consistencia del entorno de ejecución. Docker Compose, por otro lado, simplifica la orquestación de múltiples contenedores y permite definir y configurar fácilmente la infraestructura necesaria para el desarrollo y despliegue de la aplicación.

A continuación, se muestra un ejemplo visual de cómo se estructuran y comunican los componentes mencionados:

<img src="./images/docs/application_architecture.jpg" alt="Arquitectura de la aplicación" width="100%"/>

Esta arquitectura proporciona una base sólida para el desarrollo de la aplicación, asegurando un almacenamiento confiable de los datos, una comunicación eficiente entre el backend y el frontend, y una gestión sencilla del entorno de desarrollo.

## Arquitectura de la base de datos

La arquitectura de la base de datos consta de tres tablas principales para almacenar la información relacionada con las solicitudes de los estudiantes, las asignaciones de los Grimorios y el catálogo de Grimorios disponibles. Estas tablas son:

1. **student_application:** Esta tabla almacenará la información de las solicitudes de los estudiantes. Aquí se guardarán los datos relevantes como el nombre del estudiante, la fecha de la solicitud, el estado de la solicitud, entre otros.

2. **grimorio_assignment:** En esta tabla se guardará la información de las asignaciones de los Grimorios. Aquí se registrarán los detalles de cada asignación, como el ID de la solicitud, el ID del Grimorio asignado, la fecha de creación, etc.

3. **grimorio:** Esta tabla almacenará la información del catálogo de Grimorios disponibles para las asignaciones. Aquí se guardarán los datos de cada Grimorio, como su nombre, rareza, peso, etc.

A continuación, se muestra un diagrama entidad-relación que representa la relación entre estas tablas:

<img src="./images/docs/ERD.jpg" alt="Arquitectura de la base de datos" width="100%"/>

Este diagrama visualiza la estructura y las relaciones entre las tablas, lo que facilita la comprensión de cómo se almacena y se relaciona la información en la base de datos.

## ¿Comó ejecutar el proyecto?

### Requerimientos iniciales

1. Tener instalado y configurado Docker y Docker Compose

2. Clonar el repositorio

```bash
git clone https://github.com/pachedev/magic-academy
```

3. Acceder al repositorio

Dirigete a la carpeta magic-academy que se genero al clonar el repositorio

```bash
cd magic-academy
```

4. Ejecuta el siguientes comando como se muestra a continuación

```bash
docker compose up -d
```

### Interfaz grafica del backend

Ingresa a la URL que se muestra a continuación

```bash
http://localhost:3500
```

#### Página inicial

Podrás encontrar una página inicial donde se muestran los **Grimorios** disponibles para las asignaciones de manera aleatoria considerando la siguiente ponderación, se han asignado los pesos [10, 8, 6, 4, 1] a las opciones "one_leaf", "two_leaf", "three_leaf", "four_leaf" y "five_leaf", respectivamente stos pesos indican la probabilidad relativa de seleccionar cada opción cuanto mayor sea el peso, mayor será la probabilidad de que se seleccione esa opción.

<img src="./images/docs/backend_home.png" alt="Página inicial" width="100%"/>

#### Página de solicitudes

En esta página encontrarás el listado de las solicitudes recibidas en el sistema.

<img src="./images/docs/backend_solicitudes.png" alt="Página para ver las asignaciones" width="100%"/>

#### Página de asignaciones

En esta página encontrarás el listado de las asignaciones realizadas en el sistema.

<img src="./images/docs/backend_asignaciones.png" alt="Página para ver las asignaciones" width="100%"/>

### Interfaz grafica del frontend

Ingresa a la URL que se muestra a continuación, aquí encontrarás una intefaz para agregar, actualizar y eliminar solicitudes.

```bash
http://localhost:3000
```

<img src="./images/docs/frontend_page_part_1.png" alt="Página gestionar el CRUD" width="100%"/>
<img src="./images/docs/frontend_page_part_2.png" alt="Página gestionar el CRUD" width="100%"/>


## ¿Comó consumir el API?

A continuación se muestra una documentación secilla para consumir el API, está la puedes encontrar en la siguiente url con la definición del [swagger](https://app.swaggerhub.com/apis/gpachecob/magic-academy/1.0.0).

#### Crea una nueva solicitud de ingreso

<details>
 <summary><code>POST</code> <code><b>/solicitud</b></code> <code>( Crea un solicitud de ingreso )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | name      |  required | string   | Nombre del aplicante  |
> | last_name      |  required | string   | Apellido del aplicante  |
> | identification      |  required | string   | Identificador del aplicante  |
> | age      |  required | number   | Edad del aplicante  |
> | magic_affinity      |  required | string   | Afinidad mágica del aplicante (darkness,light,fire,water,wind o earth)  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Se registro la solicitud correctamente.","application":{"id":1,"name":"Harry","last_name":"Potter","age":17,"magic_affinity":{"code":"fire","value":"Fuego"}}}`                                |
> | `400`         | `application/json`                | `{"message":"Lorem ipsum."}`                            |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/solicitud
> ```

</details>

#### Actualizar una solicitud de ingreso existente

<details>
 <summary><code>PUT</code> <code><b>/solicitud/{id}</b></code> <code>( Actualiza solicitud de ingreso )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | name      |  required | string   | Nombre del aplicante  |
> | last_name      |  required | string   | Apellido del aplicante  |
> | identification      |  required | string   | Identificador del aplicante  |
> | age      |  required | number   | Edad del aplicante  |
> | magic_affinity      |  required | string   | Afinidad mágica del aplicante (darkness,light,fire,water,wind o earth)  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Se actualizo la solicitud correctamente.","application":{"id":1,"name":"Harry","last_name":"Potter","age":17,"magic_affinity":{"code":"fire","value":"Fuego"}}}`                                |
> | `400`         | `application/json`                | `{"message":"Lorem ipsum."}`                            |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/solicitud/1
> ```

</details>

#### Actualizar status de solicitud de ingreso existente

<details>
 <summary><code>PATCH</code> <code><b>/solicitud/{id}/estatus</b></code> <code>( Actualiza estatus de solicitud )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | status      |  required | string   | Estado de la solicitud (rejected,assigned)  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Se actualizo la solicitud correctamente.","application":{"id":1,"name":"Harry","last_name":"Potter","age":17,"magic_affinity":{"code":"fire","value":"Fuego"}}}`                                |
> | `400`         | `application/json`                | `{"message":"Lorem ipsum."}
> | `404`         | `application/json`                | `{"message":"La solicitud de ingreso no existe."}`                            |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/solicitud/1/status
> ```

</details>

#### Obtener todas las solicitudes de ingreso existentes

<details>
 <summary><code>GET</code> <code><b>/solicitudes</b></code> <code>( Consulta todas las solicitudes )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | None      |  required | object (JSON or YAML)   | N/A  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Solicitudes obtenidas exitosamente.","applications":[{"id":1,"name":"Harry","last_name":"Potter","age":17,"magic_affinity":{"code":"fire","value":"Fuego"}}}]`                                |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/solicitudes
> ```

</details>

#### Obtener todas las asignacioes existentes

<details>
 <summary><code>GET</code> <code><b>/asignaciones</b></code> <code>( Consulta las asignaciones de Grimorios )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | None      |  required | object (JSON or YAML)   | N/A  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Solicitudes de ingreso obtenidas exitosamente.","assignments":[]}`                                |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/asignaciones
> ```

</details>

#### Eliminar asignacioes existentes

<details>
 <summary><code>DELETE</code> <code><b>/solicitud/{id}:</b></code> <code>( Elimina una solicitud de ingreso )</code></summary>

##### Parámeteros

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | None      |  required | object (JSON or YAML)   | N/A  |

##### Posibles respuestas

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{"message":"Se ha eliminado la solicitud de ingreso."}`                                |
> | `400`         | `application/json`                | `{"message":"La solicitud no fue borrada por que ya cuenta con un Grimorio asignado."}`                            |
> | `404`         | `application/json`                | `{"message":"La solicitud de ingreso no existe."}`                            |
> | `500`         | `application/json`         | `{"message":"Lorem ipsum", "error":"Lorem ipsum error."}`                            |

##### Ejemplo cURL

> ```javascript
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:3500/solicitud/{id}
> ```

</details>

## Pruebas unitarias

Para corre las pruebas unitarias y validar el correcto funcionamiento (Opcional)
Debemos obtener el listado de los contenedores que se estan ejecutando para obtener el **CONTAINER ID** para ejecutar las pruebas unitarias

```bash
docker ps
docker exec -it -u 0 CONTAINER ID ./test.sh
```

A continuación se muestra una imagen del resultado final de la ejecución de las pruebas unitarias.

<img src="./images/docs/output_docker_ps.png" alt="docker ps" width="100%"/>
<img src="./images/docs/output_unit_test.png" alt="run tests" width="100%"/>

## Autor

[@pachedev](https://www.github.com/pachedev)

## Licencia

[MIT](https://choosealicense.com/licenses/mit)
