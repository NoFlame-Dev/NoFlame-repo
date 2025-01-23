#include <WiFi.h>
#include <HTTPClient.h>
#include <Ticker.h>

const char* ssid = "NoFlame";             
const char* password = "12345678";        
const char* serverURL = "http://104.35.175.95:5000/fireAlarm"; 

const int buzzerPin = 33;
const int buttonPin = 25;  
bool enableRequests = true;  

volatile bool timerFlag = false;  
unsigned long lastDebounceTime = 0;  
const unsigned long debounceDelay = 50;  
int lastButtonState = HIGH;  

Ticker timer;

// Function to toggle request state
void ButtonTick() {
  int currentButtonState = digitalRead(buttonPin);

  if (currentButtonState != lastButtonState) {
    if (millis() - lastDebounceTime > debounceDelay) {
      if (currentButtonState == LOW) {  // Button pressed
        enableRequests = !enableRequests;  // Toggle requests
        Serial.println(enableRequests ? "Requests enabled." : "Requests paused.");
      }
      lastDebounceTime = millis();
    }
  }

  lastButtonState = currentButtonState;
}

// Timer ISR replacement
void TimerISR() {
  timerFlag = true;
}

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(buttonPin, INPUT_PULLUP);  // Set button pin as input with pull-up resistor
  pinMode(buzzerPin, OUTPUT);
  connectToWiFi();

  // Initialize the timer to call TimerISR every 1 millisecond
  timer.attach_ms(1, TimerISR);

  while( Serial.available() > 0 ) Serial.read();
}

void loop() {
  // Handle  button state
  if (timerFlag) {
    timerFlag = false;  // Clear  flag
    ButtonTick();       
  }

  // If requests are enabled, make an HTTP request
  if (enableRequests) {
    if (WiFi.status() == WL_CONNECTED) {  
      fetchFireAlarmStatus();             // Make the HTTP request
    } else {
      Serial.println("Wi-Fi not connected. Reconnecting...");
      connectToWiFi();                    // Reconnect if disconnected
    }
  } else {
    Serial.println("Requests paused. Press the button to resume.");
    noTone(buzzerPin);
  }

  delay(5000);  // Wait 5 seconds before the next loop iteration
}

void connectToWiFi() {
  WiFi.begin(ssid, password);           // Connect to Wi-Fi
  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void fetchFireAlarmStatus() {
  HTTPClient http;
  http.begin(serverURL);                // Connect to the server
  int httpResponseCode = http.GET();    // Send a GET request

  if (httpResponseCode > 0) {           // Check the response code
    String payload = http.getString();  // Get the response payload
    Serial.print("Server Response: ");
    Serial.println(payload);

    // Handle the response
    if (payload == "true") {
      Serial.println("Fire detected! Take action!");
      tone(buzzerPin, 2000);  // Play 2000 Hz 
      delay(500);             // Wait for 500 milliseconds
      tone(buzzerPin, 3000);  // Play 3000 Hz 
      delay(500); 
    } else if (payload == "false") {
      Serial.println("No fire detected.");
      noTone(buzzerPin);
    }
  } else {
    Serial.print("Error in HTTP request: ");
    Serial.println(httpResponseCode);
  }

  http.end();  // Free the resources
}
