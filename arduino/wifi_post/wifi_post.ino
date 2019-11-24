#include <SimpleDHT.h>

#include <ArduinoHttpClient.h>
#include <WiFi101.h>
#include <SimpleDHT.h>

#define DHTPIN 2

SimpleDHT11 dht11;

char ssid[] = "svila";
char pass[] = "12341234";
char serverAddress[] = "192.168.137.145";  // server address
char post_url[] = "/temperatures/new_temperature";
int port = 8000;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;

void setup() {
  Serial.begin(9600);
  
  while (status != WL_CONNECTED){
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);

    status = WiFi.begin(ssid, pass);
  }

  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

String get_data_string(byte* temperatures){
  char temps[25];
  for(int i = 0; i < 12; i++){
    sprintf(temps + (i*2), "%02x", temperatures[i]);
    Serial.println(temps);
  }
  String postData = "data=" + String(temps);
  
  return postData;
}

void send_temperatures(byte* temperatures){
  Serial.println("Making a POST request");
  String postData = get_data_string(temperatures);

  Serial.print("Sending data: ");
  Serial.println(postData);
  
  String contentType = "application/x-www-form-urlencoded";
  client.post(post_url, contentType, postData);

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);
}

void loop() {
  byte temperatures[12];
  for (int i = 0; i <  12; i++){
    byte temperature = 0;
    byte humidity = 0;
    byte data[40] = {0};
    if (dht11.read(DHTPIN, &temperature, &humidity, data)) {
      Serial.println("Read DHT11 failed");
    }else{
      temperatures[i] = temperature;
      Serial.print("Read temperature: ");
      Serial.println(temperature);
    }
    delay(60 * 1000);
  }
  send_temperatures(temperatures);
}
