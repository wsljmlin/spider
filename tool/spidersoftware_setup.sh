#!/bin/sh

errortxt=setuperror.txt

##
## install
##
install() {
	sudo apt-get install python
	if [ $? -eq 100 ]
	then
		echo "install python error!" >> $errortxt
	fi

	sudo apt-get install python-pip
	if [ $? -eq 100 ]
        then
                echo "install python-pip error!" >> $errortxt
        fi

	sudo pip install flask || sudo apt-get install python-flask
	if [ $? -eq 100 ]
        then
                echo "install flask error!" >> $errortxt
        fi

	sudo pip install flask_wtf
	if [ $? -eq 100 ]
        then
                echo "install flask wtf error!" >> $errortxt
        fi

	sudo pip install flask_bootstrap
        if [ $? -eq 100 ]
        then
                echo "install flask bootstrap error!" >> $errortxt
        fi

	sudo pip install pymongo || sudo apt-get install python-pymongo 
	if [ $? -eq 100 ]
        then
                echo "install mongodb error!" >> $errortxt
        fi

	sudo pip install  bs4  || sudo apt-get install python-bs4
	if [ $? -eq 100 ]
        then
                echo "install bs4 error!" >> $errortxt
        fi

	sudo pip install flask-sqlalchemy || sudo apt-get install python-flask-sqlalchemy
	if [ $? -eq 100 ]
        then
                echo "install flask sqlchemy error!" >> $errortxt
        fi

	sudo apt-get install python-mysqldb
	if [ $? -eq 100 ]
        then
                echo "install mysqldb error!" >> $errortxt
        fi
}


##
##main
##
echo "will setup spider software, please wait.....!"
rm -rf $errortxt
install
if [ -f $errortxt ]
then
	echo "some software setup error, please see $errortxt"
else
	echo "setup spider software OK"
fi
