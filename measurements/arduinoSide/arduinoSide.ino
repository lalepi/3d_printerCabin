#include <DHT.h>
#include <DHT_U.h>

#include <LiquidCrystal.h>

// #include <Servo.h>
#include <LiquidCrystal_I2C.h>
// enter the I2C address and the dimensions of your LCD here
LiquidCrystal_I2C lcd(0x27, 16, 2);
////////////DHT///////////////
// Libraries
#include <DHT.h>

// Constants
#define DHTPIN1 6            // what pin we're connected to
#define DHTPIN2 7            // what pin we're connected to
#define DHTTYPE1 DHT11       // DHT 11  (AM2302)
#define DHTTYPE2 DHT22       // DHT 22  (AM2302)
DHT dht1(DHTPIN1, DHTTYPE1); //// Initialize DHT sensor for normal 16mhz Arduino
DHT dht2(DHTPIN2, DHTTYPE2); //// Initialize DHT sensor for normal 16mhz Arduino
// Variables
int chk;
int hum;     // Stores humidity value DHT22
int hum_11;  // Stores humidity value DHT11
int temp;    // Stores temperature value DHT22
int temp_11; // Stores temperature value DHT11
char ch;


int previousHum;
int previousHum_11;
int previousTemp;
int previousTemp_11;
//============================================

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char API_kaupunki[buffSize] = {0};
int RPI_temp = 0;
int ulkolampotila = 0;

int previousRPI_temp;
int previousUlkolampotila;

//============================================

// button initilization
//
const int buttonPin = 5; // the number of the pushbutton pin

// variables

byte lastButtonState = LOW;
byte currentButtonState = LOW;
unsigned long lastButtonDebounceTime = 0;
unsigned long buttonDebounceDelay = 20;



int count_value = 0;
//============================================

void setup()
{

    lcd.init();
    
    lcd.backlight();
    dht1.begin();
    dht2.begin();

    Serial.begin(115200);

    delay(500); // delay() is OK in setup as it only happens once

    // tell the PC we are ready
    Serial.println("<Arduino is ready>");
    lcd.clear();
}

//============================================
void loop()
{
    DHT_measurement();
    Lceedee();
    getDataFromPC();
    replyToPC();
    button();
    //delay(1000);
}

//============================================
void getDataFromPC()
{

    // receive data from PC and save it into inputBuffer
    delay(200);
    if (Serial.available() > 0)
    {

        char x = Serial.read();

        // the order of these IF clauses is significant

        if (x == endMarker)
        {
            readInProgress = false;
            newDataFromPC = true;
            inputBuffer[bytesRecvd] = 0;
            parseData();
        }

        if (readInProgress)
        {
            inputBuffer[bytesRecvd] = x;
            bytesRecvd++;
            if (bytesRecvd == buffSize)
            {
                bytesRecvd = buffSize - 1;
            }
        }

        if (x == startMarker)
        {
            bytesRecvd = 0;
            readInProgress = true;
        }
    }
}

//============================================

void parseData()
{

    // split the data into its parts

    char *strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(inputBuffer, ","); // get the first part - the string
    strcpy(API_kaupunki, strtokIndx);      // copy it to messageFromPC

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    RPI_temp = atoi(strtokIndx);    // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    ulkolampotila = atoi(strtokIndx); // convert this part to a float
}

//============================================

void replyToPC()
{

    if (newDataFromPC)
    {
        newDataFromPC = false;
        Serial.print("< API kutsu kaupunki ");
        Serial.print(API_kaupunki);
        Serial.print(" Raspberryn lampotila ");
        Serial.print(RPI_temp);
        Serial.print(" Ulkolampotila ");
        Serial.print(ulkolampotila);

        Serial.print(" Alakaapin lampotila ");
        Serial.print(temp_11);
        Serial.print(" Alakaapin Kosteus% ");
        Serial.print(hum_11);

        Serial.print(" Ylakaapin lampotila ");
        Serial.print(temp);
        Serial.print(" Ylakaapin Kosteus% ");
        Serial.print(hum);

        Serial.println(">");
        Serial.println("<Arduino is ready>");
    }
}

//============================================

void DHT_measurement()
{

    hum_11 = dht1.readHumidity();
    temp_11 = dht1.readTemperature();
    hum = dht2.readHumidity();
    temp = dht2.readTemperature();
}

//============================================

void button()
{
    // read the state of the pushbutton value:
     byte readValue = digitalRead(buttonPin);

    // check if the pushbutton is pressed. If it is, then the buttonState is HIGH:

    if (readValue != lastButtonState)
    {
      lastButtonDebounceTime = millis();
    }
    if (millis() - lastButtonDebounceTime > buttonDebounceDelay) {

      if (readValue != currentButtonState) {
        currentButtonState = readValue;     
          if (currentButtonState == HIGH) {
            count_value++;
            lcd.clear();
      }
    }
}

    if (count_value > 3)
    {
        count_value = 0;
    }

    lastButtonState = readValue;

}

//============================================

void Lceedee()
{

switch (count_value) {

  case 0:

  if (temp_11 != previousTemp_11)
  {
        lcd.setCursor(0, 0); // Set cursor to character 2 on line 0
        lcd.print("UPtemp:");
        lcd.setCursor(8, 0); // Set cursor to character 5 on line 1
        lcd.print(temp_11);
        lcd.setCursor(12, 0);
        lcd.print("C");
  }
if (hum_11 != previousHum_11)
  {
        lcd.setCursor(0, 1);
        lcd.print("Humid :");
        lcd.setCursor(8, 1);
        lcd.print(hum_11);
        lcd.setCursor(12, 1);
        lcd.print("%");
  }
        break;
    
  case 1:
  if (temp != previousTemp)
  {
        lcd.setCursor(0, 0);
        lcd.print("DOtemp:");
        lcd.setCursor(8, 0);
        lcd.print(temp);
        lcd.setCursor(12, 0);
        lcd.print("C");
  }
  if (hum != previousHum)
  {
        lcd.setCursor(0, 1);
        lcd.print("Humid :");
        lcd.setCursor(8, 1);
        lcd.print(hum);
        lcd.setCursor(12, 1);
        lcd.print("%");

  }
        break;
  
  case 2:
   if (RPI_temp != previousRPI_temp)
  {
        lcd.setCursor(1, 0);
        lcd.print("Raspberry CPU");

        lcd.setCursor(1, 1);
        lcd.print("TEMP: ");
        lcd.setCursor(7, 1);
        lcd.print(RPI_temp);
        lcd.setCursor(10, 1);
        lcd.print("C");

  }
        break;

  case 3:

    if (ulkolampotila != previousUlkolampotila)
  {
        lcd.setCursor(3, 0);
        lcd.print(API_kaupunki);
        lcd.setCursor(0, 1);
        lcd.print("TEMP: ");
        lcd.setCursor(6, 1);
        lcd.print(ulkolampotila);
        lcd.setCursor(12, 1);
        lcd.print("C");

  }
        break;
  default:
        break;


previousHum = hum;
previousHum_11 = hum_11;
previousTemp = temp;
previousTemp_11 = temp_11;
previousRPI_temp = RPI_temp;
previousUlkolampotila = ulkolampotila;

}
}

//============================================