#include <Arduino.h>    
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

//------------------Sesnor Pins and Variables----------------------
#include <SPI.h>
#include <MFRC522.h>
#include<Servo.h>
Servo atm;
//--------------------------------------------------
//GPIO 0 --> D3
//GPIO 2 --> D4
const uint8_t RST_PIN = D3;
const uint8_t SS_PIN = D4;
//--------------------------------------------------
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;        
//--------------------------------------------------
/* Be aware of Sector Trailer Blocks */
int blockNum = 4;
/* Create array to read data from Block */
/* Length of buffer should be 4 Bytes 
more than the size of Block (16 Bytes) */
byte bufferLen = 18;
byte readBlockData[18];
//--------------------------------------------------
MFRC522::StatusCode status;
//--------------------------------------------------


//-------------------------------------------------------------------
// Insert your network credentials
#define WIFI_SSID "shital"
#define WIFI_PASSWORD "pallavigadhave14"

// Insert Firebase project API Key
#define API_KEY "AIzaSyCpUI4UFBpr5b_L3Uk942Po0MqErfhDVVk"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://augmentedreality-af310-default-rtdb.firebaseio.com/" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;
int intValue=-1;

void setup()
{
  //--------------Pinmodes-------------------
    Serial.begin(115200);
    atm.attach(16);  //D0
  //------------------------------------------------------
  //Initialize SPI bus
  SPI.begin();
  //------------------------------------------------------
  //Initialize MFRC522 Module
  mfrc522.PCD_Init();
  Serial.println("Scan a MIFARE 1K Tag to write data...");
  //------------------------------------------------------
  //-----------------------------------------

  //dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop()
{
    /*-----------------Sensor Read Code-------------------------------*/
    String uidString = "";
  //------------------------------------------------------------------------------
    /* Prepare the ksy for authentication */
    /* All keys are set to FFFFFFFFFFFFh at chip delivery from the factory */
    for (byte i = 0; i < 6; i++){
      key.keyByte[i] = 0xFF;
    }
    //------------------------------------------------------------------------------
    /* Look for new cards */
    /* Reset the loop if no new card is present on RC522 Reader */
    if ( ! mfrc522.PICC_IsNewCardPresent()){return;}
    //------------------------------------------------------------------------------
    /* Select one of the cards */
    if ( ! mfrc522.PICC_ReadCardSerial()) {return;}
    //------------------------------------------------------------------------------
    Serial.print("\n");
    Serial.println("*Card Detected*");
    /* Print UID of the Card */
    Serial.print(F("Card UID:"));
    for (byte i = 0; i < mfrc522.uid.size; i++){
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
      uidString += String(mfrc522.uid.uidByte[i], HEX);
      Serial.println(uidString);
    }
    Serial.print("\n");
    /* Print type of card (for example, MIFARE 1K) */
    Serial.print(F("PICC type: "));
    MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
    Serial.println(mfrc522.PICC_GetTypeName(piccType));
      
   //-------------------------------------------------------------------
  //if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    // sendDataPrevMillis = millis();
    // // Write an Int number on the database path test/int
    // if (Firebase.RTDB.setInt(&fbdo, "AE197/level", (100-per))){
    //   Serial.println("PASSED");
    //   Serial.println("PATH: " + fbdo.dataPath());
    //   Serial.println("TYPE: " + fbdo.dataType());
    // }
    // else {
    //   Serial.println("FAILED");
    //   Serial.println("REASON: " + fbdo.errorReason());
    // }

    // if (Firebase.RTDB.setInt(&fbdo, "nmims/hr", random(60,90))){
    //   Serial.println("PASSED");
    //   Serial.println("PATH: " + fbdo.dataPath());
    //   Serial.println("TYPE: " + fbdo.dataType());
    // }
    // else {
    //   Serial.println("FAILED");
    //   Serial.println("REASON: " + fbdo.errorReason());
    // }
    // count++;
    
    // // Write an Float number on the database path test/float
    // if (Firebase.RTDB.setFloat(&fbdo, "nmims/humidity", h)){
    //   Serial.println("PASSED");
    //   Serial.println("PATH: " + fbdo.dataPath());
    //   Serial.println("TYPE: " + fbdo.dataType());
    // }
    // else {
    //   Serial.println("FAILED");
    //   Serial.println("REASON: " + fbdo.errorReason());
    // }

    // if (Firebase.RTDB.setFloat(&fbdo, "nmims/temp", t)){
    //   Serial.println("PASSED");
    //   Serial.println("PATH: " + fbdo.dataPath());
    //   Serial.println("TYPE: " + fbdo.dataType());
    // }
    // else {
    //   Serial.println("FAILED");
    //   Serial.println("REASON: " + fbdo.errorReason());
    // }

    if (Firebase.RTDB.getInt(&fbdo, "/AE235/otp")) {
      if (fbdo.dataType() == "int") {
        intValue = fbdo.intData();
        Serial.println(intValue);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    /*-------------Control Code----------------------*/
    if(intValue == 0 && uidString.endsWith("419a")) // && uidString == " 9A448419a"
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }
    else if(intValue == 1 && uidString.endsWith("7499"))
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }

    else if(intValue == 2 && uidString.endsWith("ad14"))
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }

    else if(intValue == 3 && uidString.endsWith("6c9a"))
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }

    else if(intValue == 4 && uidString.endsWith("6d36"))
    {
       Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }

    else if(intValue == 5 && uidString.endsWith("30fd"))
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }
    else if(intValue == 6 && uidString.endsWith("ec96"))
    {
      Serial.println("RFID Matched");
      atm.write(90);
      delay(2000);
      atm.write(0);
    }
    else
    {
      Serial.println("RFID Failed");
    }
  /* -------------------------------------------------------*/
    delay(5000);
    
  //}
}
