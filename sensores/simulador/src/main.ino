#include <Arduino.h>
#include <DHT.h>

// ==== PINOS ====
#define PIN_SENSOR_P   12      // btn1 (Fósforo)
#define PIN_SENSOR_K   14      // btn2 (Potássio)
#define PIN_SENSOR_PH  33      // LDR: pH (entrada analógica)
#define PIN_DHT        2       // DHT22: Umidade
#define PIN_RELAY      26      // Relé/Bomba
#define PIN_MODO_DECISAO 13    // Slide Switch

#define DHTTYPE DHT22
DHT dht(PIN_DHT, DHTTYPE);

const float PH_MIN = 5.5;
const float PH_MAX = 8.5;
const float UMIDADE_SOLO_MIN = 50.0; // %

void setup_pinos() {
  pinMode(PIN_SENSOR_P, INPUT);
  pinMode(PIN_SENSOR_K, INPUT);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_MODO_DECISAO, INPUT); // Slide Switch entre GND e 3V3
}

bool ler_fosforo() {
  return digitalRead(PIN_SENSOR_P) == HIGH;
}

bool ler_potassio() {
  return digitalRead(PIN_SENSOR_K) == HIGH;
}

float ler_ph() {
  int ldrValue = analogRead(PIN_SENSOR_PH); // 0 a 4095
  return map(ldrValue, 0, 4095, 0, 140) / 10.0; // Simula pH 0-14
}

float ler_umidade_solo() {
  float umidade = dht.readHumidity();
  return isnan(umidade) ? -1 : umidade;
}

void enviar_dados_serial(bool fosforo, bool potassio, float ph, float umidade) {
  Serial.print("DATA:");
  Serial.print(fosforo ? "1" : "0"); Serial.print(",");
  Serial.print(potassio ? "1" : "0"); Serial.print(",");
  Serial.print(ph, 2); Serial.print(",");
  Serial.print(umidade, 2); Serial.println();
}

void decidir_irrigacao_externa() {
  unsigned long t0 = millis();
  bool recebeuComando = false;
  while (millis() - t0 < 1000) {
    if (Serial.available()) {
      char cmd = Serial.read();
      if (cmd == '1') {
        digitalWrite(PIN_RELAY, HIGH);
        Serial.println("LOG:[INFO] Irrigacao ATIVA (decisao EXTERNA).");
      } else if (cmd == '0') {
        digitalWrite(PIN_RELAY, LOW);
        Serial.println("LOG:[INFO] Irrigacao DESLIGADA (decisao EXTERNA).");
      }
      recebeuComando = true;
      break;
    }
  }
  if (!recebeuComando) {
    digitalWrite(PIN_RELAY, LOW);
    Serial.println("LOG:[WARN] Nenhum comando externo recebido, mantendo estado anterior da bomba.");
  }
}

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

void executar_irrigacao_local(bool irrigar) {
  if (irrigar) {
    digitalWrite(PIN_RELAY, HIGH);
    Serial.println("LOG:[INFO] Irrigacao ATIVA (decisao LOCAL).");
  } else {
    digitalWrite(PIN_RELAY, LOW);
    Serial.println("LOG:[INFO] Irrigacao DESLIGADA (decisao LOCAL).");
  }
}

void setup() {
  Serial.begin(115200);
  setup_pinos();
  dht.begin();
  digitalWrite(PIN_RELAY, LOW);
  Serial.println("LOG:Sistema de irrigacao iniciado!");
}

void loop() {
  bool modoExterno = digitalRead(PIN_MODO_DECISAO) == HIGH;

  Serial.print("LOG:[MODO] Modo atual: ");
  Serial.println(modoExterno ? "EXTERNO" : "LOCAL");

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
