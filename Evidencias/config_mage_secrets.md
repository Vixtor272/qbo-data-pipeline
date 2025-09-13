Para la configuración de mage_secrets se utilizaron 4 secretos que nos permitirán mantener la seguridad de nuestro pipeline: 

<img width="539" height="476" alt="image" src="https://github.com/user-attachments/assets/d68d3e97-12b0-489f-adf8-07a2f7726a9b" />

Utilizamos el realm_id para acceder a la API, client_id y secrets_id para obtener acceso a QB y finalmente el refresh_token para generar un nuevo access_token cada que lo necesitemos puesto que este dura 101 días, a diferencia del access_token que dura tan solo 60 minutos.

