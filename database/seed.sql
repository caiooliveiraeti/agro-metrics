-- Sensores para Área 1
INSERT INTO areas (area_id, nome, latitude, longitude) VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Área 1', -23.5505, -46.6333);
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440003', 'umidade', '550e8400-e29b-41d4-a716-446655440000', -23.5505, -46.6333, 1, '123001');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440004', 'ph', '550e8400-e29b-41d4-a716-446655440000', -23.5505, -46.6333, 1, '123002');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440005', 'ce', '550e8400-e29b-41d4-a716-446655440000', -23.5505, -46.6333, 1, '123003');
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440003', 75.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440003', 76.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440004', 6.5);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440004', 6.6);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440005', 1.2);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440005', 1.3);

-- Sensores para Área 2
INSERT INTO areas (area_id, nome, latitude, longitude) VALUES ('550e8400-e29b-41d4-a716-446655440001', 'Área 2', -22.9068, -43.1729);
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440006', 'umidade', '550e8400-e29b-41d4-a716-446655440001', -22.9068, -43.1729, 1, '123004');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440007', 'ph', '550e8400-e29b-41d4-a716-446655440001', -22.9068, -43.1729, 1, '123005');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440008', 'ce', '550e8400-e29b-41d4-a716-446655440001', -22.9068, -43.1729, 1, '123006');
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440006', 80.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440006', 81.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440007', 7.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440007', 7.1);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440008', 1.5);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440008', 1.6);

-- Sensores para Área 3
INSERT INTO areas (area_id, nome, latitude, longitude) VALUES ('550e8400-e29b-41d4-a716-446655440002', 'Área 3', -19.9167, -43.9345);
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-446655440009', 'umidade', '550e8400-e29b-41d4-a716-446655440002', -19.9167, -43.9345, 1, '123007');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-44665544000a', 'ph', '550e8400-e29b-41d4-a716-446655440002', -19.9167, -43.9345, 1, '123008');
INSERT INTO sensores (sensor_id, tipo, area_id, latitude, longitude, ativo, codigo_patrimonio) VALUES ('550e8400-e29b-41d4-a716-44665544000b', 'ce', '550e8400-e29b-41d4-a716-446655440002', -19.9167, -43.9345, 1, '123009');
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440009', 85.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-446655440009', 86.0);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-44665544000a', 6.8);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-44665544000a', 6.9);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-44665544000b', 1.8);
INSERT INTO leituras (sensor_id, valor) VALUES ('550e8400-e29b-41d4-a716-44665544000b', 1.9);
