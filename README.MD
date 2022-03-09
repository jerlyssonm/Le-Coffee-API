# Le-Coffee API

Le-Coffee API, uma API para um e-commerce de cafés artesanais onde serão cadastrados administradores com acesso ao CRUD completo para administração de produtos e regiões. Já usuários que estiverem logados vão poder realizar pedidos e avaliar produtos

## Funcionalidades
***ADMINISTRADOR***

Um admistrador logado no sistema tem a opção de cadastrar novos produtos com suas respectivas informações, atualizá-las e deletar os produtos, no sistema será guradado uma chave para cada adimistrador que será necessária para a autenticação das rotas para essas tarefas.

***USUARIO***

Um usuário logado poderá ver a lista de produtos oferecidos pela loja, visualiar as regiões onde são produzidos e adicioná-los a pedidos que serão registrados. além de poder atualizar suas próprias informações.

## Rotas com exemplos de sucesso na resposta 
```http
BASE_URL = https://le-coffee.herokuapp.com
```
<details><summary> <b>ADMINISTRADOR</b> </summary>

**Criar conta de administrador**
```
POST  BASE_URL /admin/register
```
***Entrada:***
```json
    {
	    "name": "example",
	    "email": "example@hotmail.com",
	    "password": "123456789"
    }
```
***Retorno: 201, CREATED***
```json
    {
	    "user_id": "430e5ca8-ecab-4e79-bbe4-5838d99ec0f1",
	    "name": "example",
	    "email": "example@hotmail.com"
    }
```

**Login de Administrador**
```
POST  BASE_URL /admin/login
```
***Entrada:***
```json
    {
	    "email": "example@hotmail.com",
	    "password": "123456789"
    }
```
***Retorno: 200, OK***
```json
    {
	    "admin_key": "0ZrD3rXuo4FoO9lG3aQ4Uw"
    }
```
</details>

***
***

<details> <summary> <b>USUARIO<b> </summary>

**Criar conta de usuario**
```
POST  BASE_URL  /users/register
```
***Entrada:***
```json
    {
	    "name": "user",
	    "email": "user@hotmail.com",
	    "password": "123456789"
    }
```
***Retorno: 201, CREATED***
```json
    {
	    "user_id": "430e5ca8-ecab-4e79-bbe4-5838d99ec0f1",
	    "name": "user",
	    "email": "user@hotmail.com"
    }
```
****
**Login de usuario**
```
POST  BASE_URL /users/login
```
***Entrada:***
```json
    {
	    "email": "example@hotmail.com",
	    "password": "123456789"
    }
```
***Retorno: 200, OK***
```json
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0Njc5OTg4MSwianRpIjoiNGUzNjQxNzEtODc2OS00ZjNjLTkyNTEtMDk3ZjM3NjI1NmFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoiNDMwZTVjYTgtZWNhYi00ZTc5LWJiZTQtNTgzOGQ5OWVjMGYxIiwibmFtZSI6Implcmx5c3NvbiIsImVtYWlsIjoiamVybHlzc29uQGhvdG1haWwuY29tIn0sIm5iZiI6MTY0Njc5OTg4MSwiZXhwIjoxNjQ2ODAwNzgxfQ.B0OML2tpaE3bLs5z7-RrOIhBGBjfG4mu9y38Ol0N7dc"
	}
```
</details>

***
***
## ROTAS COM AUTENTICAÇÃO

<details><summary>Administrador<b></summary>

**autenticação para admin** 
```
"Bearer": admin_key
```
***
**Buscar todos usuarios**
```
GET BASE_URL /users
```
***Entrada***
```json
{

}
```
***Retorno: 200, OK***
```json
[ ] ou uma lista com todos os usuarios
```

</details>


***
***
<details><summary>Usuario</summary>

**autenticação para usuario** 
```
"Bearer": token
```
***
**Atualizar informações da conta**
```
PUT  BASE_URL  /users
```
***Entrada***
voce pode mandar um valor ou todos para atualizar
```json
{
	"password": "example1"
}
ou
{
	"name": "example2",
	"email": "example2@hotmail.com",
	"password": "123456789"
}
```
***Retorno: 204, NO CONTENT***
```
sem retorno
```
***
**Deletar conta**
```
DELETE  BASE_URL  /users
```

***Entrada:***
```

```
***retorno: 204, NO CONTENT***

```

```

</details>

