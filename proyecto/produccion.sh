#!/bin/bash


# Menú inicial
echo "Seleccione una opción:"
echo "1) Producción"
echo "2) Desarrollo"

# Leer la opción del usuario
read opcion

echo "opcion: $opcion"
if [ "$opcion" == "1" ]; then
  # Menú para Producción
  echo "Seleccione una versión para Producción:"
  echo "1) v15.0"
  echo "2) v16.0"
  echo "3) v17.0"
  
  # Leer la versión seleccionada
  read version

  echo "version: $version"

  case $version in
    1)
      echo "Has seleccionado la versión v15.0"
      version="v15.0"
      ;;
    2)
      echo "Has seleccionado la versión v16.0"
      version="v16.0"
      ;;
    3)
      echo "Has seleccionado la versión v17.0"
      version="v17.0"
      ;;
    *)
      echo "Opción no válida. Saliendo..."
      exit 1
      ;;
  esac
elif [ "$opcion" == "2" ]; then
  echo "Has seleccionado Desarrollo"
else
  echo "Opción no válida. Saliendo..."
  exit 1
fi


# Menú de selección de backup
echo "Seleccione el backup de la base de datos:"
echo "1) backup1.backup"
echo "2) backup3.backup"

# Leer la opción de backup
read backup

img=""

case $backup in
  1)
    echo "Has seleccionado el backup1.backup"
    backup="backup1.backup"
    img="backup1.zip"
    ;;
  2)
    echo "Has seleccionado el backup2.backup"
    backup="backup3.backup"
    img="backup3.zip"
    ;;
  *)
    echo "Opción no válida. Saliendo..."
    exit 1
    ;;
esac


# opcion   => 1: produccion
#             2: desarrollo

# version  => v6.0, v7.0, v8.0, v9.0

# img      => backup1.zip, backup2.zip, backup3.zip

# backup   => backup1.backup, backup2.backup, backup3.backup



# Paso 1: Asignar parámetros a variables
REPO_LINK="https://github.com/Paul-Navarro/proyecto-IIN.git"
TAG_NAME="$version"

echo "TAG_NAME: $TAG_NAME"


# Paso 2: Clonar el repositorio en el directorio actual
echo "Clonando el repositorio desde $REPO_LINK..."
git clone $REPO_LINK


echo "opcion=$opcion"
if [ "$opcion" == "1" ]; then

  echo "SCRIPT DE PRODUCCION"

  # Extraer el nombre del repositorio del URL para cambiar al directorio correcto
  REPO_NAME=$(basename $REPO_LINK .git)

  # Cambiar al directorio del repositorio clonado
  cd proyecto-IIN/proyecto/ || { echo "Error: No se pudo acceder a la carpeta proyecto-IIN/proyecto"; exit 1; }

  # Verificar si el tag existe en el repositorio
  echo "Verificando si el tag $TAG_NAME existe..."
  if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo "El tag $TAG_NAME ya existe. Continuando con la restauración..."
  else
    echo "El tag $TAG_NAME no existe en el repositorio."
    exit 1
  fi

  # Extraer las imágenes desde el archivo .zip para restaurar las imagenes posteriormente
  echo "Extrayendo imágenes desde el archivo backup1.zip..."  
  unzip -qo "$img" -d ./imagenes_contenido
  # Hacer checkout al tag especificado
  echo "Cambiando al tag $TAG_NAME..."
  git checkout $TAG_NAME
  # Borrar todos los contenedores activos
  echo "Deteniendo y eliminando contenedores..."
  docker-compose down -v
  # Construir los contenedores de nuevo
  echo "Construyendo contenedores..."
  docker-compose up --build -d
  # Esperar 30 segundos para asegurar que los contenedores se inicien correctamente
  echo "Esperando 30 segundos para que los contenedores se inicien..."
  
  sleep 30

  # Realizar el backup de la base de datos
  
  docker exec proyecto_web_1 sh -c "rm -rf /app/media/imagenes_contenido > /dev/null 2>&1"
  # Copiar el archivo de backup al contenedor de PostgreSQL


  BACKUP_FILE="./$backup"
  docker cp $BACKUP_FILE proyecto_db_1:/tmp/$backup
  

  # Paso 10: Entrar al contenedor db y restaurar el backup
  echo "Entrando al contenedor de base de datos para restaurar el backup..."
  
  docker exec -it proyecto_db_1 sh -c "
    # Vaciar la base de datos 'leticia' eliminando todas las tablas dentro del esquema public
    echo 'Vaciando la base de datos leticia...'
    psql -U postgres -d leticia -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;' && \
    
    # Restaurar el backup en la base de datos 'leticia'
    
    pg_restore -U postgres -d leticia /tmp/$backup && \

    echo 'Backup restaurado exitosamente.' && \

    rm /tmp/$backup && \
    
    # Salir del contenedor
    exit
  "
  docker cp ./imagenes_contenido/. proyecto_web_1:/app/media/ > /dev/null 2>&1

  echo "Backup restaurado exitosamente."

  

  
  



  docker exec pictshare sh -c "rm -rf /var/www/html/upload/imagenes_contenido > /dev/null 2>&1"
  docker cp ./imagenes_contenido/. pictshare:/var/www/html/upload/


  echo "Las imágenes han sido copiadas correctamente."

elif [ "$opcion" == "2" ]; then
  # Añadir el repositorio de PostgreSQL
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -c | awk "{print $2}")-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  sudo apt update

  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update


  echo "Has seleccionado Desarrollo"
  
  # Instalación de Python 3.12
  echo "Instalando Python 3.12..."
  sudo apt update -y
  #sudo apt install -y python3.12 python3.12-dev python3.12-venv python3.12-distutils
  sudo apt install -y python3.12 python3.12-dev python3.12-venv

  # Eliminar todas las versiones de PostgreSQL instaladas
  #echo "Desinstalando PostgreSQL existente..."
  #sudo apt purge -y postgresql* 
  #sudo apt autoremove -y

  # Instalar PostgreSQL 16.2
  echo "Instalando PostgreSQL 16.2..."
  sudo apt update
  sudo apt install -y postgresql-16 postgresql-client-16 postgresql-contrib-16

  

  # Crear usuario 'postgres' y asignar privilegios #IF NOT EXISTS
  echo "Creando usuario 'postgres' y asignando privilegios..." 
  sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
  sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"



  # Eliminar la base de datos si existe y vaciarla antes de crearla
  echo "Eliminando base de datos 'leticia' si existe..."
  sudo -u postgres psql -c "DROP DATABASE IF EXISTS leticia;"
  
  #psql -U postgres -d leticia -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;' && \
  
  # Crear una nueva base de datos 'leticia'
  echo "Creando la nueva base de datos 'leticia'..."
  sudo -u postgres psql -c "CREATE DATABASE leticia;"



  #sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE leticia TO postgres;"
  
  
  
  # Navegar a la carpeta 'proyecto-IIN/proyecto'
  echo "Accediendo al directorio de trabajo..."
  cd ./proyecto-IIN/proyecto
  
  # Cambiar a la rama 'master' en Git
  echo "Cambiando a la rama master..."
  git checkout master
  
  # Crear un entorno virtual
  echo "Creando entorno virtual..."
  python3.12 -m venv venv
  
  # Activar el entorno virtual
  echo "Activando el entorno virtual..."
  source venv/bin/activate
  
  # Instalar dependencias desde requirements.txt
  echo "Instalando dependencias de Python..."
  pip install --upgrade pip
  pip install -r requirements.txt


  # Restaurar el backup en la base de datos 'leticia'
    

  unzip -o "$img" -d ./imagenes_contenido
  rm -rf ./media/imagenes_contenido
  cp -r ./imagenes_contenido ./media/
  rm -r ./imagenes_contenido
  
  echo "Realizando backup de la base de datos..."
  
  sudo -u postgres pg_restore -d leticia ./$backup


  echo 'Backup restaurado exitosamente.' 



  python manage.py runserver

fi
echo "Todo el proceso se ha completado correctamente."


# Fin del script
