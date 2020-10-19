Project aim to parse the Swedish Police RSS feed and present visually according to set search parameters by user on website.

YT: https://www.youtube.com/watch?v=Gv2Ps7Ltu9Q&list=PLmxT2pVYo5LBcv5nYKTIn-fblphtD_OJO&index=3
using: mariaDB
Homebrew: https://brew.sh/
Maria DB: https://mariadb.com/kb/en/installing-mariadb-on-macos-using-homebrew/
    https://mariadb.com/resources/blog/installing-mariadb-10-1-16-on-mac-os-x-with-homebrew/
    https://www.digitalocean.com/community/tutorials/how-to-reset-your-mysql-or-mariadb-root-password
    https://ostechnix.com/how-to-reset-mysql-or-mariadb-root-password/
    https://stackoverflow.com/questions/13585910/installing-mariadb-on-mac
    https://www.linuxquestions.org/questions/linux-software-2/mysql-mariadb-install-root-password-not-working-4175602071/
    https://gist.github.com/brandonsimpson/5204ce8a46f7a20071b5
        start: sudo port load mariadb-server
            https://stackoverflow.com/questions/17461170/how-do-i-start-mariadb-on-boot-on-mac-os-x
            https://stackoverflow.com/questions/5376427/cant-connect-to-local-mysql-server-through-socket-var-mysql-mysql-sock-38
                brew services start mariadb
                brew servies start mysql

        stop: sudo port unload mariadb-server
Flask mysqlalchemy:
    https://stackoverflow.com/questions/10572498/importerror-no-module-named-sqlalchemy
    pip3 install flask sqlalchemy flask_sqlalchemy

PyMySQL
    pip3 install pymysql

Docker
    https://hub.docker.com/_/mariadb
    https://pilsniak.com/how-to-install-docker-on-mac-os-using-brew/

Docker + Python + MariaDB
    https://hackernoon.com/getting-started-with-mariadb-using-docker-python-and-flask-pa1i3ya3
    https://hub.docker.com/_/mariadb
    https://severalnines.com/blog/how-deploy-mariadb-server-docker-container
    https://www.youtube.com/watch?v=dVEjSmKFUVI
    https://mariadb.com/kb/en/installing-and-using-mariadb-via-docker/

Regex
    https://stackoverflow.com/questions/10931044/regular-expression-dictionary-in-python

Geoparse:
    https://towardsdatascience.com/geoparsing-with-python-and-natural-language-processing-4762a7c92f08
    https://github.com/openeventdata/mordecai

    https://pypi.org/project/geoparsepy/
    https://github.com/stuartemiddleton/geoparsepy

    https://www.psycopg.org/docs/install.html
    https://pypi.org/project/libpq-dev/
    https://stackoverflow.com/questions/10132274/install-libpq-dev-on-mac-os-x

Insert MariaDB
    https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
    https://www.youtube.com/watch?v=yOmxJbZjTnU


Yield function
    https://www.guru99.com/python-yield-return-generator.html
    https://lerner.co.il/2020/05/08/making-sense-of-generators-coroutines-and-yield-from-in-python/

Classes
    https://www.youtube.com/watch?v=apACNr7DC_s
