#include <Arduino.h>
#include <DHT.h>

// ==== PINOS ====
#define PIN_SENSOR_P   12      // Botão para simular presença de fósforo
#define PIN_SENSOR_K   14      // Botão para simular presença de potássio
#define PIN_SENSOR_PH  33      // LDR para simular leitura de pH
#define PIN_DHT        2       // Sensor DHT22 para medir umidade
#define PIN_RELAY      26      // Relé para controlar a bomba de irrigação
#define PIN_MODO_DECISAO 13    // Slide Switch para alternar entre modos de decisão

#define DHTTYPE DHT22
DHT dht(PIN_DHT, DHTTYPE);

const float PH_MIN = 5.5;       // Limite mínimo do pH ideal
const float PH_MAX = 8.5;       // Limite máximo do pH ideal
const float UMIDADE_SOLO_MIN = 50.0; // Umidade mínima do solo em %

void setup_pinos() {
  // Configura os pinos como entrada ou saída
  pinMode(PIN_SENSOR_P, INPUT);
  pinMode(PIN_SENSOR_K, INPUT);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_MODO_DECISAO, INPUT); // Slide Switch entre GND e 3V3
}

bool ler_fosforo() {
  // Lê o estado do botão que simula a presença de fósforo
  return digitalRead(PIN_SENSOR_P) == HIGH;
}

bool ler_potassio() {
  // Lê o estado do botão que simula a presença de potássio
  return digitalRead(PIN_SENSOR_K) == HIGH;
}

float ler_ph() {
  // Lê o valor analógico do LDR e converte para um valor de pH (0-14)
  int ldrValue = analogRead(PIN_SENSOR_PH); // 0 a 4095
  return map(ldrValue, 0, 4095, 0, 140) / 10.0; // Simula pH 0-14
}

float ler_umidade_solo() {
  // Lê a umidade do solo usando o sensor DHT22
  float umidade = dht.readHumidity();
  return isnan(umidade) ? -1 : umidade; // Retorna -1 se a leitura falhar
}

void enviar_dados_serial(bool modoDecisao, bool fosforo, bool potassio, float ph, float umidade) {
  // Envia os dados dos sensores e o modo de decisão via Serial
  Serial.print("DATA:");
  Serial.print("M="); Serial.print(modoDecisao ? "E" : "L"); Serial.print(",");
  Serial.print("P="); Serial.print(fosforo ? "1" : "0"); Serial.print(",");
  Serial.print("K="); Serial.print(potassio ? "1" : "0"); Serial.print(",");
  Serial.print("PH="); Serial.print(ph, 2); Serial.print(",");
  Serial.print("H="); Serial.print(umidade, 2); Serial.println();
}

void decidir_irrigacao_externa() {
  // Aguarda comandos via Serial para ativar ou desativar a irrigação
  unsigned long t0 = millis();
  while (millis() - t0 < 1000) { // Espera até 1 segundo por um comando
    if (Serial.available()) {
      char cmd = Serial.read();
      if (cmd == '1' || cmd == '0') {
        executar_irrigacao_local(cmd == '1', true); // Executa irrigação com base no comando
      }
      break;
    }
  }
}

void decidir_irrigacao_local(bool modoDecisao, bool fosforo, bool potassio, float ph, float umidade) {
  // Decide automaticamente se deve irrigar com base nos sensores
  bool irrigar = false;
  if (umidade != -1 && umidade < UMIDADE_SOLO_MIN) {
    Serial.println("LOG:[LOCAL] Solo seco! Deve irrigar.");
    irrigar = true;
  }
  if (ph < PH_MIN || ph > PH_MAX) {
    Serial.println("LOG:[LOCAL] pH fora do ideal! Deve irrigar.");
    irrigar = true;
  }
  if (!fosforo || !potassio) {
    Serial.println("LOG:[LOCAL] Nutriente ausente! Deve irrigar.");
    irrigar = true;
  }
  executar_irrigacao_local(irrigar, false); // Executa irrigação com base na decisão
}

void executar_irrigacao_local(bool irrigar, bool modoDecisao) {
  // Liga ou desliga a bomba de irrigação e registra no log
  if (irrigar) {
    digitalWrite(PIN_RELAY, HIGH);
    Serial.print("LOG:[INFO] Irrigacao ATIVA. Decisao: "); Serial.println(modoDecisao ? "EXTERNO" : "LOCAL");
  } else {
    digitalWrite(PIN_RELAY, LOW);
    Serial.print("LOG:[INFO] Irrigacao DESLIGADA. Decisao: "); Serial.println(modoDecisao ? "EXTERNO" : "LOCAL");
  }
}

void setup() {
  // Configura o sistema e inicializa os sensores
  Serial.begin(115200);
  setup_pinos();
  dht.begin();
  digitalWrite(PIN_RELAY, LOW); // Garante que a bomba começa desligada
  Serial.println("LOG:Sistema de irrigacao iniciado!");
}

void loop() {
  // Loop principal que alterna entre os modos de decisão e coleta dados dos sensores
  bool modoDecisao = digitalRead(PIN_MODO_DECISAO) == HIGH; // Lê o estado do Slide Switch
  
  bool fosforo = ler_fosforo();
  bool potassio = ler_potassio();
  float ph = ler_ph();
  float umidade = ler_umidade_solo();

  enviar_dados_serial(modoDecisao, fosforo, potassio, ph, umidade); // Envia os dados via Serial

  if (modoDecisao) {
    decidir_irrigacao_externa(); // Modo de decisão externa
  } else {
    decidir_irrigacao_local(modoDecisao, fosforo, potassio, ph, umidade); // Modo de decisão local
  }

  delay(2000); // Aguarda 2 segundos antes de repetir o loop
}
