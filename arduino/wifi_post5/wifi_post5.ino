#include <HttpClient.h>
#include <WiFi101.h>

//Setup Wifi Parameters
char ssid[] = "svila";    
char pass[] = "12341234";
char serverAddress[] = "http://www.arduino.cc"; 
int port = 8000;

//WiFiClient wifi;
//HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;
String response;
int statusCode = 0;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);

void setup() 
{
  Serial.begin(9600);
  while ( status != WL_CONNECTED) 
  {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    delay(6000);
  }

  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void loop() 
{
  Serial.println("making POST request");
  String contentType = "application/x-www-form-urlencoded";
  String postData = "data=0";

  client.post("/temperatures/new_temperature", contentType, postData);

  // read the status code and body of the response
  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  Serial.println("Wait five seconds");
  delay(5000);
}
