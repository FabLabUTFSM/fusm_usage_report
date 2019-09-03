# FabLab UTFSM: Informe de uso de máquinas

Este informe interactivo está orientado a mostrar información en reuniones de
gestión y para presentación de KPI's del laboratorio. El informe también
presenta una vista de impresión ideal para hacer presentaciones en PDF o
entregar información en papel si es que esta es solicitada.

Está basada en el registro de uso de máquinas que se lleva desde Mayo de 2019.
Este registro ha pasado por varias revisiones y modificaciones por lo que los
datos desde el principio hasta el presente no son completamente consistentes.

La intención de este informe es presentar los datos de forma que la última
información disponible en el informe pueda ser representada, y tratar de
compensar las lagunas de información de revisiones anteriores a través de
transformaciones de los datos originales u omisión.

Como nota para el desarrollo, las transformaciones a los datos se deberán
realizar en el proceso de ejecución del software y no directamente en los
datos, de modo que el sistema siga compatible con la información directamente
extraída del sistema.

## Entorno de desarrollo

Crearemos un entorno virtual de Python 3.7+ con su administrador de entorno
favorito, luego instalamos los requerimientos...

    git clone git@github.com:FabLabUTFSM/fusm_usage_report.git
    python3 -m venv fusm_usage_report
    cd fusm_usage_report
    source ./bin/activate
    pip install -r requirements.txt

Para ejecutar la aplicación en el modo de desarrollo...

    python ./app.py

## Desarrollo

Esta aplicación utiliza `Dash` para la presentación de la información y
`pandas` para su análisis.

Otras herramientas que pueden resultar útiles para el desarrollo, pero que
no son un requisito son `Visual Studio Code` como editor, instalando la
extensión `Excel Viewer` para mejorar la visualización de archivos `.csv`.

