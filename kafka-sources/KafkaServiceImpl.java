package com.royalcaribbean.excalibur.core.impl;

import java.util.Arrays;
import java.util.Date;
import java.util.Properties;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Service;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.royalcaribbean.excalibur.core.KafkaService;

@Component(immediate = true, metatype = false)
@Service(KafkaService.class)
public class KafkaServiceImpl implements KafkaService, Runnable {

	private static final Logger logger = LoggerFactory.getLogger(KafkaServiceImpl.class);

	private Producer<String, String> producer = null;
	private Consumer<String, String> consumer = null;
	
	private boolean ONOFF = false;

	@Activate
	public void init() {
		try {
			this.setupProducer();
			this.setupConsumer();
		} catch (Exception ex) {
			logger.info(ex.getMessage());
		}
	}

	private void setupProducer() {
		try {
			if (producer == null) {
				logger.info("Register Kafka Producer");
				Properties prop = new Properties();
				Thread.currentThread().setContextClassLoader(null);
				prop.put("bootstrap.servers", "localhost:9092,localhost:9094,localhost:9096");
				prop.put("acks", "all");
				prop.put("retries", 0);
				prop.put("batch.size", 16384);
				prop.put("linger.ms", 1);
				prop.put("buffer.memory", 3554432);
				prop.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
				prop.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
				producer = new KafkaProducer<String, String>(prop);
			}
		} catch (Exception ex) {
			logger.info(ex.getMessage());
			ex.printStackTrace(System.out);
		}
	}

	private void setupConsumer() {
		try {
			if (consumer == null) {
				logger.info("Register Kafka Consumer");
				Properties prop = new Properties();
				Thread.currentThread().setContextClassLoader(null);
				prop.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,
						"localhost:9092,localhost:9094,localhost:9096");
				prop.put(ConsumerConfig.GROUP_ID_CONFIG, "g1");
				prop.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
				prop.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
				prop.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
						StringDeserializer.class.getName());
				prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
						StringDeserializer.class.getName());
				// consumerProperties.put(ConsumerConfig.GROUP_ID_CONFIG,
				// "onlyOne");
				// consumerProperties.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG,
				// "roundrobin");
				// consumerProperties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,
				// "earliest");
				consumer = new KafkaConsumer<String, String>(prop);
			}
		} catch (Exception ex) {
			logger.info(ex.getMessage());
			ex.printStackTrace(System.out);
		}
	}
	
	@Override
	public void sendMessage() {
		ProducerRecord<String, String> record = new ProducerRecord<String, String>("test",
				"A kafkaMessage, timestamp=" + new Date());
		producer.send(record);

		ProducerRecord<String, String> record2 = new ProducerRecord<String, String>("test", "key1",
				"A kafkaMessage, timestamp=" + new Date());
		producer.send(record2);

		logger.info("Produced 2 messages");
	}

	@Override
	public void run() {
		synchronized (this) {
			if (ONOFF == true) {
				logger.info("Consuming process is already ON.");
				return;
			}

			try {
				ONOFF = true;
				while (ONOFF) {
					ConsumerRecords<String, String> records = consumer.poll(2000);

					if (records != null) {
						for (ConsumerRecord<String, String> record : records) {
							logger.info("OnMessage => " + record.offset() + ": " + record.partition() + ":"
									+ record.key() + ":" + record.value());
						}
					}
				}
			} finally {
				consumer.close();
				consumer = null;
			}

			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				//do nothing
			}
		}
	}

	@Override
	public void startConsuming() {
		this.setupConsumer();

		logger.info("Consumer subscribe a topic");
		consumer.subscribe(Arrays.asList("test"));
		
		logger.info("Start consuming...");
		new Thread(this).start();
	}

	@Override
	public void stopConsuming() {

		logger.info("Stop consuming...");
		ONOFF = false;
	}

	@Deactivate
	public void end() {
		if (producer != null) {
			producer.close();
		}
		if (consumer != null) {
			consumer.close();
		}
	}
}
