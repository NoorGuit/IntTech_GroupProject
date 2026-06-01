#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#include <Servo.h>

#define TFT_CS 16   //for D1 mini or TFT I2C Connector Shield (V1.1.0 or later)
#define TFT_DC 15   //for D1 mini or TFT I2C Connector Shield (V1.1.0 or later)
#define TFT_RST -1  //for D1 mini or TFT I2C Connector Shield (V1.1.0 or later)
//#define TS_CS 0   //no touch screen //for D1 mini or TFT I2C Connector Shield (V1.1.0 or later)

#define pin_blueIn 5   // GPIO
#define pin_blueOut 2  // GPIO
#define pin_redIn A0    // GPIO //4
#define pin_redOut 0   // GPIO

#define pin_servo 4  // GPIO //1

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);
Servo myservo;

bool bluePressed = false;
bool redPressed = false;

unsigned long prev_buttons = 0;
unsigned long prev_screen = 0;
unsigned long prev_servo = 0;
const unsigned long interval_buttons = 100;
const unsigned long interval_screen = 1000;
const unsigned long interval_servo = 15;

int pos = 0;  // testing

void setup() {
  Serial.begin(115200);
  Serial.print("starting setup");

  tft.begin();
  screenDiagnostics();

  // Input with internal pull-up
  pinMode(pin_blueIn, INPUT_PULLUP);
  pinMode(pin_redIn, INPUT_PULLUP);

  pinMode(pin_blueOut, OUTPUT);
  pinMode(pin_redOut, OUTPUT);

  Serial.print("Setup Complete!");
  Serial.end();

  myservo.attach(pin_servo);
  myservo.write(0);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - prev_buttons >= interval_buttons) {
    prev_buttons = currentMillis;

    bluePressed = buttonState(pin_blueIn);
    redPressed = analogButtonState(pin_redIn);
    buttonLight(bluePressed, pin_blueOut);
    buttonLight(redPressed, pin_redOut);
  }

  if (currentMillis - prev_screen >= interval_screen) {
    prev_screen = currentMillis;
    testText();
  }

  if (currentMillis - prev_servo >= interval_servo) {
    prev_servo = currentMillis;
    test_servo();
  }
}

bool buttonState(uint8_t pin_button) {
  if (digitalRead(pin_button) == LOW) {
    return true;
  } else {
    return false;
  }
}

bool analogButtonState(uint8_t pin_button){
  // Unpressed is typically 1024; pressed is 0
  if (analogRead(pin_button) < 500) {
    return true;
  } else {
    return false;
  }
}

void buttonLight(bool bool_button, uint8_t pin_button) {
  if (bool_button == true) {
    digitalWrite(pin_button, HIGH);
  } else {
    digitalWrite(pin_button, LOW);
  }
}

void test_servo() {
  if (redPressed && pos < 180) {  // goes from 0 degrees to 180 degrees
    pos += 10;
  } else if (pos > 0) {
    pos -= 10;
  }
  myservo.write(pos);
}

unsigned long testText() {
  tft.fillScreen(ILI9341_BLACK);
  unsigned long start = micros();
  tft.setCursor(0, 0);
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(1);
  tft.println("Hello World!");
  tft.setTextColor(ILI9341_YELLOW);
  tft.setTextSize(2);
  tft.println(1234.56);
  tft.setTextColor(ILI9341_RED);
  tft.setTextSize(3);
  tft.println(0xDEADBEEF, HEX);
  tft.println();
  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(5);
  tft.println("Groop");
  tft.setTextSize(2);
  tft.println("I implore thee,");
  tft.setTextSize(1);
  tft.println("my foonting turlingdromes.");
  tft.println("And hooptiously drangle me");
  tft.println("with crinkly bindlewurdles,");
  tft.println("Or I will rend thee");
  tft.println("in the gobberwarts");
  tft.println("with my blurglecruncheon,");
  tft.println("see if I don't!");
  return micros() - start;
}

void screenDiagnostics() {
  // read diagnostics (optional but can help debug problems)
  uint8_t x = tft.readcommand8(ILI9341_RDMODE);
  Serial.print("Display Power Mode: 0x");
  Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDMADCTL);
  Serial.print("MADCTL Mode: 0x");
  Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDPIXFMT);
  Serial.print("Pixel Format: 0x");
  Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDIMGFMT);
  Serial.print("Image Format: 0x");
  Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDSELFDIAG);
  Serial.print("Self Diagnostic: 0x");
  Serial.println(x, HEX);

  Serial.println(F("Benchmark                Time (microseconds)"));
  delay(10);
  Serial.print(F("Screen fill              "));
  Serial.println(testFillScreen());
  delay(500);
}

unsigned long testFillScreen() {
  unsigned long start = micros();
  tft.fillScreen(ILI9341_BLACK);
  yield();
  tft.fillScreen(ILI9341_RED);
  yield();
  tft.fillScreen(ILI9341_GREEN);
  yield();
  tft.fillScreen(ILI9341_BLUE);
  yield();
  tft.fillScreen(ILI9341_BLACK);
  yield();
  return micros() - start;
}