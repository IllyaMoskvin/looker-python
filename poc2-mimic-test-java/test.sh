#!/usr/bin/env bash

# TODO: Would be nice to pass host and auth here
javac -cp mariadb-java-client-2.5.4.jar Test.java
java -cp .:mariadb-java-client-2.5.4.jar Test
