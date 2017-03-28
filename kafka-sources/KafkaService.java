package com.royalcaribbean.excalibur.core;

public interface KafkaService {
	
	public void sendMessage();
	
	public void startConsuming();
	public void stopConsuming();
}
