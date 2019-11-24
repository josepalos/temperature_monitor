#include <ArduinoHttpClient.h>
#include <WiFi101.h>


char ssid[] = "svila";
char pass[] = "12341234";
char serverAddress[] = "192.168.137.145";
char post_url[] = "/temperatures/new_temperature";
int port = 8000;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;

void setup() {
  // put your setup code here, to run once:
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

String get_data_string(int* temperatures){
  char temps[25];
  for(int i = 0; i < 12; i++){
    sprintf(temps + (i*2), "%x", temperatures[i]);
  }
  String postData = "data=" + String(temps);
  
  return postData;
}

void send_temperatures(int* temperatures){
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

  Serial.println("Wait five seconds");
  delay(5000);
}

void loop() {
  int temperatures[12] = {25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25};
  send_temperatures(temperatures);
}
