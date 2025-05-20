#include <Arduino.h>
#include <DHT.h>

// ==== PINOS ====
#define PIN_SENSOR_P   12      // Botão: Fósforo
#define PIN_SENSOR_K   14      // Botão: Potássio
#define PIN_SENSOR_PH  34      // LDR: pH (entrada analógica)
#define PIN_DHT        27      // DHT22: Umidade
#define PIN_RELAY      26      // Relé/Bomba
#define PIN_LED        2       // LED status irrigação
#define PIN_MODE_BTN   33      // Botão para alternar modo decisão (externa/interna)

// ==== DHT ====
#define DHTTYPE DHT22
DHT dht(PIN_DHT, DHTTYPE);

// ==== VARIÁVEIS DE ESTADO ====
bool modoExterno = true;      // true = lógica Python, false = lógica local

// ==== PARAMETROS DA REGRA LOCAL SIMPLES ====
const float PH_MIN = 5.5;
const float PH_MAX = 8.5;
const float UMIDADE_SOLO_MIN = 50.0; // %

unsigned long ultimaTrocaModo = 0;
const unsigned long DEBOUNCE_TIME = 400; // ms

// ---- SETUP DE PINOS ----
void setup_pinos() {
  pinMode(PIN_SENSOR_P, INPUT_PULLUP);
  pinMode(PIN_SENSOR_K, INPUT_PULLUP);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_MODE_BTN, INPUT_PULLUP);
}

// ---- LEITURA DE SENSORES ----
bool ler_fosforo() {
  return !digitalRead(PIN_SENSOR_P);
}

bool ler_potassio() {
  return !digitalRead(PIN_SENSOR_K);
}

float ler_ph() {
  int ldrValue = analogRead(PIN_SENSOR_PH); // 0 a 4095
  return map(ldrValue, 0, 4095, 0, 140) / 10.0; // Simula pH 0-14
}

float ler_umidade_solo() {
  float umidade = dht.readHumidity();
  return isnan(umidade) ? -1 : umidade;
}

// ---- ENVIO DE DADOS SERIAL (agora com prefixo DATA:) ----
void enviar_dados_serial(bool fosforo, bool potassio, float ph, float umidade) {
  Serial.print("DATA:");
  Serial.print(fosforo ? "1" : "0"); Serial.print(",");
  Serial.print(potassio ? "1" : "0"); Serial.print(",");
  Serial.print(ph, 2); Serial.print(",");
  Serial.print(umidade, 2); Serial.println();
}

// ---- DECISÃO DE IRRIGAÇÃO EXTERNA (VIA SERIAL) ----
void decidir_irrigacao_externa() {
  unsigned long t0 = millis();
  bool recebeuComando = false;
  while (millis() - t0 < 1000) { // Espera até 1s por comando
    if (Serial.available()) {
      char cmd = Serial.read();
      if (cmd == '1') {
        digitalWrite(PIN_RELAY, HIGH);
        digitalWrite(PIN_LED, HIGH);
        Serial.println("LOG:[INFO] Irrigacao ATIVA (decisao EXTERNA).");
      } else if (cmd == '0') {
        digitalWrite(PIN_RELAY, LOW);
        digitalWrite(PIN_LED, LOW);
        Serial.println("LOG:[INFO] Irrigacao DESLIGADA (decisao EXTERNA).");
      }
      recebeuComando = true;
      break;
    }
  }
  if (!recebeuComando) {
    Serial.println("LOG:[WARN] Nenhum comando externo recebido, mantendo estado anterior da bomba.");
  }
}

// ---- DECISÃO DE IRRIGAÇÃO LOCAL (SIMPLES) ----
bool decidir_irrigacao_local(bool fosforo, bool potassio, float ph, float umidade) {
  if (umidade != -1 && umidade < UMIDADE_SOLO_MIN) {
    Serial.println("LOG:[LOCAL] Solo seco! Deve irrigar.");
    return true;
  }
  if (ph < PH_MIN || ph > PH_MAX) {
    Serial.println("LOG:[LOCAL] pH fora do ideal! Deve irrigar.");
    return true;
  }
  if (!fosforo || !potassio) {
    Serial.println("LOG:[LOCAL] Nutriente ausente! Deve irrigar.");
    return true;
  }
  Serial.println("LOG:[LOCAL] Condicoes normais, nao irrigar.");
  return false;
}

// ---- EXECUTA IRRIGAÇÃO LOCAL ----
void executar_irrigacao_local(bool irrigar) {
  if (irrigar) {
    digitalWrite(PIN_RELAY, HIGH);
    digitalWrite(PIN_LED, HIGH);
    Serial.println("LOG:[INFO] Irrigacao ATIVA (decisao LOCAL).");
  } else {
    digitalWrite(PIN_RELAY, LOW);
    digitalWrite(PIN_LED, LOW);
    Serial.println("LOG:[INFO] Irrigacao DESLIGADA (decisao LOCAL).");
  }
}

// ---- CHECA BOTÃO E ALTERNAR MODO ----
void checar_e_alternar_modo() {
  static bool lastBtn = HIGH;
  bool btn = digitalRead(PIN_MODE_BTN);
  unsigned long agora = millis();

  if (lastBtn == HIGH && btn == LOW && (agora - ultimaTrocaModo > DEBOUNCE_TIME)) {
    modoExterno = !modoExterno;
    ultimaTrocaModo = agora;
    Serial.print("LOG:[MODO] Mudando para decisao ");
    Serial.println(modoExterno ? "EXTERNA (Python)" : "LOCAL (ESP32)");
  }
  lastBtn = btn;
}

// ---- SETUP ----
void setup() {
  Serial.begin(115200);
  delay(5000); // wait until Platformio monitor is active
  setup_pinos();
  dht.begin();

  digitalWrite(PIN_RELAY, LOW);
  digitalWrite(PIN_LED, LOW);

  Serial.println("LOG:Sistema de irrigacao iniciado!");
  Serial.println("LOG:[MODO] Inicial: decisao EXTERNA (Python)");
}

// ---- LOOP PRINCIPAL ----
void loop() {
  checar_e_alternar_modo();

  bool fosforo = ler_fosforo();
  bool potassio = ler_potassio();
  float ph = ler_ph();
  float umidade = ler_umidade_solo();

  enviar_dados_serial(fosforo, potassio, ph, umidade);

  if (modoExterno) {
    decidir_irrigacao_externa();
  } else {
    bool irrigar = decidir_irrigacao_local(fosforo, potassio, ph, umidade);
    executar_irrigacao_local(irrigar);
  }

  delay(2000);
}
