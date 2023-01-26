#!/bin/bash

echo "Starting twitter ingestion job..."
curl -X POST --data-binary @data/tweets.json -H "Content-Type: application/json" http://localhost:8080/?network=twitter

echo "Starting vkontakte ingestion job..."
curl -X POST --data-binary @data/vk.json -H "Content-Type: application/json" http://localhost:8080/?network=vkontakte

echo "Waiting for 5 seconds..."
sleep 5

echo "Getting the data back!"
curl -X GET http://localhost:8080/?network=vkontakte&network=twitter
