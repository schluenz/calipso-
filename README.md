# calipso+
Use Cases for Calipso+ Project

The repository provides recipes for building the Calipso+ use case in various packaging formats.
The singularity/docker recipes are triggering automated builds on singularity/docker hubs - where possible.

#### Available singularity container:
* invoking crystfel
  * singularity shell shub://schluenz/calipsoplus:crystfel

#### Available docker container:
* invoking crystfel
  * docker run -t -u $(id -u):$(id -g) --userns=host --security-opt no-new-privileges -i schluenz/calipsoplus:crystfel
  * bind mount volumes for example ... --mount type=bind,source=/data,target=/data
  * pulling the crystfel container: docker pull schluenz/calipsoplus:crystfel
  
