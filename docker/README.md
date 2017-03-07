# Commands

* build
  * docker build -t [imageTag] -f [Dockerfile] [Path]
  * docker build -t ijahpredictor -f predictorDockerfile .

* check log
  * docker logs -f -t [imageName]
  * docker logs -f -t ijah_predictor_0_daemon
  * docker logs -f -t ijah_loadbalancer_daemon

* run
  * docker run -d --name "ijah_predictor_0_daemon" -p 5010-5012:5010-5012 -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi

* run the dir xplorerdocker
  * exec -it [imageName] bash

* task manager
  * docker ps -a

* see port status
  * netstat -ntlp
