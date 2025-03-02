# Creación de usuarios
Una vez se ha desplegado el stack correctamente, debemos crear los usuarios que deseemos para las pruebas.

Se ha creado una user pool de Cognito, que se usará para autenticar y autorizar a los usuarios para las diferentes acciones dentro de la aplicación.

Dentro de esta pool hay dos grupos:

- `advertisers-group`: Los usuarios que estén en este grupo tienen permiso de crear anuncios, además de poder usar todo el resto de la funcionalidad.
- `consumers-group`: Los usuarios que estén en este grupo podrán realizar toda la funcionalidad de la aplicación excepto publicar un anuncio.

Si un usuario no está en ninguno de los dos grupos, se asumirá el de `consumers-group`.

Estos usuarios se deben crear a mano desde la interfaz de cognito en AWS, no se ha implementado manera de registrarse.
