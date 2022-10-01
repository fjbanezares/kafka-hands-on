# kafka-hands-on
Apache Kafka basic practices

## Set up Kafka

```
In the Cloud Console, open the Navigation menu and click Marketplace.
Launch Apache Kafka Server on Ubuntu Server 20.04
```

While the cluster is being generated try to understand what we do in this code,
* we instantiate a KStream object with lines of text
* We generate a KTable object by transforming the KStream into individual lowercase words stream and counting the appearences of every word with a groupBy
* We do this because there is no "grouping a Stream"
* Finally we take the table and Stream it in a Kafka sink topic

```java
// Serializers/deserializers (serde) for String and Long types
final Serde<String> stringSerde = Serdes.String();
final Serde<Long> longSerde = Serdes.Long();
// Construct a `KStream` from the input topic "streams-plaintext-input", where message values
// represent lines of text (for the sake of this example, we ignore whatever may be stored
// in the message keys).
KStream<String, String> textLines = builder.stream("streams-plaintext-input", Consumed.with(stringSerde, stringSerde));
KTable<String, Long> wordCounts = textLines
    // Split each text line, by whitespace, into words.  The text lines are the message
    // values, i.e. we can ignore whatever data is in the message keys and thus invoke
    // `flatMapValues` instead of the more generic `flatMap`.
    .flatMapValues(value -> Arrays.asList(value.toLowerCase().split("\\W+")))
    // We use `groupBy` to ensure the words are available as message keys
    .groupBy((key, value) -> value)
    // Count the occurrences of each word (message key).
    .count();
// Convert the `KTable<String, Long>` into a `KStream<String, Long>` and write to the output topic.
wordCounts.toStream().to("streams-wordcount-output", Produced.with(stringSerde, longSerde));
```

## Start the Kafka environment

```
ssh to the VM that composes the Kafka cluster
```

```shell
cd /opt/kafka/
sudo bin/zookeeper-server-start.sh config/zookeeper.properties

```

## Start the Kafka broker service

```
ssh to the VM that composes the Kafka cluster in other window
```

```shell
cd /opt/kafka/
sudo bin/kafka-server-start.sh config/server.properties
```

## Prepare the topics and the input data

```
ssh to the VM that composes the Kafka cluster in other window
```

```shell
cd /opt/kafka/

# create the input topic
sudo bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-plaintext-input
 
# create the output topic   
sudo bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic streams-wordcount-output
    
echo -e "all streams lead to kafka\nhello kafka streams\njoin kafka summit" > /tmp/file-input.txt

```


``` 
all streams lead to kafka

hello kafka streams

join kafka summit
```

```shell
cat /tmp/file-input.txt | sudo bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic streams-plaintext-input
```

## Process the input data with Kafka streams

Kafka's WordCount demo application is bundled with Confluent Platform, which means you can run it without further ado, i.e. you do not need to compile any Java sources and so on:

Execute the following command to run the WordCount demo application. You can safely ignore any warn log messages:
```shell
sudo bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo
```
``` 
Unlike other WordCount examples you might have seen before that operate on finite, bounded data, 
the WordCount demo application behaves slightly differently because it is designed to operate on an infinite, 
unbounded stream of input data
```
``` 
The WordCount demo application will read from the input topic streams-plaintext-input, 
perform the computations of the WordCount algorithm on the input data, 
and continuously write its current results to the output topic streams-wordcount-output
 (the names of its input and output topics are hardcoded). 
 
You can terminate the demo at any point by entering Ctrl-C from the keyboard.
```

## Inspect the output data

```shell
cd /opt/kafka
sudo bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic streams-wordcount-output \
    --from-beginning \
    --formatter kafka.tools.DefaultMessageFormatter \
    --property print.key=true \
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer \
    --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
```

Read the following about Streams and Tables in Confluent page:
```
https://docs.confluent.io/platform/current/streams/concepts.html#duality-of-streams-and-tables
https://docs.confluent.io/platform/current/streams/developer-guide/dsl-api.html#streams-dsl
```