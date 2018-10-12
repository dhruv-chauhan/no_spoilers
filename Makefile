all: init.sh run.sh
	chmod u+x init.sh
	chmod u+x run.sh 
	./init.sh

clean:
	rm -rf no_spoilers_env